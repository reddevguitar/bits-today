#!/usr/bin/env python3
import json
import re
from pathlib import Path

BASE = Path('/Users/reddevguitar/.openclaw/workspace/bits-today')
REPORTS = BASE / 'reports'
DASH = BASE / 'dashboard'
PORTFOLIO = BASE / 'portfolio.json'
STRATEGY = BASE / 'strategy-state.json'

ICONS = {
    'BTC': '₿',
    'ETH': '◆',
    'XRP': '💧',
    'SOL': '☀️',
    'DOGE': '🐕',
    'SUPER': '🦸',
    'CHZ': '⚽',
    'BLUR': '🌫️',
    'CFG': '🏗️',
    'PIEVERSE': '🥧',
    'SOON': '🔜',
    'AAVE': '🏦',
    'BIO': '🧬',
    'NEWT': '🆕',
    'SENT': '📡',
    'IP': '🪪',
    'AXL': '🛰️',
    'AXS': '🎮',
    'CHIP': '🧩',
    'FLOCK': '🐦',
    'OPEN': '📬',
    'XLM': '✨',
    'MET2': '🧱',
    'CPOOL': '🌊',
    'AVNT': '🚀',
    'FLUID': '💧',
    'SEI': '🟥',
    'CARV': '🕹️',
    'PENGU': '🐧',
    'SPK': '⚡',
    'KAT': '🐱',
    'ZAMA': '🛡️',
    'SKR': '🧭',
    'TREE': '🌳',
    'RED': '🟥',
    'ENSO': '🌀',
    'ESP': '☕',
    'ZKP': '🔐',
    'ZBT': '🧨',
    'API3': '📡',
    'RVN': '🪶',
    'SAFE': '🛟',
    'HYPER': '⚛️',
    'ORCA': '🐋',
    'SAHARA': '🏜️'
}


def fmt_krw(value):
    if isinstance(value, (int, float)):
        return f"{value:,.0f} KRW"
    return str(value)


def icon_for(symbol):
    return ICONS.get(symbol, '🪙')


def extract_threshold_krw(text):
    if not text:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)\s*원', str(text))
    return float(match.group(1)) if match else None


def parse_report_sections(text):
    sections = {}
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith('## '):
            current = line.replace('## ', '').strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {k: [line for line in v if line.strip()] for k, v in sections.items()}


def classify_candidate_health(last_price, threshold):
    if threshold is None or not isinstance(last_price, (int, float)):
        return 'unknown', None
    distance_pct = round(((last_price - threshold) / threshold) * 100, 2) if threshold else None
    if last_price < threshold:
        return 'broken', distance_pct
    if distance_pct is not None and distance_pct <= 5:
        return 'near', distance_pct
    return 'healthy', distance_pct


reports = sorted(REPORTS.glob('*.md'))
latest_report = reports[-1] if reports else None
portfolio = json.loads(PORTFOLIO.read_text()) if PORTFOLIO.exists() else {}
strategy = json.loads(STRATEGY.read_text()) if STRATEGY.exists() else {}
positions = portfolio.get('positions', {}) or {}
history = portfolio.get('history', []) or []
preferred = strategy.get('preferred_buy_candidates') or []
watchlist = portfolio.get('watchlist', []) or strategy.get('watchlist', []) or []
improvements = strategy.get('improvement_log', []) or []
risk_plan = strategy.get('risk_plan', {}) or {}
scorecard = strategy.get('scorecard', {}) or {}
rotation_map_raw = strategy.get('rotation_map', []) or []
self_evaluation = strategy.get('self_evaluation', {}) or {}
sections = {}
recent_history = history[-40:]
excluded_majors = {'BTC', 'ETH', 'XRP', 'SOL'}
preferred_symbols = [item.get('symbol') for item in preferred[:5]]
selection_checks = {
    'preferred_count': len(preferred[:5]),
    'has_exactly_five': len(preferred[:5]) == 5,
    'excluded_majors_present': [sym for sym in preferred_symbols if sym in excluded_majors],
    'majors_rule_ok': not any(sym in excluded_majors for sym in preferred_symbols)
}
recent_buys = sum(1 for item in recent_history if item.get('action') == 'BUY')
recent_sells = sum(1 for item in recent_history if item.get('action') == 'SELL')
latest_cycle_day = str(portfolio.get('last_updated', ''))[:10]
preferred_changes = [item.get('change_pct_24h', 0) or 0 for item in preferred[:5]]
preferred_turnovers = [item.get('turnover_krw_24h', 0) or 0 for item in preferred[:5]]
total_preferred_turnover = sum(preferred_turnovers)
leader_turnover_share = round((max(preferred_turnovers) / total_preferred_turnover) * 100, 2) if total_preferred_turnover else 0
leader_symbol = preferred_turnovers.index(max(preferred_turnovers)) if preferred_turnovers else None
market_breadth = {
    'preferred_avg_change_pct_24h': round(sum(preferred_changes) / len(preferred_changes), 2) if preferred_changes else 0,
    'preferred_positive_count': sum(1 for x in preferred_changes if x > 0),
    'preferred_negative_count': sum(1 for x in preferred_changes if x < 0),
    'preferred_positive_ratio_pct': round((sum(1 for x in preferred_changes if x > 0) / len(preferred_changes)) * 100, 2) if preferred_changes else 0,
    'preferred_turnover_total_krw_24h': total_preferred_turnover,
    'leader_turnover_share_pct': leader_turnover_share,
    'leader_symbol': preferred[leader_symbol].get('symbol') if leader_symbol is not None and preferred else None
}
risk_exit_rules = []
if risk_plan.get('review_trigger'):
    risk_exit_rules.append(risk_plan['review_trigger'])
