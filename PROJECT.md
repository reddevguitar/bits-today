# bit's today

## Goal
Build a simple Bitcoin monitoring and decision-support agent.

## What it does
Every 2 hours, the agent checks:
- Bitcoin price status and recent movement
- Major Bitcoin-related news
- Market chart context / trend clues
- Notable public-figure investment news when relevant
  - Example: Trump family / Trump-linked crypto or Bitcoin investment news
  - Skip this section when there is no meaningful fresh news

Then it produces:
- a short market summary
- a tentative investment judgment
- a confidence note
- clear reasons

## Important boundary
This is decision support plus paper trading.
Actual exchange execution remains manual. The agent may simulate trades in a virtual portfolio, but must not place real trades.

## Virtual portfolio
- Starting capital: 10,000,000 KRW
- The agent updates a paper portfolio whenever a new report is generated
- Each report must include the simulated action and portfolio status

## Cadence
- Run every 2 hours
- Save each report to `reports/`

## First version output format
Each run should produce:
1. Timestamp
2. BTC price snapshot
3. Trend summary
4. News summary
5. Notable investor / public figure note if any
6. Judgment: bullish / bearish / neutral
7. Confidence: low / medium / high
8. Reasoning bullets
9. Suggested action: buy small / hold / wait / reduce risk
10. Virtual trade action
11. Portfolio snapshot

## Next steps
- Create reporting prompt / workflow
- Set up recurring 2-hour job
- Decide data sources
- Add simple scoring logic
- Track paper portfolio performance over time
