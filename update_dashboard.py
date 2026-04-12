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

latest_report = None
reports = sorted(REPORTS.glob('*.md'))
if reports:
    latest_report = reports[-1]

portfolio = {}
if PORTFOLIO.exists():
    portfolio = json.loads(PORTFOLIO.read_text())

judgment = 'unknown'
confidence = 'unknown'
suggested_action = 'unknown'
updated_at = None
summary_lines = []

if latest_report and latest_report.exists():
    text = latest_report.read_text()
    lines = text.splitlines()
    in_reasons = False
    for line in lines:
        if line.startswith('- Timestamp: '):
            updated_at = line.replace('- Timestamp: ', '').strip()
        elif line.startswith('- Judgment: '):
            judgment = line.replace('- Judgment: ', '').strip()
        elif line.startswith('- Confidence: '):
            confidence = line.replace('- Confidence: ', '').strip()
        elif line.startswith('- Suggested action: '):
            suggested_action = line.replace('- Suggested action: ', '').strip()
        elif line.startswith('- BTC snapshot: ') or line.startswith('- Trend summary: ') or line.startswith('- News summary: '):
            summary_lines.append(line[2:])
        elif line.startswith('- Reasons:'):
            in_reasons = True
            continue
        elif in_reasons:
            if line.startswith('  - '):
                summary_lines.append(line.strip())
            elif line.startswith('- '):
                in_reasons = False
    (DASH / 'latest-report.md').write_text(text)

initial_cash = portfolio.get('initial_cash_krw', 0) or 0
valuation = portfolio.get('last_valuation_krw', 0) or 0
return_pct = ((valuation - initial_cash) / initial_cash * 100) if initial_cash else 0
history = portfolio.get('history', []) or []
recent_trades = history[-5:][::-1]

status = {
    'project': portfolio.get('project', "bit's today"),
    'judgment': judgment,
    'confidence': confidence,
    'suggested_action': suggested_action,
    'updated_at': updated_at,
    'cash_krw': fmt_krw(portfolio.get('cash_krw', 0)),
    'btc': f"{portfolio.get('btc', 0)} BTC",
    'avg_buy_price_krw': fmt_krw(portfolio.get('avg_buy_price_krw', 0)),
    'last_price_krw': fmt_krw(portfolio.get('last_price_krw', 0)),
    'realized_pnl_krw': fmt_krw(portfolio.get('realized_pnl_krw', 0)),
    'last_valuation_krw': fmt_krw(valuation),
    'initial_cash_krw': fmt_krw(initial_cash),
    'return_pct': round(return_pct, 2),
    'last_action': portfolio.get('last_action', '-'),
    'trade_count': portfolio.get('trade_count', 0),
    'last_updated': portfolio.get('last_updated', '-'),
    'summary': summary_lines[:6],
    'recent_trades': recent_trades,
    'latest_report_file': latest_report.name if latest_report else None,
}
(DASH / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
print('dashboard updated')
