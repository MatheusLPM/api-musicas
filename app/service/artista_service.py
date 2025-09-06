from app.repositories.artista_repository import ArtistaRepository


class ArtistaService :
    
    def __init__(self, artista_repo : ArtistaRepository):
        self.artista_repo = artista_repo
        
    def obter_todos_artistas(self):
        return self.artista_repo.listar_todas()
    
    def obter_artista_por_id(self, id):
        return self.artista_repo.buscar_por_id(id);
    
    def criar_novo_artista(self, dados_artista):
        if not dados_artista.get("nome"):
            raise ValueError("Nome do artista é obrigatório.")
        return self.artista_repo.adicionar_artista(dados_artista)
    
    def atualizar_artista_existente(self, id_artista, dados_musica):
        musica = self.artista_repo.buscar_por_id(id_artista)
        if not musica:
            return None
        return self.artista_repo.atualizar_artista(id_artista, dados_musica)
    
    def deletar_artista_existente(self, id_artista):
        return self.artista_repo.deletar_artista(id_artista)