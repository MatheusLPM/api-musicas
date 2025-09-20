from app.config.db_config import db

class Gravadora(db.Model):
    __tablename__ = 'gravadora'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    pais_de_origem = db.Column(db.String(50))
    ano_fundacao = db.Column(db.Integer, nullable=True)
    site = db.Column(db.String(100), nullable=True)
    musicas = db.relationship("Musica", back_populates="gravadora")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "pais_de_origem": self.pais_de_origem,
            "ano_fundacao": self.ano_fundacao,
            "site": self.site
        }
        
    def __repr__(self):
        return f"<Gravadora {self.nome}>"