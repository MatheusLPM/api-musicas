from app.config.db_config import db

class Musica(db.Model):
    __tablename__ = 'musicas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    # artista = db.Column(db.String(100), nullable=False)
    id_artista = db.Column(db.String(100), db.ForeignKey('artistas.id'))
    genero = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    duracao = db.Column(db.Integer)
    album = db.Column(db.String(100))
    
    def get_id(self):
        return self.id
    
    def get_titulo(self):
        return self.titulo
    
    def to_dict(self):
        data = {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "ano": self.ano,
            "duracao": self.duracao,
            "id_artista": self.artista.id if self.artista else None,
            "artista_nome": self.artista.nome if self.artista else None
        }
        data["album"] = self.album
        return data
    
    def __repr__(self):
        return f"<Musica {self.titulo} by {self.artista_nome}>"
