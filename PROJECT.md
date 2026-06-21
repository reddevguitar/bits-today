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
- When breadth stays strong and a held continuation slot cools toward roughly 55% of the day range while a higher-turnover 75%+ alternative is already leading, force the next cycle to promote the stronger name instead of defending the older basket out of inertia.
- When majors break down but 4개 이상 비메이저 알트가 75%+ range-position과 실거래대금을 동시에 유지하면, 50% 미만으로 내려온 대형 품질 코어를 고집하지 말고 독립 강세 생존주로 교체한다.
- When a held preferred alt collapses below roughly 20% of the day range while losing positive momentum, force a full anti-trap rotation next cycle instead of defending it for turnover alone
- When breadth stays weak, do not keep a merely narrative rebound slot around 50% of the day range if a 70%+ structured alternative with real turnover exists; rotate into the cleaner structure.
- When fresh-breakout breadth disappears (fresh breakouts near zero) but relative-strength survivors remain active, force at least 3 of 5 preferred picks to come from survivor/reclaim groups and avoid sub-55% range-position laggards unless a clearly stronger turnover catalyst exists.
- When fresh-breakout breadth disappears entirely (fresh breakouts = 0) and 3개 이상 current holdings are below roughly 50% of the day range or turn negative, force the next cycle to reset around the top positive leaderboard names and cap deployment around 65-70% until structure improves.
- When fresh breakouts disappear (fresh = 0) while 4개 이상 current holdings re-break invalidation in the very next cycle, force a 60-65% rebuild around exactly 1 highest-range fresh/near-fresh name if available, at least 2 liquid 60%+ survivors, and at most 1 attention-recovery slot instead of retrying the failed basket.
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
- When major average range-position collapses into the teens and fresh breakouts are zero while 2개 이상 held preferred names break invalidation or lose upper-range structure, force the next cycle to purge those broken slots, rebuild around 65-75% positive survivor/reclaim names, and cap deployment around 75% until majors recover.
- When breadth recovers but a same-day leader is still more than roughly 10% below its intraday high after a vertical surge, classify it as an exhausted blowoff and prefer cleaner 75%+ continuation/reclaim names instead of late chasing the spike
- When a former attention-trap leader reclaims roughly 85%+ of the day range with clear top-turnover leadership, allow re-entry even if headline overhang remains, but pair it with at least 2 cleaner non-attention slots so the basket does not overfit one narrative
- When major average range-position rebounds above roughly 70 and a former attention-trap leader reclaims 85%+ of the day range with clear top-turnover leadership, force at least 1 of 5 preferred picks into that mega-reclaim setup and do not keep 2 or more exhausted blowoff names with worse than roughly -10% day-high gap in the same basket
- When major average range-position falls below roughly 40 and a held same-day breakout is more than 12% below its intraday high or slips under roughly 55% of the day range, force that slot out next cycle instead of defending the earlier breakout headline alone
- When fresh breakouts are zero and one of the held names actually breaks invalidation while a positive 75%+ range-position alternative with cleaner day-high gap exists, force the next cycle to rotate into the cleaner structure instead of defending turnover alone
- When major average range-position falls below roughly 35 and a held liquid survivor slips under roughly 30% of the day range or turns negative, force that slot out next cycle and trim overall deployment by roughly 5-10% instead of defending it for past liquidity alone
- When top15 non-major positives shrink to 2 or fewer and major average range-position drops below roughly 10, keep 5 preferred candidates but cap actual portfolio deployment around 60% until breadth recovers
- When top15 non-major positives shrink to 3 or fewer and 3개 이상 held preferred names simultaneously turn negative or break invalidation, force the next cycle portfolio into all-positive candidates where possible and trim actual deployment toward roughly 70-75% instead of defending the broken basket
- When major average range-position rebounds above roughly 60 while 2개 이상 held preferred names are still below roughly 20% of the day range or more than 15% below the intraday high, force a full anti-trap rotation into cleaner 75%+ continuation/breakout names on the next cycle instead of defending the broken basket
- When a prior beta-upgrade cycle cools fast and major average range-position slips below roughly 65 while 2개 이상 held beta names fall below roughly 50% of the day range or turn negative, force those beta slots out next cycle and refill with 60%+ liquid survivors/reclaimed leaders plus at most 1 fresh breakout instead of defending the failed acceleration basket
- When 2개 이상 held preferred names fall into turnover-trap territory (top-turnover but roughly sub-25% day-range or clear negative drift) and fresh breakouts recover to 2 or more, force those broken slots into the fresh/high-range alternatives next cycle instead of defending the prior basket just because it is recent
- When major average range-position rebounds above roughly 60 but a top-turnover attention name stays negative and below roughly 30% of the day range, force it out next cycle and replace it with a positive 70%+ liquid survivor or breakout instead of defending raw turnover alone

