import string
import random
from urllib.parse import urlparse
from app.models import Url

def generate_short_code(length=6):
    """Génère un code alphanumérique unique qui n'existe pas encore en base."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        # Vérifie dans la base que ce code n'est pas déjà pris
        if not Url.query.filter_by(short_code=code).first():
            return code

def is_valid_url(url):
    """Vérifie que la chaîne est bien une URL valide commençant par http:// ou https://."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False