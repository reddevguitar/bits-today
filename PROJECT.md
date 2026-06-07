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
- Exclude the top 4 largest Upbit majors from alt candidate picks
- Major coins may still be tracked as market context and risk barometers
- Use community/news/search inputs when they materially help
- Prefer fresh, comparative judgment over static watchlists
- When top-turnover leaders look trap-like, widen the scan to second-tier high-range breakouts instead of anchoring on size alone
- A former turnover-trap name may re-enter only after reclaiming clear upper-range structure (roughly 60-65%+ of the day range) with positive momentum
- On breadth-flip sessions where majors sharply recover and top-turnover breadth re-expands, allow fast re-entry of former trap names only if they hold roughly 80%+ range-position with real turnover
- Prefer 65%+ range-position for core picks unless a recent listing or explicit event explains a slightly lower reading
- When top-turnover breadth weakens and many leaders sink below mid-range, shift from raw gainers to liquid relative-strength survivors (roughly 55%+ range-position with real turnover) instead of chasing exhausted spikes
- When majors collapse into single-digit range-position, allow a few 45-60% quality survivors with clean gap/turnover to fill the last slots rather than forcing late parabolic chases
- When former turnover-trap names reclaim, allow at most 2 of 5 preferred picks to come from that bucket unless major average range-position is above roughly 55 and breadth is clearly expanding; this prevents over-chasing one rebound narrative.
- When majors stay weak but fresh-breakout breadth is clearly active (for example multiple 90%+ range-position alts with real turnover), permit a faster rotation back into breakout leaders instead of over-defending older survivors.
- When breadth stays strong but one of the held high-beta slots turns negative or slips below stronger 80%+ range-position alternatives, replace it in the next cycle instead of defending stale laggards.
- When majors break down but 4개 이상 비메이저 알트가 75%+ range-position과 실거래대금을 동시에 유지하면, 50% 미만으로 내려온 대형 품질 코어를 고집하지 말고 독립 강세 생존주로 교체한다.
- When a held preferred alt collapses below roughly 20% of the day range while losing positive momentum, force a full anti-trap rotation next cycle instead of defending it for turnover alone
- When breadth stays weak, do not keep a merely narrative rebound slot around 50% of the day range if a 70%+ structured alternative with real turnover exists; rotate into the cleaner structure.
- When fresh-breakout breadth disappears (fresh breakouts near zero) but relative-strength survivors remain active, force at least 3 of 5 preferred picks to come from survivor/reclaim groups and avoid sub-55% range-position laggards unless a clearly stronger turnover catalyst exists.
- When major average range-position surges above roughly 80 and fresh breakouts are 4개 이상, force at least 3 of 5 preferred picks to come from 75%+ fresh/reclaimed leaders instead of defending older 40-60% continuations from the prior cycle.

## Dashboard direction
The dashboard should evolve toward a compact portal experience:
- icon-rich candidate list
- at-a-glance strategy state
- easy comparison of 5 preferred picks
- visible notes on what improved this cycle
- compact scorecard, risk-plan, and rotation-bucket visibility