- When a held top-turnover headline leader slips below roughly 40% of the day range while a positive 75%+ mega-reclaim or 85%+ continuation alternative with real liquidity is available, force the rotation next cycle instead of defending the older headline leader

- When major average range-position pushes above roughly 90 and fresh breakouts are 5개 이상, do not keep 70-80% continuation names if 90%+ alternatives with comparable real turnover exist; upgrade at least 2 of 5 slots into those fresher leaders instead of defending the older basket

- When major average range-position falls below roughly 10 and 4개 이상 held preferred names simultaneously break invalidation or slip below roughly 35% of the day range, force a full reset into exactly 1 fresh breakout leader plus the remaining positive survivor/secondary-continuation names, and cap deployment around 70% until major average range-position recovers above roughly 20.
- When breadth rebounds sharply from a fresh-breakout drought (for example fresh breakouts rise from 0-1 to 2+ and top15 low-range count improves by 5 or more) while major average range-position is still below roughly 30, allow up to 2 former broken leaders back into the basket only if each reclaims 70%+ of the day range with better than roughly -3% day-high gap, and keep at least 1 non-recycled survivor/quality slot so the rebound basket does not overfit yesterday's failures.
- When major average range-position rebounds above roughly 45 but 2개 이상 held reclaim/beta names simultaneously fall below roughly 30% of the day range or worse than roughly -8% day-high gap, force those broken slots out next cycle and rebuild around fresh 85%+ leaders plus clean 75%+ liquid continuations instead of giving the rebound basket another chance

- When majors all reclaim roughly 85%+ of the day range together and 2개 이상 held small-cap breakouts slip below roughly 50% of the day range, force the next cycle to replace those fading slots with larger-liquidity 75%+ continuation leaders instead of defending the earlier spike basket

- When major average range-position stays above roughly 80, top15 non-major positives are 10개 이상, and fresh breakouts fall to 0, keep deployment around 90% and allow 60-80% range-position mega/liquid continuation leaders to remain in the basket; however cap every position at equal weight and require at least 3 of 5 picks to come from multi-10B KRW liquidity names instead of overreacting to the fresh-count drop alone.
- When major average range-position collapses by roughly 50 points or more within one cycle and 3개 이상 held preferred names simultaneously break invalidation or lose roughly 45% day-range structure, cut next-cycle deployment toward roughly 70%, force at least 2 picks into 90%+ fresh/high-range leaders, keep 1 large-cap survivor, and allow at most 1 sub-55 mega-turnover salvage slot instead of defending the old 90% basket.
- When a same-day fresh breakout held in the portfolio collapses to roughly 15% or less of the day range and worse than roughly -12% day-high gap by the next cycle, force that slot out immediately and replace it with an 80%+ liquid reclaim/continuation leader instead of giving the failed breakout another chance.
- When a held fresh-breakout name collapses below roughly 35% of the day range within one cycle and there are 3 or more positive 80%+ range-position alternatives with real liquidity, force that failed breakout out next cycle instead of giving it another chance

- When major average range-position drops by roughly 20 points or more within one cycle and 2개 이상 held preferred names slip below roughly 30% of the day range or worse than roughly -8% day-high gap, force the next cycle to keep at least 1 mega-turnover core but rebuild the remaining 4 slots around 85%+ fresh/high-range names where possible, and trim deployment toward roughly 75% instead of defending the older basket.

- When major average range-position falls by roughly 30 points or more within one cycle and 2개 이상 held preferred names break invalidation together, force an immediate reset around exactly 1 fresh breakout plus all-positive survivors/continuations, and cap deployment around 70% instead of defending broken leaders.

- When major average range-position rebounds above roughly 45 while fresh breakouts are still 0, force at least 2 of 5 preferred picks into 75%+ clean continuation names and reject same-day leaders with worse than roughly -8% day-high gap even if they remain top-turnover; this prevents chasing exhausted rebound headlines during partial breadth recovery.
- When a 90%-deployed breadth-reclaim basket is followed by a next-cycle major-average collapse below roughly 20 and 2개 이상 held names slip below roughly 30% of the day range, force an immediate reset toward roughly 70%, keep only 1 mega-turnover salvage core, and refill the remaining slots with cleaner positive survivors/continuations instead of defending the prior 90% basket.
- When weak_breadth_warning flips true at the same time major average range-position drops by roughly 30 points or more and 2개 이상 held names break invalidation, cap the next cycle around 75%, keep exactly 1 90%+ fresh/mega leader, and rebuild the other 4 slots from all-positive continuation/survivor names instead of retrying the failed acceleration basket.

