from app.config.db_config import db
from app.models.artista import Artista

class ArtistaRepository:
    def __init__(self):
        pass
            
    def listar_todas(self):
        artistas = Artista.query.all()
        return [artista.to_dict() for artista in artistas]
    
    def buscar_por_id(self, id):
        artista = Artista.query.get(id)
        return artista.to_dict() if artista else None
    
    def adicionar_artista(self, dados_artista):
        artista = Artista(
            nome=dados_artista["nome"],
            nacionalidade=dados_artista["nacionalidade"]
        )
        db.session.add(artista)
        db.session.commit()
        return artista.to_dict()
    
    def atualizar_artista(self, id, dados_artista): 
        artista = Artista.query.get(id)
        if artista :
            artista.nome = dados_artista.get("nome", artista.nome)
            artista.nacionalidade = dados_artista.get("nacionalidade", artista.nacionalidade)
            db.session.commit()
            
            return artista.to_dict() 
        return None 

    def deletar_artista(self, id):
        artista = Artista.query.get(id)
        if artista:
            db.session.delete(artista)
            db.session.commit()
            return True
        return False
