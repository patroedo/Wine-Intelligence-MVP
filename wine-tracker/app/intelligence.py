from flask import Blueprint, render_template, request, jsonify
from wine_resolver import resolve

bp=Blueprint('intelligence',__name__)

@bp.get('/intelligence')
def home(): return render_template('intelligence_demo.html')

@bp.post('/api/intelligence/resolve')
def api_resolve():
    from app import get_db
    data=request.get_json(silent=True) or {}; q=(data.get('query') or '').strip()
    if not q:return jsonify({'ok':False,'error':'query_required'}),400
    rows=get_db().execute('SELECT id,name,year,region,grape,vivino_id FROM wines').fetchall()
    result=resolve(q,rows); result.update(ok=True,resolver_version='0.1')
    return jsonify(result)

@bp.get('/api/intelligence/health')
def health(): return jsonify(ok=True,resolver='0.1',apify=False,paid_dependencies=False)
