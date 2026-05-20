#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

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
majors = [r for r in rows if r['symbol'] in TOP4_MAJORS]
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

snapshot = {
    'updated_at_utc': datetime.now(timezone.utc).isoformat(),
    'krw_market_count': len(krw),
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:30],
    'top_positive_alts_by_turnover': positive[:30],
    'high_conviction_positive_alts': high_conviction_positive[:20],
    'resilient_positive_alts': resilient_positive[:20],
    'quality_recovery_alts': quality_recovery[:20],
    'continuation_positive_alts': continuation_positive[:20],
    'turnover_trap_alts': turnover_traps[:20],
    'fading_positive_leaders': fading_positive_leaders[:20],
}

(OUT / 'upbit_snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
print(json.dumps({
    'updated_at_utc': snapshot['updated_at_utc'],
    'krw_market_count': len(krw),
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:15],
    'top_positive_alts_by_turnover': positive[:15],
    'high_conviction_positive_alts': high_conviction_positive[:10],
    'resilient_positive_alts': resilient_positive[:10],
    'quality_recovery_alts': quality_recovery[:10],
    'continuation_positive_alts': continuation_positive[:10],
    'turnover_trap_alts': turnover_traps[:10],
    'fading_positive_leaders': fading_positive_leaders[:10],
}, ensure_ascii=False, indent=2))