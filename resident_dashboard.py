"""Resident dashboard blueprint with route parity to legacy app routes."""

import os

from flask import Blueprint, g, jsonify, render_template, request
from jinja2 import TemplateNotFound

import database as db
import tenant as tenant_module

resident_bp = Blueprint('resident_dashboard', __name__)
APP_BASE_URL = os.getenv('APP_BASE_URL', 'http://localhost:5003')
SITE_URL = APP_BASE_URL.rstrip('/')


def _render_city_template(template_name, **kwargs):
    tenant = getattr(g, 'tenant', tenant_module.DEFAULT_TENANT)
    kwargs.setdefault('tenant', tenant)
    kwargs.setdefault('site_url', SITE_URL)
    kwargs.setdefault('ga4_id', tenant.get('ga4_id') or os.getenv('GA4_MEASUREMENT_ID', ''))
    city_path = f"cities/{tenant['territory']}/{template_name}"
    try:
        return render_template(city_path, **kwargs)
    except TemplateNotFound:
        return render_template(template_name, **kwargs)


@resident_bp.route('/dashboard')
def dashboard():
    building_id = request.args.get('bid', '').strip()
    if not building_id:
        return _render_city_template('dashboard.html', error='Kein Profil angegeben.', user=None)

    user = db.get_building_for_dashboard(building_id)
    if not user:
        return _render_city_template('dashboard.html', error='Profil nicht gefunden.', user=None)

    score = 0
    checks = []
    if user.get('verified'):
        score += 25
        checks.append(('E-Mail bestätigt', True))
    else:
        checks.append(('E-Mail bestätigt', False))
    if user.get('annual_consumption_kwh'):
        score += 25
        checks.append(('Verbrauchsdaten hinterlegt', True))
    else:
        checks.append(('Verbrauchsdaten hinterlegt', False))
    if user.get('share_with_utility'):
        score += 25
        checks.append(('EVU-Einwilligung erteilt', True))
    else:
        checks.append(('EVU-Einwilligung erteilt', False))
    if user.get('share_with_neighbors'):
        score += 25
        checks.append(('Nachbar-Einwilligung erteilt', True))
    else:
        checks.append(('Nachbar-Einwilligung erteilt', False))

    neighbor_count = 0
    referral_link = ''
    lat = user.get('lat')
    lon = user.get('lon')
    city_id = g.tenant.get('territory') if hasattr(g, 'tenant') else None
    if lat and lon:
        neighbor_count = db.get_neighbor_count_near(float(lat), float(lon), city_id=city_id)
    ref_code = db.get_referral_code(building_id)
    if ref_code:
        referral_link = f'{APP_BASE_URL}/?ref={ref_code}'

    return _render_city_template(
        'dashboard.html',
        user=user,
        readiness_score=score,
        checks=checks,
        neighbor_count=neighbor_count,
        referral_link=referral_link,
        error=None,
    )


@resident_bp.route('/api/referral/stats/<building_id>')
def api_referral_stats(building_id):
    stats = db.get_referral_stats(building_id)
    referral_code = db.get_referral_code(building_id)
    return jsonify(
        {
            'referral_code': referral_code,
            'referral_link': f'{APP_BASE_URL}/?ref={referral_code}' if referral_code else None,
            'total_referrals': stats.get('total_referrals', 0),
        }
    )


@resident_bp.route('/api/referral/leaderboard')
def api_referral_leaderboard():
    city_id = g.tenant.get('territory') if hasattr(g, 'tenant') else None
    leaderboard = db.get_referral_leaderboard(limit=10, city_id=city_id)
    for entry in leaderboard:
        street = entry.get('street', '')
        entry['display_name'] = street[:15] + '...' if len(street) > 15 else street
    return jsonify({'leaderboard': leaderboard})
