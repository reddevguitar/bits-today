#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path('/Users/reddevguitar/.openclaw/workspace/bits-today')
REPORTS = BASE / 'reports'
DASH = BASE / 'dashboard'
PORTFOLIO = BASE / 'portfolio.json'

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

if latest_report and latest_report.exists():
    text = latest_report.read_text()
    for line in text.splitlines():
        if line.startswith('- Timestamp: '):
            updated_at = line.replace('- Timestamp: ', '').strip()
        elif line.startswith('- Judgment: '):
            judgment = line.replace('- Judgment: ', '').strip()
        elif line.startswith('- Confidence: '):
            confidence = line.replace('- Confidence: ', '').strip()
        elif line.startswith('- Suggested action: '):
            suggested_action = line.replace('- Suggested action: ', '').strip()
    (DASH / 'latest-report.md').write_text(text)

status = {
    'judgment': judgment,
    'confidence': confidence,
    'suggested_action': suggested_action,
    'updated_at': updated_at,
    'cash_krw': f"{portfolio.get('cash_krw', 0):,} KRW" if isinstance(portfolio.get('cash_krw', 0), (int, float)) else str(portfolio.get('cash_krw', '-')),
    'btc': f"{portfolio.get('btc', 0)} BTC",
    'realized_pnl_krw': f"{portfolio.get('realized_pnl_krw', 0):,} KRW" if isinstance(portfolio.get('realized_pnl_krw', 0), (int, float)) else str(portfolio.get('realized_pnl_krw', '-')),
    'last_valuation_krw': f"{portfolio.get('last_valuation_krw', 0):,} KRW" if isinstance(portfolio.get('last_valuation_krw', 0), (int, float)) else str(portfolio.get('last_valuation_krw', '-')),
}
(DASH / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
print('dashboard updated')
