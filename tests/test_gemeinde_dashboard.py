"""Gemeinde dashboard tests for shared dashboard foundation."""

import importlib
import os
from unittest.mock import MagicMock, patch


def _request(path, *, env=None, get_muni=None, stats=None):
    merged_env = {
        'DATABASE_URL': 'postgresql://x:x@localhost/x',
        'REDIS_URL': 'memory://',
    }
    if env:
        merged_env.update(env)

    with patch.dict(os.environ, merged_env, clear=False):
        with (
            patch('database.init_db', return_value=True),
            patch('database._connection_pool', MagicMock()),
            patch('database.is_db_available', return_value=True),
            patch('database.get_stats', return_value=stats or {'total_buildings': 2, 'registrations_today': 1}),
            patch('database.get_municipality', return_value=get_muni),
        ):
            import app as app_module

            importlib.reload(app_module)
            app_module.app.config['TESTING'] = True
            client = app_module.app.test_client()
            return client.get(path)


def test_dashboard_supports_bfs_lookup():
    municipality = {'name': 'Dietikon', 'subdomain': 'dietikon', 'dso_name': 'EKZ', 'onboarding_status': 'registered'}
    response = _request('/gemeinde/dashboard?bfs=261', get_muni=municipality)

    assert response.status_code == 200
    html = response.data.decode('utf-8', errors='ignore')
    assert 'Dietikon' in html


def test_dashboard_has_shared_nav_and_noindex():
    municipality = {'name': 'Dietikon', 'subdomain': 'dietikon', 'dso_name': 'EKZ', 'onboarding_status': 'registered'}
    response = _request('/gemeinde/dashboard?subdomain=dietikon', get_muni=municipality)

    html = response.data.decode('utf-8', errors='ignore')
    assert 'id="dashboard-title"' in html
    assert 'Gemeinde Dashboard' in html
    assert 'name="robots" content="noindex, nofollow"' in html


def test_dashboard_uses_utf8_umlauts_and_no_entities():
    municipality = {'name': 'Dietikon', 'subdomain': 'dietikon', 'dso_name': 'EKZ', 'onboarding_status': 'registered'}
    response = _request('/gemeinde/dashboard?subdomain=dietikon', get_muni=municipality)

    html = response.data.decode('utf-8', errors='ignore')
    assert 'Nächste Schritte' in html
    assert 'Erste LEG gründen' in html
    assert '&uuml;' not in html
    assert '&auml;' not in html


def test_dashboard_renders_ga4_when_configured():
    municipality = {'name': 'Dietikon', 'subdomain': 'dietikon', 'dso_name': 'EKZ', 'onboarding_status': 'registered'}
    response = _request(
        '/gemeinde/dashboard?subdomain=dietikon',
        env={'GA4_MEASUREMENT_ID': 'G-TEST123'},
        get_muni=municipality,
    )

    html = response.data.decode('utf-8', errors='ignore')
    assert 'googletagmanager.com/gtag/js?id=G-TEST123' in html


def test_dashboard_not_found_message():
    response = _request('/gemeinde/dashboard?subdomain=missing', get_muni=None)

    assert response.status_code == 200
    html = response.data.decode('utf-8', errors='ignore')
    assert 'Gemeinde nicht gefunden' in html
