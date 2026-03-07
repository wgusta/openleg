"""Admin dashboard blueprint tests."""

import importlib
import os
from unittest.mock import MagicMock, patch

import pytest

ROUTES = ['/admin/overview', '/admin/pipeline', '/admin/export', '/admin/lea-reports']


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
            patch('database.get_stats', return_value={'total_buildings': 10, 'registrations_today': 2}),
            patch('database.get_email_stats', return_value={'pending': 1, 'sent': 2, 'failed': 0}),
            patch('database.count_consented_buildings', return_value=5),
            patch('database.get_all_municipalities', return_value=[{'id': 1}]),
            patch('database.get_vnb_pipeline', return_value=[]),
            patch('database.get_vnb_pipeline_stats', return_value={'total': 0, 'funnel': {}}),
            patch('database.get_all_building_profiles', return_value=[{'building_id': 'b1', 'city_id': 'zh'}]),
            patch('database.get_lea_reports', return_value=[{'job_name': 'daily', 'status': 'ok'}]),
            patch('database.get_billing_period', return_value={'id': 1}),
        ):
            import app as app_module

            importlib.reload(app_module)
            app_module.app.config['TESTING'] = True
            client = app_module.app.test_client()
            return client.get(path, headers=headers or {})


@pytest.mark.parametrize('route', ROUTES)
def test_admin_routes_require_token(route):
    response = _request(route)
    assert response.status_code == 403


@pytest.mark.parametrize('route', ROUTES)
def test_admin_routes_reject_query_token(route):
    response = _request(f'{route}?token=test-admin-token')
    assert response.status_code == 403


def test_overview_returns_stats_json():
    response = _request('/admin/overview', headers={'X-Admin-Token': 'test-admin-token'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'stats' in data
    assert data['platform'] == 'OpenLEG'


def test_pipeline_returns_html_when_requested():
    response = _request('/admin/pipeline', headers={'X-Admin-Token': 'test-admin-token', 'Accept': 'text/html'})
    assert response.status_code == 200
    assert b'<html' in response.data


def test_export_supports_json_and_csv():
    json_resp = _request('/admin/export', headers={'X-Admin-Token': 'test-admin-token'})
    assert json_resp.status_code == 200
    assert json_resp.get_json()['count'] == 1

    csv_resp = _request('/admin/export?format=csv', headers={'X-Admin-Token': 'test-admin-token'})
    assert csv_resp.status_code == 200
    assert csv_resp.headers.get('Content-Disposition') == 'attachment; filename=openleg_export.csv'


def test_lea_reports_returns_list():
    response = _request('/admin/lea-reports', headers={'X-Admin-Token': 'test-admin-token'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'reports' in data
    assert len(data['reports']) == 1


def test_pipeline_route_stays_available():
    response = _request('/admin/pipeline', headers={'X-Admin-Token': 'test-admin-token'})
    assert response.status_code == 200
