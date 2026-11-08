from flask import Blueprint, request, jsonify, redirect, render_template
from app import db
from app.models import Url
from app.utils import generate_short_code, is_valid_url

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    """Gère l'affichage de la page et le formulaire HTML directement côté serveur."""
    short_url = None
    error = None

    if request.method == 'POST':
        long_url = request.form.get('long_url', '').strip()
        
        if not long_url:
            error = "Veuillez saisir une URL."
        elif not is_valid_url(long_url):
            error = "URL invalide. Elle doit commencer par http:// ou https://"
        else:
            existing_url = Url.query.filter_by(original_url=long_url).first()
            if existing_url:
                short_url = f"{request.host_url}{existing_url.short_code}"
            else:
                short_code = generate_short_code()
                new_url = Url(original_url=long_url, short_code=short_code)
                db.session.add(new_url)
                db.session.commit()
                short_url = f"{request.host_url}{short_code}"

    return render_template('index.html', short_url=short_url, error=error)

@main_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Endpoint API JSON."""
    data = request.get_json(silent=True)
    if not data or 'long_url' not in data:
        return jsonify({"error": "Le champ 'long_url' est requis."}), 400
    
    long_url = data['long_url'].strip()
    if not is_valid_url(long_url):
        return jsonify({"error": "URL invalide. Elle doit commencer par http:// ou https://"}), 400
    
    existing_url = Url.query.filter_by(original_url=long_url).first()
    if existing_url:
        return jsonify(existing_url.to_dict(request.host_url)), 200
    
    short_code = generate_short_code()
    new_url = Url(original_url=long_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    
    return jsonify(new_url.to_dict(request.host_url)), 201

@main_bp.route('/<string:short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirige le code court vers l'URL longue."""
    url_entry = Url.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({"error": "Ce lien court n'existe pas."}), 404
    
    url_entry.clicks += 1
    db.session.commit()
    return redirect(url_entry.original_url, code=302)