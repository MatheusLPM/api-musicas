from app.repositories.gravadora_repository import GravadoraRepository


class GravadoraService :
    
    def __init__(self, gravadora_repo : GravadoraRepository):
        self.gravadora_repo = gravadora_repo
        
    def obter_todas_gravadoras(self):
        return self.gravadora_repo.listar_todas()
    
    def obter_gravadora_por_id(self, id):
        return self.gravadora_repo.buscar_por_id(id);
    
    def criar_nova_gravadora(self, dados_artista):
        if not dados_artista.get("nome"):
            raise ValueError("Nome do gravadora é obrigatório.")
        return self.gravadora_repo.adicionar_gravadora(dados_artista)
    
    def atualizar_gravadora_existente(self, id_gravadora, dados_musica):
        musica = self.gravadora_repo.buscar_por_id(id_gravadora)
        if not musica:
            return None
        return self.gravadora_repo.atualizar_gravadora(id_gravadora, dados_musica)
    
    def deletar_gravadora_existente(self, id_gravadora):
        return self.gravadora_repo.deletar_gravadora(id_gravadora)