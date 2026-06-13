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
- When fresh-breakout breadth disappears entirely (fresh breakouts = 0) and 3개 이상 current holdings are below roughly 50% of the day range or turn negative, force the next cycle to reset around the top positive leaderboard names and cap deployment around 65-70% until structure improves.
- When fresh-breakout breadth is zero and 3개 이상 current holdings fall below roughly 50% of the day range or hover near invalidation, force the next cycle to purge broken slots, allow at most 1 exhausted reclaim name, and cap deployment around 70% until cleaner survivors appear
- When major average range-position surges above roughly 80 and fresh breakouts are 4개 이상, force at least 3 of 5 preferred picks to come from 75%+ fresh/reclaimed leaders instead of defending older 40-60% continuations from the prior cycle.
- When major average range-position surges above roughly 80 and fresh breakouts expand to 5 or more, push paper deployment toward roughly 85% and force at least 4 of 5 preferred picks to come from 80%+ range-position leaders unless liquidity is clearly insufficient.
- When major average range-position jumps from below roughly 75 to above roughly 85 within one cycle and at least 5 non-major leaders hold 80%+ range-position with real turnover, force at least 2 of 5 preferred picks to upgrade from survivor anchors into faster beta continuation names instead of keeping the older defensive basket unchanged
- When a prior breadth-flip session cools quickly (major average falls back toward the 60s and fresh breakouts shrink to 1 or fewer), stop treating the old 90%+ basket as intact and rebuild around 1 fresh breakout plus 4 survivor/reclaim names.
- When major average range-position stays above roughly 80 but fresh breakouts contract to 2 or fewer, force out any held same-day leader with worse than roughly -8% day-high gap or below roughly 60% of the day range, even if its daily gain is still large; rotate into cleaner mega-reclaim or continuation names instead.
- When major average range-position cools from the low-80s/high-80s into roughly the high-60s while fresh breakouts fall to zero, keep the strongest mega-reclaim/core leader but force at least 1 weaker 55%-range large-cap continuation slot into a cleaner 60%+ relative-strength survivor instead of defending all 5 prior slots unchanged
- When one non-major leader accounts for more than roughly 60% of preferred-basket turnover, keep equal weighting and do not add concentration unless breadth remains extremely broad and at least four other preferred names still show real liquidity.
- When major average range-position falls below roughly 30 and 2개 이상 held preferred names break invalidation together, force those broken slots out next cycle and allow at most 1 sub-55 attention slot in the rebuilt basket.
- When major average range-position falls below roughly 20 and 60%+ range-position non-major leaders with at least roughly 30억원 turnover shrink to 3 or fewer, cap deployment around 70%, force at least 2 picks to come from those surviving green leaders, and allow at most 2 sub-55% rescue/reclaim slots.
- When breadth recovers but a same-day leader is still more than roughly 10% below its intraday high after a vertical surge, classify it as an exhausted blowoff and prefer cleaner 75%+ continuation/reclaim names instead of late chasing the spike
- When a former attention-trap leader reclaims roughly 85%+ of the day range with clear top-turnover leadership, allow re-entry even if headline overhang remains, but pair it with at least 2 cleaner non-attention slots so the basket does not overfit one narrative
- When major average range-position rebounds above roughly 70 and a former attention-trap leader reclaims 85%+ of the day range with clear top-turnover leadership, force at least 1 of 5 preferred picks into that mega-reclaim setup and do not keep 2 or more exhausted blowoff names with worse than roughly -10% day-high gap in the same basket
- When major average range-position falls below roughly 40 and a held same-day breakout is more than 12% below its intraday high or slips under roughly 55% of the day range, force that slot out next cycle instead of defending the earlier breakout headline alone
- When major average range-position falls below roughly 35 and a held liquid survivor slips under roughly 30% of the day range or turns negative, force that slot out next cycle and trim overall deployment by roughly 5-10% instead of defending it for past liquidity alone
- When top15 non-major positives shrink to 2 or fewer and major average range-position drops below roughly 10, keep 5 preferred candidates but cap actual portfolio deployment around 60% until breadth recovers
- When top15 non-major positives shrink to 3 or fewer and 3개 이상 held preferred names simultaneously turn negative or break invalidation, force the next cycle portfolio into all-positive candidates where possible and trim actual deployment toward roughly 70-75% instead of defending the broken basket
- When major average range-position rebounds above roughly 60 while 2개 이상 held preferred names are still below roughly 20% of the day range or more than 15% below the intraday high, force a full anti-trap rotation into cleaner 75%+ continuation/breakout names on the next cycle instead of defending the broken basket
- When a prior beta-upgrade cycle cools fast and major average range-position slips below roughly 65 while 2개 이상 held beta names fall below roughly 50% of the day range or turn negative, force those beta slots out next cycle and refill with 60%+ liquid survivors/reclaimed leaders plus at most 1 fresh breakout instead of defending the failed acceleration basket
- When major average range-position rebounds above roughly 60 but a top-turnover attention name stays negative and below roughly 30% of the day range, force it out next cycle and replace it with a positive 70%+ liquid survivor or breakout instead of defending raw turnover alone

- When a held top-turnover headline leader slips below roughly 40% of the day range while a positive 75%+ mega-reclaim or 85%+ continuation alternative with real liquidity is available, force the rotation next cycle instead of defending the older headline leader

- When major average range-position pushes above roughly 90 and fresh breakouts are 5개 이상, do not keep 70-80% continuation names if 90%+ alternatives with comparable real turnover exist; upgrade at least 2 of 5 slots into those fresher leaders instead of defending the older basket

## Dashboard direction
The dashboard should evolve toward a compact portal experience:
- icon-rich candidate list
- at-a-glance strategy state
- easy comparison of 5 preferred picks
- visible notes on what improved this cycle
- compact scorecard, risk-plan, and rotation-bucket visibility
