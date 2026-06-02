#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOT_PATH = Path('/Users/reddevguitar/.openclaw/workspace/bits-today/data/upbit_snapshot.json')

BASE = Path('/Users/reddevguitar/.openclaw/workspace/bits-today')
OUT = BASE / 'data'
OUT.mkdir(exist_ok=True)

TOP4_MAJORS = {'BTC', 'ETH', 'XRP', 'SOL'}
STABLES = {'USDT', 'USDC', 'USDS', 'USDE', 'USD1'}
HIGH_CONVICTION_MIN_TURNOVER = 5_000_000_000
TURNOVER_TRAP_MIN_TURNOVER = 8_000_000_000
TURNOVER_TRAP_MAX_RANGE_POSITION = 35
RESILIENT_POSITIVE_MIN_TURNOVER = 6_000_000_000
RESILIENT_POSITIVE_MIN_RANGE_POSITION = 55
QUALITY_RECOVERY_MIN_TURNOVER = 3_000_000_000
QUALITY_RECOVERY_MIN_RANGE_POSITION = 45
CONTINUATION_MIN_TURNOVER = 8_000_000_000
CONTINUATION_MIN_RANGE_POSITION = 60
CONTINUATION_MAX_DAY_HIGH_GAP = -5
FADING_LEADER_MIN_TURNOVER = 10_000_000_000
FADING_LEADER_MAX_RANGE_POSITION = 55
FADING_LEADER_MAX_DAY_HIGH_GAP = -7
RECLAIMED_LEADER_MIN_TURNOVER = 15_000_000_000
RECLAIMED_LEADER_MIN_RANGE_POSITION = 55
RECLAIMED_LEADER_MAX_RANGE_POSITION = 65
RECLAIMED_LEADER_MAX_DAY_HIGH_GAP = -4.5
FRESH_BREAKOUT_MIN_TURNOVER = 8_000_000_000
FRESH_BREAKOUT_MIN_RANGE_POSITION = 90
FRESH_BREAKOUT_MAX_DAY_HIGH_GAP = -3.5
STALLED_POSITIVE_LIQUIDITY_MIN_TURNOVER = 12_000_000_000
STALLED_POSITIVE_LIQUIDITY_MAX_RANGE_POSITION = 50
STALLED_POSITIVE_LIQUIDITY_MAX_DAY_HIGH_GAP = -1
EXHAUSTED_BLOWOFF_MIN_TURNOVER = 20_000_000_000
EXHAUSTED_BLOWOFF_MIN_CHANGE_PCT = 8
EXHAUSTED_BLOWOFF_MAX_DAY_HIGH_GAP = -10
EXHAUSTED_BLOWOFF_MIN_RANGE_POSITION = 50
STABILITY_SUPPORT_MIN_TURNOVER = 3_000_000_000
STABILITY_SUPPORT_MIN_RANGE_POSITION = 60
STABILITY_SUPPORT_MAX_DAY_HIGH_GAP = -4
SECONDARY_CONTINUATION_MIN_TURNOVER = 2_000_000_000
SECONDARY_CONTINUATION_MIN_RANGE_POSITION = 70
SECONDARY_CONTINUATION_MAX_DAY_HIGH_GAP = -5
QUALITY_SURVIVOR_MIN_TURNOVER = 5_000_000_000
QUALITY_SURVIVOR_MIN_RANGE_POSITION = 45
QUALITY_SURVIVOR_MAX_DAY_HIGH_GAP = -6
MEGA_RECLAIM_MIN_TURNOVER = 100_000_000_000
MEGA_RECLAIM_MIN_RANGE_POSITION = 65
MEGA_RECLAIM_MAX_DAY_HIGH_GAP = -8
LIQUID_SELECTION_MIN_TURNOVER = 2_000_000_000
RELATIVE_STRENGTH_RECLAIM_MIN_TURNOVER = 4_000_000_000
RELATIVE_STRENGTH_RECLAIM_MIN_RANGE_POSITION = 60
RELATIVE_STRENGTH_RECLAIM_MAX_DAY_HIGH_GAP = -3.5
RELATIVE_STRENGTH_RECLAIM_MIN_CHANGE_PCT = -2


