from datetime import datetime, timezone
from app import db

class Url(db.Model):
    """Modèle représentant une URL raccourcie dans la base SQLite."""
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self, base_url=""):
        """Sérialise l'objet en dictionnaire pour les réponses JSON de l'API."""
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "short_url": f"{base_url}{self.short_code}",
            "clicks": self.clicks,
            "created_at": self.created_at.isoformat()
        }