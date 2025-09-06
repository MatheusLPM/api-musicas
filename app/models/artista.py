from app.config.db_config import db

class Artista(db.Model):
    __tablename__ = 'artistas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    nacionalidade = db.Column(db.String(50))
    musicas = db.relationship('Musica', backref='artista', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "nacionalidade": self.nacionalidade
        }
        
    def __repr__(self):
        return f"<Artista {self.nome}>"