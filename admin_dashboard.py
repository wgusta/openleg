"""Admin dashboard blueprint extracted from app routes."""

import csv
import io
import os

from flask import Blueprint, Response, abort, jsonify, render_template, request

import database as db

admin_bp = Blueprint('admin_dashboard', __name__)
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '').strip()


def _require_admin():
    if not ADMIN_TOKEN:
        abort(404)
    token = request.headers.get('X-Admin-Token', '')
    if token != ADMIN_TOKEN:
        abort(403)


@admin_bp.route('/admin/overview')
def admin_overview():
    _require_admin()
    stats = db.get_stats()
    email_stats = db.get_email_stats()
    consented = db.count_consented_buildings()
    municipalities = db.get_all_municipalities()
    return jsonify(
        {
            'platform': 'OpenLEG',
            'stats': stats,
            'email_stats': email_stats,
            'consented_buildings': consented,
            'municipalities': len(municipalities),
        }
    )


@admin_bp.route('/admin/pipeline')
def admin_pipeline():
    _require_admin()
    status_filter = request.args.get('status')
    entries = db.get_vnb_pipeline(status_filter=status_filter)
    stats = db.get_vnb_pipeline_stats()

    if 'text/html' in (request.headers.get('Accept') or ''):
        return render_template('admin/pipeline.html', entries=entries, stats=stats)
    return jsonify({'entries': entries, 'stats': stats})


@admin_bp.route('/admin/export')
def admin_export():
    _require_admin()
    fmt = (request.args.get('format') or 'json').lower()
    city_id = request.args.get('city_id')

    buildings = db.get_all_building_profiles(city_id=city_id)
    if fmt == 'csv':
        output = io.StringIO()
        if buildings:
            writer = csv.DictWriter(output, fieldnames=buildings[0].keys())
            writer.writeheader()
            for row in buildings:
                writer.writerow(row)
        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=openleg_export.csv'
        return response
    return jsonify({'records': buildings, 'count': len(buildings)})


@admin_bp.route('/admin/lea-reports')
def admin_lea_reports():
    _require_admin()
    reports = db.get_lea_reports(limit=50)
    return jsonify({'reports': reports})
