# DECISIONS

- Project title: `bit's today`
- The project is now Upbit-centered and altcoin-forward, not BTC-only
- Main cadence is now one autonomous strategy/improvement cycle every 6 hours
- The previous 30-minute lightweight execution model is deprecated
- The agent must maintain 5 preferred buy candidates at all times when data is available
- Preferred buy candidates should focus on Upbit-listed altcoins and exclude the top 4 largest Upbit majors
- Major coins may still be tracked as market context and risk barometers
- The strategy should be aggressive and diversified in paper trading, and should avoid defaulting to passive observation without a strong reason
- Candidate selection should compare turnover, momentum, community attention, news flow, and internal judgment
- Reports and dashboard output should become easier to scan, more visual, and more portal-like over time
- Each 6-hour cycle should include self-evaluation plus at least one concrete improvement to the strategy, report structure, or UI when feasible
- Real exchange execution remains out of scope for now
- External information gathering may use web search, web fetch, and local reasoning, but should stay selective rather than noisy
