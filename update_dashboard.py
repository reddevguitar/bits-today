#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path('/Users/reddevguitar/.openclaw/workspace/bits-today')
REPORTS = BASE / 'reports'
DASH = BASE / 'dashboard'
PORTFOLIO = BASE / 'portfolio.json'


def fmt_krw(value):
    if isinstance(value, (int, float)):
        return f"{value:,.0f} KRW"
    return str(value)

reports = sorted(REPORTS.glob('*.md'))
latest_report = reports[-1] if reports else None
portfolio = json.loads(PORTFOLIO.read_text()) if PORTFOLIO.exists() else {}
positions = portfolio.get('positions', {}) or {}
history = portfolio.get('history', []) or []

status = {
    'project': portfolio.get('project', "bit's today"),
    'judgment': 'unknown',
    'confidence': 'unknown',
    'suggested_action': 'unknown',
    'updated_at': None,
    'market_status': '데이터 없음',
    'fear_greed': '데이터 없음',
    'btc_snapshot': '데이터 없음',
    'cash_krw': fmt_krw(portfolio.get('cash_krw', 0)),
    'realized_pnl_krw': fmt_krw(portfolio.get('realized_pnl_krw', 0)),
    'last_valuation_krw': fmt_krw(portfolio.get('last_valuation_krw', 0)),
    'initial_cash_krw': fmt_krw(portfolio.get('initial_cash_krw', 0)),
    'return_pct': round((((portfolio.get('last_valuation_krw', 0) or 0) - (portfolio.get('initial_cash_krw', 0) or 0)) / (portfolio.get('initial_cash_krw', 1) or 1)) * 100, 2) if portfolio.get('initial_cash_krw', 0) else 0,
    'last_action': portfolio.get('last_action', '-'),
    'trade_count': portfolio.get('trade_count', 0),
    'last_updated': portfolio.get('last_updated', '-'),
    'summary': [],
    'recent_trades': history[-8:][::-1],
    'recent_reports': [{'file': p.name, 'title': p.stem} for p in reports[-8:][::-1]],
    'positions': [],
    'chart_series': {},
    'latest_report_file': latest_report.name if latest_report else None,
}

for symbol, pos in positions.items():
    status['positions'].append({
        'symbol': symbol,
        'market': pos.get('market', '-'),
        'amount': pos.get('amount', 0),
        'avg_buy_price_krw': fmt_krw(pos.get('avg_buy_price_krw', 0)),
        'last_price_krw': fmt_krw(pos.get('last_price_krw', 0)),
        'thesis': pos.get('thesis', '-'),
        'strategy': pos.get('strategy', '-'),
    })

for item in history[-30:]:
    sym = item.get('symbol', 'UNKNOWN')
    status['chart_series'].setdefault(sym, []).append({
        'timestamp': item.get('timestamp'),
        'price_krw': item.get('price_krw', 0),
        'action': item.get('action', '-')
    })

if latest_report and latest_report.exists():
    text = latest_report.read_text()
    (DASH / 'latest-report.md').write_text(text)
    lines = text.splitlines()
    for line in lines:
        if line.startswith('- 시각: '):
            status['updated_at'] = line.replace('- 시각: ', '').strip()
        elif line.startswith('- BTC 스냅샷: '):
            status['btc_snapshot'] = line.replace('- BTC 스냅샷: ', '').strip()
        elif line.startswith('- 현재 시황: '):
            status['market_status'] = line.replace('- 현재 시황: ', '').strip()
        elif line.startswith('- 공포탐욕지수: '):
            status['fear_greed'] = line.replace('- 공포탐욕지수: ', '').strip()
        elif line.startswith('- 판단: '):
            status['judgment'] = line.replace('- 판단: ', '').strip()
        elif line.startswith('- 신뢰도: '):
            status['confidence'] = line.replace('- 신뢰도: ', '').strip()
        elif line.startswith('- 추천 행동: '):
            status['suggested_action'] = line.replace('- 추천 행동: ', '').strip()
        elif line.startswith('- '):
            status['summary'].append(line[2:])

(DASH / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
print('dashboard updated')
