"""Utility dashboard coverage for auth and UI contract."""

import importlib
import os
from unittest.mock import MagicMock, patch


def _dashboard_response(client_data=None):
    env = {
        'DATABASE_URL': 'postgresql://x:x@localhost/x',
        'REDIS_URL': 'memory://',
    }
    with patch.dict(os.environ, env, clear=False):
        with (
            patch('database.init_db', return_value=True),
            patch('database._connection_pool', MagicMock()),
            patch('database.is_db_available', return_value=True),
            patch('database.get_stats', return_value={'total_buildings': 0}),
            patch('database.get_utility_client', return_value=client_data),
        ):
            import app as app_module

            importlib.reload(app_module)
            app_module.app.config['TESTING'] = True
            client = app_module.app.test_client()

            if client_data:
                with client.session_transaction() as session:
                    session['utility_client_id'] = client_data.get('client_id', 'cid-1')

            return client.get('/utility/dashboard')


def _sample_client(status='active', api_key_hash='hash'):
    return {
        'client_id': 'cid-1',
        'company_name': 'Stadtwerke Test',
        'tier': 'pro',
        'status': status,
        'vnb_name': 'EKZ',
        'population': 25000,
        'api_key_hash': api_key_hash,
        'kanton': 'ZH',
        'contact_name': 'Max',
        'contact_email': 'max@test.ch',
        'contact_phone': '+41790000000',
        'created_at': None,
        'last_login_at': None,
    }


def test_dashboard_requires_auth_redirect():
    response = _dashboard_response(client_data=None)
    assert response.status_code == 302
    assert '/utility/login' in response.headers.get('Location', '')


def test_dashboard_renders_company_name():
    response = _dashboard_response(client_data=_sample_client())
    html = response.data.decode('utf-8', errors='ignore')
    assert response.status_code == 200
    assert 'Stadtwerke Test' in html


def test_dashboard_has_noindex_meta():
    response = _dashboard_response(client_data=_sample_client())
    html = response.data.decode('utf-8', errors='ignore')
    assert 'name="robots" content="noindex, nofollow"' in html


def test_dashboard_status_badge_active_and_trial():
    active_html = _dashboard_response(client_data=_sample_client(status='active')).data.decode('utf-8', errors='ignore')
    trial_html = _dashboard_response(client_data=_sample_client(status='trial')).data.decode('utf-8', errors='ignore')

    assert 'Active' in active_html
    assert 'Trial' in trial_html


def test_dashboard_api_key_section_present():
    response = _dashboard_response(client_data=_sample_client(api_key_hash='abc'))
    html = response.data.decode('utf-8', errors='ignore')
    assert 'API-Zugang' in html
    assert 'API-Schluessel aktiv' in html


def test_dashboard_onboarding_steps_render_without_stale_white_label():
    response = _dashboard_response(client_data=_sample_client(api_key_hash=None))
    html = response.data.decode('utf-8', errors='ignore')

    assert 'Onboarding' in html
    assert 'Technische Integration prüfen' in html
    assert 'White-Label Branding' not in html
