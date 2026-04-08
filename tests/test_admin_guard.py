"""Guardrail tests: admin surface must stay private."""

import importlib
import os
from unittest.mock import MagicMock, patch

import pytest

ADMIN_ROUTES = [
    '/admin/overview',
    '/admin/pipeline',
    '/admin/export',
    '/admin/lea-reports',
    '/api/email/stats',
    '/api/billing/community/c1/period/1',
]


def _request(path, *, headers=None, admin_token='test-admin-token'):
    env = {
        'DATABASE_URL': 'postgresql://x:x@localhost/x',
        'REDIS_URL': 'memory://',
        'ADMIN_TOKEN': admin_token,
    }
    with patch.dict(os.environ, env, clear=False):
        with (
            patch('database.init_db', return_value=True),
            patch('database._connection_pool', MagicMock()),
            patch('database.is_db_available', return_value=True),
            patch('database.get_stats', return_value={'total_buildings': 0, 'registrations_today': 0}),
            patch('database.get_email_stats', return_value={'pending': 0, 'sent': 0, 'failed': 0}),
            patch('database.count_consented_buildings', return_value=0),
            patch('database.get_all_municipalities', return_value=[]),
            patch('database.get_vnb_pipeline', return_value=[]),
            patch('database.get_vnb_pipeline_stats', return_value={'total': 0, 'funnel': {}}),
            patch('database.get_all_building_profiles', return_value=[]),
            patch('database.get_lea_reports', return_value=[]),
            patch('database.get_billing_period', return_value={'id': 1, 'community_id': 'c1'}),
            patch('database.get_all_utility_clients', return_value=[]),
            patch('database.get_utility_client_stats', return_value={}),
        ):
            import app as app_module

            importlib.reload(app_module)
            app_module.app.config['TESTING'] = True
            client = app_module.app.test_client()
            return client.get(path, headers=headers or {})


@pytest.mark.parametrize('route', ADMIN_ROUTES)
def test_admin_routes_require_header_token(route):
    unauthorized = _request(route)
    assert unauthorized.status_code == 403

    query_only = _request(f'{route}?token=test-admin-token')
    assert query_only.status_code == 403


@pytest.mark.parametrize('route', ADMIN_ROUTES)
def test_admin_routes_accept_valid_header(route):
    authorized = _request(route, headers={'X-Admin-Token': 'test-admin-token'})
    assert authorized.status_code not in (403, 404)


def test_admin_routes_return_404_when_admin_token_missing():
    response = _request('/admin/overview', headers={'X-Admin-Token': 'any'}, admin_token='')
    assert response.status_code == 404


def test_utility_admin_clients_header_only_auth():
    unauthorized = _request('/utility/admin/clients')
    assert unauthorized.status_code == 403

    query_only = _request('/utility/admin/clients?token=test-admin-token')
    assert query_only.status_code == 403

    authorized = _request('/utility/admin/clients', headers={'X-Admin-Token': 'test-admin-token'})
    assert authorized.status_code == 200