def get_json(url: str):
    req = urllib.request.Request(url, headers={'User-Agent': 'bits-today/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


markets = get_json('https://api.upbit.com/v1/market/all?is_details=false')
krw = [m for m in markets if m['market'].startswith('KRW-')]
krw_map = {m['market']: m for m in krw}
market_codes = [m['market'] for m in krw]

all_tickers = []
for i in range(0, len(market_codes), 80):
    chunk = market_codes[i:i + 80]
    all_tickers.extend(get_json('https://api.upbit.com/v1/ticker?markets=' + ','.join(chunk)))

rows = []
for t in all_tickers:
    market = t['market']
    symbol = market.split('-')[1]
    high = t.get('high_price') or 0
    low = t.get('low_price') or 0
    price = t.get('trade_price') or 0
    range_position_pct = None
    if high > low:
        range_position_pct = round(((price - low) / (high - low)) * 100, 1)
    day_high_gap_pct = None
    if high:
        day_high_gap_pct = round(((price - high) / high) * 100, 2)
    rows.append({
        'market': market,
        'symbol': symbol,
        'korean_name': krw_map[market]['korean_name'],
        'english_name': krw_map[market]['english_name'],
        'price_krw': price,
        'change_pct_24h': round((t.get('signed_change_rate') or 0) * 100, 8),
        'turnover_krw_24h': t.get('acc_trade_price_24h') or 0,
        'opening_price': t.get('opening_price'),
        'high_price': high,
        'low_price': low,
        'range_position_pct': range_position_pct,
        'day_high_gap_pct': day_high_gap_pct,
    })

rows.sort(key=lambda x: x['turnover_krw_24h'], reverse=True)

def selection_score(row, max_turnover):
    turnover = row.get('turnover_krw_24h') or 0
    turnover_score = (turnover / max_turnover) * 35 if max_turnover else 0
    change_pct = row.get('change_pct_24h') or 0
    momentum_score = min(max(change_pct, -8), 18) * 1.6
    range_position = row.get('range_position_pct') if row.get('range_position_pct') is not None else 0
    range_score = range_position * 0.35
    gap = row.get('day_high_gap_pct') if row.get('day_high_gap_pct') is not None else -10
    gap_score = max(-10, 6 + gap * 1.5)
    penalty = 0
    if change_pct < 0:
        penalty += min(18, abs(change_pct) * 2.2)
    if range_position < 35:
        penalty += (35 - range_position) * 0.35
    return round(turnover_score + momentum_score + range_score + gap_score - penalty, 2)

max_turnover = max((r['turnover_krw_24h'] for r in rows), default=0)
for row in rows:
    row['selection_score'] = selection_score(row, max_turnover)

majors = [r for r in rows if r['symbol'] in TOP4_MAJORS]
major_range_positions = [r['range_position_pct'] for r in majors if r.get('range_position_pct') is not None]
major_health = {
    'major_avg_range_position_pct': round(sum(major_range_positions) / len(major_range_positions), 2) if major_range_positions else 0,
    'major_positive_count': sum(1 for r in majors if r['change_pct_24h'] > 0),
    'major_negative_count': sum(1 for r in majors if r['change_pct_24h'] < 0),
}
leaders = [r for r in rows if r['symbol'] not in TOP4_MAJORS and r['symbol'] not in STABLES]
positive = [r for r in leaders if r['change_pct_24h'] > 0]
high_conviction_positive = [
    r for r in positive
    if (r['range_position_pct'] is not None and r['range_position_pct'] >= 70)
    and r['turnover_krw_24h'] >= HIGH_CONVICTION_MIN_TURNOVER
]
resilient_positive = [
    r for r in positive
    if (r['range_position_pct'] is not None and r['range_position_pct'] >= RESILIENT_POSITIVE_MIN_RANGE_POSITION)
    and r['turnover_krw_24h'] >= RESILIENT_POSITIVE_MIN_TURNOVER
]
quality_recovery = [
    r for r in positive
    if (r['range_position_pct'] is not None and r['range_position_pct'] >= QUALITY_RECOVERY_MIN_RANGE_POSITION)
    and r['turnover_krw_24h'] >= QUALITY_RECOVERY_MIN_TURNOVER
]
continuation_positive = [
    r for r in positive
    if (r['range_position_pct'] is not None and r['range_position_pct'] >= CONTINUATION_MIN_RANGE_POSITION)
    and r['turnover_krw_24h'] >= CONTINUATION_MIN_TURNOVER
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= CONTINUATION_MAX_DAY_HIGH_GAP)
]
turnover_traps = [
    r for r in leaders
    if r['turnover_krw_24h'] >= TURNOVER_TRAP_MIN_TURNOVER
    and r['change_pct_24h'] < 0
    and (r['range_position_pct'] is not None and r['range_position_pct'] <= TURNOVER_TRAP_MAX_RANGE_POSITION)
]
fading_positive_leaders = [
    r for r in positive
    if r['turnover_krw_24h'] >= FADING_LEADER_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] <= FADING_LEADER_MAX_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] <= FADING_LEADER_MAX_DAY_HIGH_GAP)
]
reclaimed_positive_leaders = [
    r for r in positive
    if r['turnover_krw_24h'] >= RECLAIMED_LEADER_MIN_TURNOVER
    and (r['range_position_pct'] is not None and RECLAIMED_LEADER_MIN_RANGE_POSITION <= r['range_position_pct'] <= RECLAIMED_LEADER_MAX_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= RECLAIMED_LEADER_MAX_DAY_HIGH_GAP)
]
fresh_breakout_positive_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= FRESH_BREAKOUT_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= FRESH_BREAKOUT_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= FRESH_BREAKOUT_MAX_DAY_HIGH_GAP)
]
stalled_positive_liquidity_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= STALLED_POSITIVE_LIQUIDITY_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] <= STALLED_POSITIVE_LIQUIDITY_MAX_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] <= STALLED_POSITIVE_LIQUIDITY_MAX_DAY_HIGH_GAP)
]
exhausted_blowoff_positive_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= EXHAUSTED_BLOWOFF_MIN_TURNOVER
    and r['change_pct_24h'] >= EXHAUSTED_BLOWOFF_MIN_CHANGE_PCT
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= EXHAUSTED_BLOWOFF_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] <= EXHAUSTED_BLOWOFF_MAX_DAY_HIGH_GAP)
]
stability_support_alts = [
    r for r in leaders
    if r['turnover_krw_24h'] >= STABILITY_SUPPORT_MIN_TURNOVER
    and r['change_pct_24h'] >= 0
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= STABILITY_SUPPORT_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= STABILITY_SUPPORT_MAX_DAY_HIGH_GAP)
]
secondary_continuation_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= SECONDARY_CONTINUATION_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= SECONDARY_CONTINUATION_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= SECONDARY_CONTINUATION_MAX_DAY_HIGH_GAP)
]

