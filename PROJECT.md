# bit's today

## Goal
Build an aggressive Upbit-centered crypto decision-support and paper-trading agent.

## What it does
Every 6 hours, the agent runs a full strategy cycle:
- scans Upbit market leaders and fast-moving altcoins
- excludes the top 4 largest Upbit majors from alt-pick selection
- compares candidate coins using price action, turnover, news, community attention, and internal judgment
- maintains a constantly refreshed list of 5 preferred buy candidates
- assigns candidate roles, paper allocations, and invalidation triggers
- updates a paper portfolio with active, diversified, aggressive positioning
- writes a concise Korean report and upgrades the dashboard/UI when useful

## Important boundary
This is still decision support plus paper trading.
Actual exchange execution remains manual. The agent may simulate trades in a virtual portfolio, but must not place real trades.

## Virtual portfolio
- Starting capital: 10,000,000 KRW
- The agent updates a paper portfolio whenever a new 6-hour cycle is generated
- Each report must include simulated action and portfolio status
- The strategy should avoid passive all-cash behavior unless the market is clearly broken

## Cadence
- Single major strategy cycle every 6 hours
- Save each report to `reports/`
- Each cycle should also propose and apply at least one improvement to analysis quality, selection logic, dashboard clarity, or presentation when feasible

## Output priorities
1. Convenient, easy-to-scan new information
2. Simple strategy and direction updates
3. Aggressive and diversified investing, not passive waiting
4. Continuous learning from market data, news, search, and community flow
5. Honest self-evaluation and continuous program improvement

## Core selection rules
- Always maintain 5 preferred buy candidates
- Focus on Upbit-listed altcoins
- Exclude the top 4 largest Upbit majors from the preferred alt-buy list
- Keep majors visible as reference signals, but not as alt picks
- Use community/news/search inputs when they materially help
- Prefer fresh, comparative judgment over static watchlists
- When top-turnover leaders look trap-like, widen the scan to second-tier high-range breakouts instead of anchoring on size alone
- A former turnover-trap name may re-enter only after reclaiming clear upper-range structure (roughly 60-65%+ of the day range) with positive momentum
- Prefer 65%+ range-position for core picks unless a recent listing or explicit event explains a slightly lower reading
- When top-turnover breadth weakens and many leaders sink below mid-range, shift from raw gainers to liquid relative-strength survivors (roughly 55%+ range-position with real turnover) instead of chasing exhausted spikes
- When majors collapse into single-digit range-position, allow a few 45-60% quality survivors with clean gap/turnover to fill the last slots rather than forcing late parabolic chases
- When majors stay weak but fresh-breakout breadth is clearly active (for example multiple 90%+ range-position alts with real turnover), permit a faster rotation back into breakout leaders instead of over-defending older survivors.

## Dashboard direction
The dashboard should evolve toward a compact portal experience:
- icon-rich candidate list
- at-a-glance strategy state
- easy comparison of 5 preferred picks
- visible notes on what improved this cycle
- compact scorecard, risk-plan, and rotation-bucket visibility

