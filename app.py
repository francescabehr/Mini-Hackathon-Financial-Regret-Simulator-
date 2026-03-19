import re
import math
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///regret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class RegretEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    decision_text = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    insight = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def fetch_exchange_rate(base='USD', target='USD'):
    if base.upper() == target.upper():
        return 1.0
    try:
        response = requests.get(f'https://api.frankfurter.app/latest?from={base.upper()}&to={target.upper()}')
        response.raise_for_status()
        rate = response.json().get('rates', {}).get(target.upper())
        return float(rate) if rate is not None else None
    except Exception:
        return None


def calc_future_value(amount, years, annual_rate=0.07):
    return amount * ((1 + annual_rate) ** years)


def parse_decision(raw_text):
    text = raw_text.strip().lower()

    # daily cost pattern
    m = re.search(r'\$?([0-9]+(?:\.[0-9]+)?)\s*(?:per\s*)?(?:day|daily|every day)', text)
    if m:
        daily = float(m.group(1))
        annual = daily * 365
        category = 'Daily Spending' 
        insight = (f"You spend ${daily:.2f} daily -> ${annual:.2f} annually. "
                   "If invested at 7% for 10 years, this becomes much larger.")
        amount = annual
        years = 10
        future = calc_future_value(annual, years)
        potential_gain = future - annual
        score = regret_score(amount, potential_gain, years, recurring=True)
        return category, amount, score, insight, future

    # monthly subscription pattern
    m = re.search(r'\$?([0-9]+(?:\.[0-9]+)?)\s*(?:per\s*)?(?:month|mo|monthly)', text)
    if m:
        monthly = float(m.group(1))
        annual = monthly * 12
        category = 'Subscription' 
        insight = (f"Your subscription costs ${monthly:.2f}/month -> ${annual:.2f}/year. "
                   "Over 5 years, that could be invested instead.")
        amount = annual
        years = 5
        future = calc_future_value(annual, years)
        potential_gain = future - annual
        score = regret_score(amount, potential_gain, years, recurring=True)
        return category, amount, score, insight, future

    # buy/sell investment regret pattern
    m = re.search(r'bought\s+([^\s]+)\s+at\s+\$?([0-9,]+(?:\.[0-9]+)?)\s+and\s+sold\s+at\s+\$?([0-9,]+(?:\.[0-9]+)?)', text)
    if m:
        asset = m.group(1)
        buy = float(m.group(2).replace(',', ''))
        sell = float(m.group(3).replace(',', ''))
        category = 'Trading Loss'
        loss = buy - sell
        pct_loss = (loss / buy) * 100 if buy != 0 else 0
        insight = (f"You bought {asset} at ${buy:.2f} and sold at ${sell:.2f}, a loss of ${loss:.2f} ({pct_loss:.1f}%).")
        amount = abs(loss)
        years = 3
        future = calc_future_value(amount, years)
        potential_gain = future - amount
        score = regret_score(abs(loss), potential_gain, years, recurring=False, loss_pct=pct_loss)
        return category, amount, score, insight, future

    # currency convert regret pattern
    m = re.search(r'converted\s+\$?([0-9,]+(?:\.[0-9]+)?)\s*(\w{3})\s+to\s+(\w{3})', text)
    if m:
        amount = float(m.group(1).replace(',', ''))
        from_cur = m.group(2).upper()
        to_cur = m.group(3).upper()
        category = 'Currency Exchange'
        rate = fetch_exchange_rate(from_cur, to_cur)
        if rate is None:
            insight = f"Could not fetch exchange rate for {from_cur}->{to_cur}."
            score = 20
            future = amount
        else:
            exchanged = amount * rate
            insight = (f"Converted {amount:.2f} {from_cur} -> {exchanged:.2f} {to_cur} at rate {rate:.4f}. "
                       "Relative fee + regret measured by currency risk.")
            # use hypothetical value if stable USD over 3 years
            opp = calc_future_value(amount, 3)
            potential_gain = opp - amount
            score = regret_score(amount, potential_gain, 3, recurring=False)
            future = exchanged
        return category, amount, score, insight, future

    # fallback one-time purchase pattern
    m = re.search(r'\$?([0-9]+(?:\.[0-9]+)?)', text)
    if m:
        amount = float(m.group(1))
        category = 'One-time Purchase'
        intention = 'luxury' if 'luxury' in text or 'expensive' in text else 'general'
        insight = (f"One-time expense ${amount:.2f} treated as {intention}. "
                   "Consider that investing this amount for 5 years could grow significantly.")
        years = 5
        future = calc_future_value(amount, years)
        potential_gain = future - amount
        score = regret_score(amount, potential_gain, years, recurring=False)
        return category, amount, score, insight, future

    # no numeric found
    category = 'Unknown'
    amount = 0
    score = 0
    insight = "Could not parse numeric value; please provide a clearer purchase statement."
    future = 0
    return category, amount, score, insight, future


def regret_score(base_amount, potential_gain, years, recurring=False, loss_pct=0):
    # factor 1: opportunity loss normalized
    opp_factor = min(1.0, potential_gain / (base_amount + 1e-9))
    if opp_factor < 0:
        opp_factor = min(1.0, abs(opp_factor))

    # factor 2: time significance (long recurring -> higher)
    time_factor = min(1.0, years / 10) if years > 0 else 0

    # factor 3: behavioural penalty for losses / habits
    habit_factor = 0.5 if recurring else 0.3
    loss_factor = min(1.0, abs(loss_pct) / 100)

    raw_score = (0.5 * opp_factor + 0.3 * time_factor + 0.2 * habit_factor + 0.1 * loss_factor) * 100
    score = max(0, min(100, raw_score))
    return round(score, 1)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    decision = request.form.get('decision', '')
    if not decision:
        return redirect(url_for('index'))

    category, amount, score, insight, future = parse_decision(decision)
    entry = RegretEntry(
        decision_text=decision,
        category=category,
        score=score,
        insight=insight,
        amount=amount
    )
    db.session.add(entry)
    db.session.commit()

    return render_template(
        'result.html',
        decision=decision,
        category=category,
        amount=amount,
        score=score,
        insight=insight,
        future=future,
        range_label=score_label(score)
    )


@app.route('/history', methods=['GET'])
def history():
    entries = RegretEntry.query.order_by(RegretEntry.created_at.desc()).limit(50).all()
    return render_template('history.html', entries=entries)


def score_label(score):
    if score <= 20:
        return 'Probably fine'
    if score <= 50:
        return 'Mild regret'
    if score <= 80:
        return 'Risky decision'
    return 'High regret'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