quality_survivor_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= QUALITY_SURVIVOR_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= QUALITY_SURVIVOR_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= QUALITY_SURVIVOR_MAX_DAY_HIGH_GAP)
]

mega_reclaim_alts = [
    r for r in positive
    if r['turnover_krw_24h'] >= MEGA_RECLAIM_MIN_TURNOVER
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= MEGA_RECLAIM_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= MEGA_RECLAIM_MAX_DAY_HIGH_GAP)
]

relative_strength_reclaim_alts = [
    r for r in leaders
    if r['turnover_krw_24h'] >= RELATIVE_STRENGTH_RECLAIM_MIN_TURNOVER
    and r['change_pct_24h'] >= RELATIVE_STRENGTH_RECLAIM_MIN_CHANGE_PCT
    and (r['range_position_pct'] is not None and r['range_position_pct'] >= RELATIVE_STRENGTH_RECLAIM_MIN_RANGE_POSITION)
    and (r['day_high_gap_pct'] is not None and r['day_high_gap_pct'] >= RELATIVE_STRENGTH_RECLAIM_MAX_DAY_HIGH_GAP)
]

top15_alt_leaders = leaders[:15]
top15_alt_positive_count = sum(1 for r in top15_alt_leaders if r['change_pct_24h'] > 0)
top15_alt_low_range_count = sum(1 for r in top15_alt_leaders if (r['range_position_pct'] is not None and r['range_position_pct'] <= 35))
leadership_health = {
    'top15_alt_positive_count': top15_alt_positive_count,
    'top15_alt_positive_ratio_pct': round((top15_alt_positive_count / len(top15_alt_leaders)) * 100, 2) if top15_alt_leaders else 0,
    'top15_alt_low_range_count': top15_alt_low_range_count,
    'top15_alt_low_range_ratio_pct': round((top15_alt_low_range_count / len(top15_alt_leaders)) * 100, 2) if top15_alt_leaders else 0,
    'weak_breadth_warning': top15_alt_positive_count <= 3 or top15_alt_low_range_count >= 8
}
breakout_breadth = {
    'fresh_breakout_count': len(fresh_breakout_positive_alts),
    'high_conviction_count': len(high_conviction_positive),
    'quality_survivor_count': len(quality_survivor_alts),
    'relative_strength_reclaim_count': len(relative_strength_reclaim_alts),
    'breakout_cluster_active': len(fresh_breakout_positive_alts) >= 4 or len(high_conviction_positive) >= 6,
    'summary': (
        f"fresh {len(fresh_breakout_positive_alts)} / conviction {len(high_conviction_positive)} / "
        f"survivor {len(quality_survivor_alts)} / reclaim {len(relative_strength_reclaim_alts)}"
    )
}

liquid_leaders = [r for r in leaders if r['turnover_krw_24h'] >= LIQUID_SELECTION_MIN_TURNOVER]
selection_leaderboard = sorted(liquid_leaders or leaders, key=lambda x: x.get('selection_score', 0), reverse=True)[:25]