risk_exit_rules.extend(risk_plan.get('hard_rules', []))
rotation_map = [
    {
        'bucket': f"{item.get('out', '-')} → {item.get('in', '-')}",
        'symbols': [item.get('out', '-'), item.get('in', '-')],
        'note': item.get('why', '-')
    }
    for item in rotation_map_raw
]
discipline_alerts = []
candidate_health = []
for item in preferred[:5]:
    symbol = item.get('symbol')
    pos = positions.get(symbol, {}) or {}
    threshold = extract_threshold_krw(item.get('invalidated_if') or item.get('risk'))
    last_price = pos.get('last_price_krw', item.get('price_krw'))
    health, distance_pct = classify_candidate_health(last_price, threshold)
    candidate_health.append({
        'icon': icon_for(symbol),
        'symbol': symbol,
        'last_price_krw': last_price,
        'threshold_krw': threshold,
        'distance_to_invalidation_pct': distance_pct,
        'status': health
    })
    if threshold is not None and isinstance(last_price, (int, float)) and last_price < threshold:
        discipline_alerts.append({
            'symbol': symbol,
            'last_price_krw': last_price,
            'threshold_krw': threshold,
            'message': f"{symbol} 가격이 무효화 기준 {threshold:,.1f}원 아래"
        })
portfolio_health = {
    'discipline_alert_count': len(discipline_alerts),
    'green_position_count': sum(1 for symbol, pos in positions.items() if (pos.get('last_price_krw', 0) or 0) >= (pos.get('avg_buy_price_krw', 0) or 0)),
    'red_position_count': sum(1 for symbol, pos in positions.items() if (pos.get('last_price_krw', 0) or 0) < (pos.get('avg_buy_price_krw', 0) or 0))
}

