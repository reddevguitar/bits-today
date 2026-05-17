#!/usr/bin/env python3
import json
import math
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/Users/reddevguitar/.openclaw/workspace/bits-today')
OUT = BASE / 'data'
OUT.mkdir(exist_ok=True)

TOP4_MAJORS = {'BTC', 'ETH', 'XRP', 'SOL'}
STABLES = {'USDT', 'USDC', 'USDS', 'USDE', 'USD1'}


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
    chunk = market_codes[i:i+80]
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
    row = {
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
    }
    rows.append(row)

rows.sort(key=lambda x: x['turnover_krw_24h'], reverse=True)
majors = [r for r in rows if r['symbol'] in TOP4_MAJORS]
leaders = [r for r in rows if r['symbol'] not in TOP4_MAJORS and r['symbol'] not in STABLES]
positive = [r for r in leaders if r['change_pct_24h'] > 0]

snapshot = {
    'updated_at_utc': datetime.now(timezone.utc).isoformat(),
    'krw_market_count': len(krw),
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:30],
    'top_positive_alts_by_turnover': positive[:30],
}

(OUT / 'upbit_snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
print(json.dumps({
    'updated_at_utc': snapshot['updated_at_utc'],
    'krw_market_count': len(krw),
    'top_majors': majors,
    'top_alt_leaders_by_turnover': leaders[:15],
    'top_positive_alts_by_turnover': positive[:15],
}, ensure_ascii=False, indent=2))