previous_snapshot = {}
if SNAPSHOT_PATH.exists():
    try:
        previous_snapshot = json.loads(SNAPSHOT_PATH.read_text())
    except Exception:
        previous_snapshot = {}

prev_leadership = previous_snapshot.get('leadership_health', {}) if isinstance(previous_snapshot, dict) else {}
prev_top_turnover = [item.get('symbol') for item in previous_snapshot.get('top_alt_leaders_by_turnover', [])[:5]] if isinstance(previous_snapshot, dict) else []
current_top_turnover = [item.get('symbol') for item in leaders[:5]]
prev_major_health = previous_snapshot.get('major_health', {}) if isinstance(previous_snapshot, dict) else {}
leadership_delta = {
    'top15_alt_positive_count_delta': top15_alt_positive_count - (prev_leadership.get('top15_alt_positive_count') or 0),
    'top15_alt_low_range_count_delta': top15_alt_low_range_count - (prev_leadership.get('top15_alt_low_range_count') or 0),
    'weak_breadth_warning_changed': leadership_health['weak_breadth_warning'] != prev_leadership.get('weak_breadth_warning') if prev_leadership else None,
    'entered_top5_turnover': [sym for sym in current_top_turnover if sym and sym not in prev_top_turnover],
    'exited_top5_turnover': [sym for sym in prev_top_turnover if sym and sym not in current_top_turnover],
}
major_delta = {
    'major_avg_range_position_pct_delta': round(major_health['major_avg_range_position_pct'] - (prev_major_health.get('major_avg_range_position_pct') or 0), 2),
    'major_positive_count_delta': major_health['major_positive_count'] - (prev_major_health.get('major_positive_count') or 0),
    'major_negative_count_delta': major_health['major_negative_count'] - (prev_major_health.get('major_negative_count') or 0),
}

snapshot = {
    'updated_at_utc': datetime.now(timezone.utc).isoformat(),
    'leadership_delta': leadership_delta,
    'major_health': major_health,
    'major_delta': major_delta,
    'krw_market_count': len(krw),
    'major_health': major_health,
    'major_delta': major_delta,
    'leadership_health': leadership_health,
    'breakout_breadth': breakout_breadth,
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:30],
    'selection_leaderboard': selection_leaderboard,
    'top_positive_alts_by_turnover': positive[:30],
    'high_conviction_positive_alts': high_conviction_positive[:20],
    'resilient_positive_alts': resilient_positive[:20],
    'quality_recovery_alts': quality_recovery[:20],
    'continuation_positive_alts': continuation_positive[:20],
    'turnover_trap_alts': turnover_traps[:20],
    'fading_positive_leaders': fading_positive_leaders[:20],
    'reclaimed_positive_leaders': reclaimed_positive_leaders[:20],
    'fresh_breakout_positive_alts': fresh_breakout_positive_alts[:20],
    'stalled_positive_liquidity_alts': stalled_positive_liquidity_alts[:20],
    'exhausted_blowoff_positive_alts': exhausted_blowoff_positive_alts[:20],
    'stability_support_alts': stability_support_alts[:20],
    'secondary_continuation_alts': secondary_continuation_alts[:20],
    'quality_survivor_alts': quality_survivor_alts[:20],
    'mega_reclaim_alts': mega_reclaim_alts[:20],
    'relative_strength_reclaim_alts': relative_strength_reclaim_alts[:20],
}

(OUT / 'upbit_snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
print(json.dumps({
    'updated_at_utc': snapshot['updated_at_utc'],
    'krw_market_count': len(krw),
    'major_health': major_health,
    'major_delta': major_delta,
    'leadership_health': leadership_health,
    'breakout_breadth': breakout_breadth,
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:15],
    'selection_leaderboard': selection_leaderboard[:12],
    'top_positive_alts_by_turnover': positive[:15],
    'high_conviction_positive_alts': high_conviction_positive[:10],
    'resilient_positive_alts': resilient_positive[:10],
    'quality_recovery_alts': quality_recovery[:10],
    'continuation_positive_alts': continuation_positive[:10],
    'turnover_trap_alts': turnover_traps[:10],
    'fading_positive_leaders': fading_positive_leaders[:10],
    'reclaimed_positive_leaders': reclaimed_positive_leaders[:10],
    'fresh_breakout_positive_alts': fresh_breakout_positive_alts[:10],
    'stalled_positive_liquidity_alts': stalled_positive_liquidity_alts[:10],
    'stability_support_alts': stability_support_alts[:10],
    'secondary_continuation_alts': secondary_continuation_alts[:10],
    'quality_survivor_alts': quality_survivor_alts[:10],
    'mega_reclaim_alts': mega_reclaim_alts[:10],
    'relative_strength_reclaim_alts': relative_strength_reclaim_alts[:10],
}, ensure_ascii=False, indent=2))
