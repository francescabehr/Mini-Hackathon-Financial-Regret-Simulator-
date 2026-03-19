# ECO5040S - Mini-Hackathon | Financial Regret Simulator 😬 

## Overview

Many financial decisions seem small at the time: buying coffee, purchasing gadgets, or subscribing to services.
However, these decisions can have **hidden long-term consequences**.

In this mini-hackathon, you will build a **Flask web application** that reveals the potential **regret** associated with a financial decision.

Your goal is to help users answer:
> "What might I regret about this purchase later?"

Your application should transform a simple financial input into a **surprising** financial insight.

## Your Task

Build a **Flask web application** that:
1. Accepts a **financial decision** from the user (e.g., "I bought a $5 coffee every day").
2. Calculates an **alternative outcome or hidden cost**
3. Generates a **Financial Regret Score** (0-100).

### Example

Input:
- "Purchase: R1200 headphones"
- "Monthly Subscription: R50 for 12 months"
- "Daily Coffee: R30 every day for a year"
- "Bought BTC at R100,000 and sold at R50,000"
- "Converted R10,000 to USD in 2020 and back in 2024"

Output Insight:
- What that money could have become if invested
- The long-term cost of a recurring expense (e.g., subscription)
- The inflation-adjusted value of the money
- Risk exposure if invested in volatile assets
- Currency loss due to exchange rates


## Regret Categories
Each team must pick **one category of regret** to focus on:

### Opportunity Cost Regret
- What could have been earned if the money was invested instead?
- Crypto Alternative, Stock Market Investment, Compound Interest

### Time Regret
- How does this cost grow over time?
- Subscription traps, daily spending accumulation, long-term habit cost

### Inflation Regret
- How much purchasing power is lost due to inflation?
- Inflation-adjusted value of money, future cost of current purchases


### Volatility Regret
- What is the risk hidden in this financial decision?
- Crypto volatility, stock market risk, currency exchange risk


### Global Regret
- How does this financial decision compare globally?
- Currency loss, global cost comparison, international purchasing power

## Financial Behaviour Regret
- What does this purchase say about your financial habits?
- Impulse purchase detector, luxury vs necessity analysis, financial health score


## Required Feature: Financial Regret Score
- A score from 0 to 100 that quantifies the level of regret associated with the financial decision.

> 0 = No regret, 100 = Maximum regret

| Score  | Meaning        |
| ------ | -------------- |
| 0–20   | Probably fine  |
| 20–50  | Mild regret    |
| 50–80  | Risky decision |
| 80–100 | High regret    |

Your score must be calculated using **at least TWO factors** relevant to the chosen regret category.

Example (Daily Coffee Regret):

```
Regret Score = (Annual Cost of Coffee / Average Annual Investment Return) * (1 + Inflation Rate)
```

You must design your **own formula**. Be creative and justify your choice of factors.


## Technical Requirements
Your project must include/use:

- **Flask**: For building the web application (At least two routes, e.g., home and result)
- **HTML/CSS**: For the user interface (Jinja2 templates for dynamic content)
- **SQLAlchemy + SQLite**: Store at least one piece of data (e.g., user inputs, calculated regret scores)
- **External API**: Use at least one external API to fetch relevant financial data (e.g., stock prices, inflation rates, exchange rates)
- **GitHub Repository**: Host your code on GitHub with a clear README and commit history

## "Judging Criteria"

| Category                 | Description                                |
| ------------------------ | ------------------------------------------ |
| Functionality            | App works and produces results             |
| Technical Implementation | Flask, API, and database used              |
| Financial Insight        | Does the app reveal something interesting? |
| Creativity               | Is the idea unique or surprising?          |
| Demo                     | Clear explanation and demonstration        |


## Demo Rules
- Each team will have 5 minutes to present their application.
- Start your demo with a question: "Should you buy coffee or invest that money?", "How expensive is that subscription really?", "What is the hidden cost of that purchase?"
- Show the input, insight and the regret score.

## API Suggestions
These are some great APIs that don't need you to sign up for an API key:

- [Frankfurter API](https://frankfurter.dev/) - Currency exchange rates
- [CoinGecko API](https://www.coingecko.com/en/api) - Cryptocurrency prices
- [Alpha Vantage API](https://www.alphavantage.co/) - Stock market
- [World Bank API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview) - Economic indicators (Inflation, GDP, etc.)
