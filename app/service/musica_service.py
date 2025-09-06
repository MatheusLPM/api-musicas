from app.repositories.musica_repository import MusicaRepository


class MusicaService:
    
    def __init__(self, musica_repository: MusicaRepository):
        self.musica_repo = musica_repository

    def obter_todas_musicas(self, titulo=None, id_artista=None, genero=None, ano=None, pagina=None, limite=None, album=None):
        return self.musica_repo.listar_todas(
            titulo=titulo,
            id_artista=id_artista,
            genero=genero,
            ano=ano,
            pagina=pagina,
            limite=limite,
            album=album
        )

    def obter_musica_por_id(self, musica_id):
        return self.musica_repo.buscar_por_id(musica_id)

    def criar_nova_musica(self, dados_musica):
        if not dados_musica.get("titulo") or not dados_musica.get("id_artista"):
            raise ValueError("Título e artista são obrigatórios.")
        return self.musica_repo.adicionar_musica(dados_musica)
    
    def atualizar_musica_existente(self, musica_id, dados_musica):
        musica = self.musica_repo.buscar_por_id(musica_id)
        if not musica:
            return None
        return self.musica_repo.atualizar_musica(musica_id, dados_musica)
    
    def deletar_musica_existente(self, musica_id):
        return self.musica_repo.deletar_musica(musica_id)