- When major average range-position rebounds above roughly 60 while a held mega-turnover salvage core remains negative and below roughly 35% of the day range, force that salvage slot out next cycle and rotate into a positive 80%+ leader with real turnover instead of defending old liquidity.

- When top15 non-major positives shrink to 3 or fewer while 3개 이상 current holdings simultaneously sit below roughly 30% of the day range, force the next cycle to rebuild around 5 all-positive names where possible, cap deployment around 70%, and prefer cleaner mid-turnover survivors over larger turnover traps.

- When major average range-position rebounds above roughly 80 within one cycle while 2개 이상 held survivor names are still below roughly 45% of the day range, and at least 1 non-major leader is printing a 90%+ upper-range breakout with real multi-5B KRW turnover, force the next cycle to raise deployment toward roughly 90%, keep at least 1 mega-liquidity reclaim slot, and replace those stale survivors instead of leaving the older 70% defensive basket intact.

- When 2개 이상 current holdings collapse to roughly 20% or less of the day range but breadth improves enough to clear the weak_breadth_warning flag, force the next cycle to abandon those broken survivors and rebuild around 5 all-positive candidates instead of defending the older basket.

## Dashboard direction
The dashboard should evolve toward a compact portal experience:
- icon-rich candidate list
- at-a-glance strategy state
- easy comparison of 5 preferred picks
- visible notes on what improved this cycle
- compact scorecard, risk-plan, and rotation-bucket visibility
- When a breadth-surge basket cools within one cycle (major average range-position drops by roughly 20 points or more and fresh breakouts shrink to 1 or fewer), force at least 3 of 5 preferred picks into 70%+ continuation/survivor names and remove faded attention/beta leaders with roughly -7% or worse day-high gaps instead of defending the prior surge basket
- When major average range-position falls below roughly 25 and 3개 이상 held preferred names simultaneously slip below roughly 35% of the day range or break invalidation, force the next cycle to reset around exactly 1 fresh 85%+ leader plus 4 stronger 60%+ continuation/survivor names, and cap deployment around 75% instead of defending the broken basket.

- When major average range-position rebounds from roughly the teens into the 30s within one cycle but fresh breakouts stay at 0, force the next cycle to replace sub-40% stalled survivors with at least 2 clean 75%+ continuation names, 2 liquid 50%+ survivors/reclaims, and at most 1 mid-cap beta slot instead of defending the earlier defensive reset.

- When major average range-position rebounds above roughly 60 and at least 3 non-major alts simultaneously hold 80%+ of the day range with real multi-10B KRW turnover, force at least 2 of 5 preferred picks into those mega-liquidity reclaim leaders and allow paper deployment toward roughly 90% instead of staying stuck in the prior 70-80% survivor basket.

- When major average range-position cools into roughly 60-75 after a prior breadth surge but 4개 이상 비메이저 알트가 여전히 70%+ range-position과 실거래대금을 유지하면, 45% 미만으로 식은 기존 보유 슬롯을 방치하지 말고 상단 continuation/reclaim 군으로 즉시 교체하며 paper deployment는 대체로 85-90%를 유지한다.
- When fresh breakouts fall to 0 and a held fresh-breakout name is sitting at or below its invalidation level while 2개 이상 80%+ liquid continuation leaders exist, force that failed fresh slot out next cycle and promote the cleaner continuation names instead of defending the old listing momentum.
- When a former mega-turnover core stays positive but slips below roughly 30% of the day range while major average range-position is below roughly 50 and at least two cleaner 70%+ non-major continuation names with real 10B+ KRW turnover exist, force that stalled core out next cycle instead of anchoring on size alone.
- When community/attention data shows an extreme sell-pressure warning and the same name also trades with roughly -7% or worse day-high gap, reject it from preferred buys until it reclaims about 70%+ of the day range.

- When fresh breakouts stay at 0 but a mega-liquidity attention alt reclaims roughly 70%+ of the day range with a cleaner day-high gap than held 40-50% basket names, force at least 1 of 5 preferred picks into that survivor and evict the weaker faded headline/breakout slot instead of defending the older basket.
