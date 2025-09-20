from app.config.db_config import db
from app.models.gravadora import Gravadora

class GravadoraRepository:
    def __init__(self):
        pass
            
    def listar_todas(self):
        gravadoras = Gravadora.query.all()
        return [gravadora.to_dict() for gravadora in gravadoras]
    
    def buscar_por_id(self, id):
        gravadora = Gravadora.query.get(id)
        return gravadora.to_dict() if gravadora else None
    
    def adicionar_gravadora(self, dados_gravadora):
        gravadora = Gravadora(
            nome=dados_gravadora["nome"],
            pais_de_origem=dados_gravadora["pais_de_origem"],
            ano_fundacao=dados_gravadora.get("ano_fundacao"),
            site=dados_gravadora.get("site")
        )
        db.session.add(gravadora)
        db.session.commit()
        return gravadora.to_dict()
    
    def atualizar_gravadora(self, id, dados_gravadora): 
        gravadora = Gravadora.query.get(id)
        if gravadora :
            gravadora.nome = dados_gravadora.get("nome", gravadora.nome)
            gravadora.pais_de_origem = dados_gravadora.get("pais_de_origem", gravadora.pais_de_origem)
            gravadora.ano_fundacao = dados_gravadora.get("ano_fundacao", gravadora.ano_fundacao)
            gravadora.site = dados_gravadora.get("site", gravadora.site)
            db.session.commit()
            
            return gravadora.to_dict() 
        return None 

    def deletar_gravadora(self, id):
        gravadora = Gravadora.query.get(id)
        if gravadora:
            db.session.delete(gravadora)
            db.session.commit()
            return True
        return False
