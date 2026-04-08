"""Resident dashboard blueprint extraction parity tests."""

import importlib
import os
from unittest.mock import MagicMock, patch


BASE_USER = {
    'building_id': 'b1',
    'address': 'Musterstrasse 1, 8000 Zürich',
    'verified': True,
    'annual_consumption_kwh': 4200,
    'share_with_utility': True,
    'share_with_neighbors': True,
    'lat': 47.37,
    'lon': 8.54,
}


def _get(path, *, user=None, referral_code='abc123', referral_stats=None, leaderboard=None):
    env = {
        'DATABASE_URL': 'postgresql://x:x@localhost/x',
        'REDIS_URL': 'memory://',
        'APP_BASE_URL': 'http://openleg.ch',
    }
    with patch.dict(os.environ, env, clear=False):
        with (
            patch('database.init_db', return_value=True),
            patch('database._connection_pool', MagicMock()),
            patch('database.is_db_available', return_value=True),
            patch('database.get_stats', return_value={'total_buildings': 0, 'registrations_today': 0}),
            patch('database.get_building_for_dashboard', return_value=user),
            patch('database.get_neighbor_count_near', return_value=2),
            patch('database.get_referral_code', return_value=referral_code),
            patch('database.get_referral_stats', return_value=referral_stats or {'total_referrals': 4}),
            patch(
                'database.get_referral_leaderboard',
                return_value=leaderboard
                or [
                    {'street': 'Lange Musterstrasse 123', 'count': 3},
                    {'street': 'Kurzweg', 'count': 1},
                ],
            ),
        ):
            import app as app_module

            importlib.reload(app_module)
            app_module.app.config['TESTING'] = True
            client = app_module.app.test_client()
            return client.get(path)


def test_dashboard_requires_bid_query_param():
    response = _get('/dashboard', user=None)
    assert response.status_code == 200
    html = response.data.decode('utf-8', errors='ignore')
    assert 'Kein Profil angegeben.' in html


def test_dashboard_renders_with_valid_bid_and_score():
    response = _get('/dashboard?bid=b1', user=BASE_USER)
    assert response.status_code == 200
    html = response.data.decode('utf-8', errors='ignore')
    assert '100%' in html
    assert 'Ihre LEG-Bereitschaft' in html


def test_dashboard_renders_referral_link_and_noindex():
    response = _get('/dashboard?bid=b1', user=BASE_USER)
    html = response.data.decode('utf-8', errors='ignore')
    assert 'http://openleg.ch/?ref=abc123' in html
    assert 'name="robots" content="noindex, nofollow"' in html


def test_referral_stats_route_preserved():
    response = _get('/api/referral/stats/b1', referral_stats={'total_referrals': 7}, referral_code='code7')
    assert response.status_code == 200
    data = response.get_json()
    assert data['referral_code'] == 'code7'
    assert data['total_referrals'] == 7


def test_referral_leaderboard_truncates_display_names():
    response = _get('/api/referral/leaderboard')
    assert response.status_code == 200
    data = response.get_json()
    assert data['leaderboard'][0]['display_name'].endswith('...')
    assert data['leaderboard'][1]['display_name'] == 'Kurzweg'
