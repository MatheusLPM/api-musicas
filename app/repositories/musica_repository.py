from app.models.musica import Musica
from app.config.db_config import db
from app.models.artista import Artista
from app.models.gravadora import Gravadora
from sqlalchemy import and_

class MusicaRepository:
    def __init__(self):
        pass
    
    def listar_todas(self, titulo=None, id_artista=None, genero=None, ano=None, pagina=1, limite=10, album=None, id_gravadora=None):
        query = Musica.query
        if titulo:
            query = query.filter(Musica.titulo.ilike(f"%{titulo}%")) 
        if id_artista:
            query = query.filter(Musica.id_artista==id_artista)
        if id_gravadora:
            query = query.filter(Musica.id_gravadora==id_gravadora)
        if genero:
            query = query.filter_by(genero=genero)
        if ano:
            query = query.filter_by(ano=ano)
        if album:
            query = query.filter_by(Musica.album.ilike(f"%{album}%"))
        musicas = query.order_by(Musica.titulo).paginate(
            page=pagina,
            per_page=limite,
            error_out=False,
            count=True
        ).items
        # musicas = query.all()
        return [musica.to_dict() for musica in musicas]
    
    def listar_todas_gravadora(self, id_gravadora):
        query = Musica.query
        if id_gravadora:
            query = query.filter(Musica.id_gravadora==id_gravadora)
        musicas = query.order_by(Musica.titulo).all()
        return [musica.to_dict() for musica in musicas]
    
    def buscar_por_id(self, id):
        musica = Musica.query.get(id)
        return musica.to_dict() if musica else None
    
    def adicionar_musica(self, dados_musica):
        artista = Artista.query.get(dados_musica['id_artista'])
        gravadora = Gravadora.query.get(dados_musica['id_gravadora'])
        musica = Musica(
            titulo=dados_musica["titulo"],
            genero=dados_musica.get("genero"),
            ano=dados_musica.get("ano"),
            duracao=dados_musica.get("duracao"),
            album=dados_musica.get("album"),
            id_artista=artista.id,
            id_gravadora=gravadora.id
        )
        db.session.add(musica)
        db.session.commit()
        return musica.to_dict()
    
    def atualizar_musica(self, id, dados_musica): 
        musica = Musica.query.get(id)
        if musica :
            musica.titulo = dados_musica.get("titulo", musica.titulo)
            musica.artista = dados_musica.get("artista", musica.artista)
            musica.genero = dados_musica.get("genero", musica.genero)
            musica.ano = dados_musica.get("ano", musica.ano)
            musica.duracao = dados_musica.get("duracao", musica.duracao)
            musica.album = dados_musica.get("album", musica.album)
            db.session.commit()
            
            return musica.to_dict() 
        return None 

    def deletar_musica(self, id):
        musica = Musica.query.get(id)
        if musica:
            db.session.delete(musica)
            db.session.commit()
            return True
        return False