status = {
    'project': portfolio.get('project', "bit's today"),
    'judgment': strategy.get('overall_bias', 'unknown'),
    'confidence': strategy.get('confidence', 'unknown'),
    'suggested_action': 'aggressive diversified paper trading with refreshed alt focus',
    'updated_at': None,
    'market_status': strategy.get('major_coin_summary', '데이터 없음'),
    'fear_greed': strategy.get('fear_greed', '데이터 없음'),
    'btc_snapshot': strategy.get('btc_reference', '데이터 없음'),
    'cash_krw': fmt_krw(portfolio.get('cash_krw', 0)),
    'realized_pnl_krw': fmt_krw(portfolio.get('realized_pnl_krw', 0)),
    'last_valuation_krw': fmt_krw(portfolio.get('last_valuation_krw', 0)),
    'initial_cash_krw': fmt_krw(portfolio.get('initial_cash_krw', 0)),
    'return_pct': round((((portfolio.get('last_valuation_krw', 0) or 0) - (portfolio.get('initial_cash_krw', 0) or 0)) / (portfolio.get('initial_cash_krw', 1) or 1)) * 100, 2) if portfolio.get('initial_cash_krw', 0) else 0,
    'last_action': portfolio.get('last_action', '-'),
    'trade_count': portfolio.get('trade_count', 0),
    'last_updated': portfolio.get('last_updated', '-'),
    'position_count': len(positions),
    'rotation_footprint': {
        'recent_buy_count': recent_buys,
        'recent_sell_count': recent_sells,
        'recent_rotation_count': min(recent_buys, recent_sells),
        'recent_trade_actions_24h': sum(1 for item in history if latest_cycle_day and str(item.get('timestamp', '')).startswith(latest_cycle_day))
    },
    'summary': [],
    'recent_trades': history[-8:][::-1],
    'recent_reports': [{'file': p.name, 'title': p.stem} for p in reports[-8:][::-1]],
    'positions': [],
    'chart_series': {},
    'latest_report_file': latest_report.name if latest_report else None,
    'preferred_buy_candidates': [
        {
            'icon': icon_for(item.get('symbol', '')),
            'symbol': item.get('symbol', '-'),
            'market': item.get('market', '-'),
            'price_krw': item.get('price_krw'),
            'change_pct_24h': item.get('change_pct_24h'),
            'turnover_krw_24h': item.get('turnover_krw_24h'),
            'reason': item.get('reason', '-'),
            'score': item.get('score'),
            'community': item.get('community'),
            'risk': item.get('risk'),
            'allocation_krw': item.get('allocation_krw'),
            'role': item.get('role'),
            'invalidated_if': item.get('invalidated_if')
        }
        for item in preferred[:5]
    ],
    'reference_watchlist': [
        {
            'icon': icon_for(item.get('symbol', '')),
            'symbol': item.get('symbol', '-'),
            'market': item.get('market', '-'),
            'reason': item.get('reason', '-')
        }
        for item in watchlist[:8]
    ],
    'cycle_improvements': improvements[:5],
    'top_line': strategy.get('top_line', '6시간 단위 자율 전략 개선 루프 실행 중'),
    'ui_version': strategy.get('ui_version', 'v2'),
    'risk_plan': {**risk_plan, 'exit_rules': risk_exit_rules},
    'scorecard': scorecard,
    'rotation_map': rotation_map,
    'self_evaluation': self_evaluation,
    'market_breadth': market_breadth,
    'selection_checks': selection_checks,
    'discipline_alerts': discipline_alerts,
    'candidate_health': candidate_health,
    'portfolio_health': portfolio_health,
    'report_sections': sections,
}

for symbol, pos in positions.items():
    amount = pos.get('amount', 0) or 0
    avg_buy = pos.get('avg_buy_price_krw', 0) or 0
    last_price = pos.get('last_price_krw', 0) or 0
    pnl_krw = (last_price - avg_buy) * amount
    pnl_pct = round(((last_price - avg_buy) / avg_buy) * 100, 2) if avg_buy else 0
    status['positions'].append({
        'icon': icon_for(symbol),
        'symbol': symbol,
        'market': pos.get('market', '-'),
        'amount': amount,
        'avg_buy_price_krw': fmt_krw(avg_buy),
        'last_price_krw': fmt_krw(last_price),
        'thesis': pos.get('thesis', '-'),
        'strategy': pos.get('strategy', '-'),
        'role': pos.get('role', '-'),
        'risk_limit_pct': pos.get('risk_limit_pct'),
        'profit_take_pct': pos.get('profit_take_pct'),
        'pnl_krw': fmt_krw(pnl_krw),
        'pnl_pct': pnl_pct
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
    sections = parse_report_sections(text)
    status['report_sections'] = sections
    (DASH / 'latest-report.md').write_text(text)
    lines = text.splitlines()
    for line in lines:
        if line.startswith('- 시각: '):
            status['updated_at'] = line.replace('- 시각: ', '').strip()
        elif line.startswith('- 기준 한줄: '):
            status['top_line'] = line.replace('- 기준 한줄: ', '').strip()
        elif line.startswith('- 시장 한줄 요약: '):
            status['market_status'] = line.replace('- 시장 한줄 요약: ', '').strip()
        elif line.startswith('- 공포탐욕지수: '):
            status['fear_greed'] = line.replace('- 공포탐욕지수: ', '').strip()
        elif line.startswith('- BTC 참고: '):
            status['btc_snapshot'] = line.replace('- BTC 참고: ', '').strip()
        elif line.startswith('- 판단: '):
            status['judgment'] = line.replace('- 판단: ', '').strip()
        elif line.startswith('- 신뢰도: '):
            status['confidence'] = line.replace('- 신뢰도: ', '').strip()
        elif line.startswith('- 추천 행동: '):
            status['suggested_action'] = line.replace('- 추천 행동: ', '').strip()
        elif line.startswith('- '):
            status['summary'].append(line[2:])

(DASH / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
(BASE / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
if latest_report and latest_report.exists():
    (BASE / 'latest-report.md').write_text(latest_report.read_text())
print('dashboard updated')
