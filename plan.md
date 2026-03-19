# Our Idea

## Concept 

- Build a Flask app to help users answer: "What might I regret about this purchase later?"
- Input: natural language financial decision (one-time/outcome, recurring, investment, currency swap)
- Output: regret score (0-100), category, insight, and estimated opportunity cost

## Implementation Plan

1. scaffold project files
	- `app.py` (Flask app, routes, parser, regret formula)
	- `templates/index.html`, `result.html`, `history.html`
	- `static/styles.css`
	- `requirements.txt` with `Flask`, `Flask-SQLAlchemy`, `requests`, `pytest`
2. define data model
	- `RegretEntry(id, decision_text, category, score, insight, amount, created_at)`
3. implement parsing and regret categories
	- daily spending (`$5 every day`, `daily coffee`)
	- subscription (`$50 monthly`)
	- trading loss (`bought ... sold ...`)
	- currency exchange (`converted USD to EUR`)
	- fallback one-time `purchase` pattern
4. add external data for realism
	- Frankfurter API for exchange rate in currency regret
5. compute regret score with 2+ factors
	- opportunity loss vs invested return
	- time horizon factor
	- recurring vs one-time, loss percentage
	- map score to labels (fine, mild regret, risky, high regret)
6. add routes
	- `/` home form
	- `/result` compute, store entry, show result
	- `/history` view saved entries
7. test
	- create DB in app context
	- confirm parser scenarios functions
	- run app with sample inputs

## Demo Plan

- Show UI with input prompt and sample questions from `regret.md`
- Demonstrate at least one category each:
  - daily coffee
  - monthly subscription
  - crypto loss
  - currency conversion
- Explain the formula and factors used
- Highlight history persistence and API usage

## Bonus

- Add better NLP parsing (numbers + dates + keywords)
- Add inflation API from World Bank (if time remains)
- Add unit tests for `parse_decision()` and `regret_score()`


