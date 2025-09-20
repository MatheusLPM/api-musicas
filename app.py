# iniciar aplicação -> source /opt/projeto-api-musica/venv/bin/activate

from urllib.parse import quote_plus
from flask import Flask, jsonify, request

# from app.config.db_config import db
from app.config.db_config import db, db_manager

from app.repositories.musica_repository import MusicaRepository
from app.repositories.artista_repository import ArtistaRepository
from app.repositories.gravadora_repository import GravadoraRepository
from app.models.musica import Musica 
from app.service.musica_service import MusicaService
from app.service.artista_service import ArtistaService
from app.service.gravadora_service import GravadoraService

app = Flask(__name__)

# ---------------------------------------------------------------------------------------------
user = "root"
password = quote_plus("@mysql")
host = "localhost"
port = 3306
database = "apimusica"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_manager.init_app(app)

# db.init_app(app)
# ---------------------------------------------------------------------------------------------

musica_repo = MusicaRepository()
musica_service = MusicaService(musica_repo)

artista_repo = ArtistaRepository()
artista_service = ArtistaService(artista_repo)

gravadora_repo = GravadoraRepository()
gravadora_service = GravadoraService(gravadora_repo)


# @app.route("/musicas", methods=["GET"])
# def get_musicas():
#     musicas = musica_service.obter_todas_musicas()
#     return jsonify(musicas), 200

@app.route("/musicas", methods=["GET"])
def get_musicas():
    titulo = request.args.get("titulo")
    id_artista = request.args.get("id_artista")
    genero = request.args.get("genero")
    album = request.args.get("album")
    ano = request.args.get("ano", type=int)
    pagina = request.args.get("pagina", 1, type=int)
    limite = request.args.get("limite", 10, type=int)
    musicas = musica_service.obter_todas_musicas(
        titulo=titulo,
        id_artista=id_artista,
        genero=genero,
        ano=ano,
        pagina=pagina,
        limite=limite,
        album=album
    )
    return jsonify(musicas)

@app.route("/musicas/gravadora/<int:id_gravadora>", methods=["GET"])
def get_musicas_by_gravadora(id_gravadora):
    musica = musica_service.get_musicas_by_gravadora(id_gravadora)
    if musica:
        return jsonify(musica), 200
    return jsonify({"erro": "Músicas não encontrada"}), 404

@app.route("/musicas/<int:id>", methods=["GET"])
def get_musica_by_id(id):
    musica = musica_service.obter_musica_por_id(id)
    if musica:
        return jsonify(musica), 200
    return jsonify({"erro": "Música não encontrada"}), 404

@app.route("/musicas", methods=["POST"])
def create_musica():
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados inválidos"}), 400
    required_fields = ["titulo", "id_artista", "genero", "ano", "duracao"]
    if not all(field in dados for field in required_fields):
        return jsonify({"message": "Campos obrigatórios faltando"}), 400
    if not dados.get("titulo") or not dados.get("id_artista"):
        return jsonify({"message": "Título e Artista não podem ser vazios"}), 400
    try:
        musica_criada = musica_service.criar_nova_musica(dados)
        return jsonify(musica_criada), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar música: {e}")
        return jsonify({"message": "Erro interno ao criar música"}), 500

@app.route("/musicas/<int:id>", methods=["PUT"])
def update_musica(id):
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados inválidos"}), 400
    try:
        musica_atualizada = musica_service.atualizar_musica_existente(id, dados)
        if musica_atualizada:
            return jsonify(musica_atualizada)
        return jsonify({"message": "Música não encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar música: {e}")
        return jsonify({"message": "Erro interno ao atualizar música"}), 500

@app.route("/musicas/<int:id>", methods=["DELETE"])
def delete_musica(id):
    try:
        if musica_service.deletar_musica_existente(id):
            return jsonify({"message": "Música deletada com sucesso"}), 200
        return jsonify({"message": "Música não encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar música: {e}")
        return jsonify({"message": "Erro interno ao deletar música"}), 500
    
    
    
@app.route("/artista", methods=["POST"])
def create_artista():
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados inválidos"}), 400
    required_fields = ["nome", "nacionalidade"]
    if not all(field in dados for field in required_fields):
        return jsonify({"message": "Campos obrigatórios faltando"}), 400
    if not dados.get("nome") or not dados.get("nacionalidade"):
        return jsonify({"message": "Nome e Nacionalidade não podem ser vazios"}), 400
    try:
        artista_repo_criada = artista_service.criar_novo_artista(dados)
        return jsonify(artista_repo_criada), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar artista: {e}")
        return jsonify({"message": "Erro interno ao criar artista"}), 500
    
@app.route("/artista", methods=["GET"])
def get_artistas():
    artistas = artista_service.obter_todos_artistas()
    return jsonify(artistas), 200


@app.route("/gravadora", methods=["POST"])
def create_gravadora():
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados inválidos"}), 400
    required_fields = ["nome", "pais_de_origem"]
    if not all(field in dados for field in required_fields):
        return jsonify({"message": "Campos obrigatórios faltando"}), 400
    if not dados.get("pais_de_origem"):
        return jsonify({"message": "País de Origem é obrigatório"}), 400
    if not dados.get("nome"):
        return jsonify({"message": "Nome do gravadora é obrigatório"}), 400
    try:
        gravadora_criada = gravadora_service.criar_nova_gravadora(dados)
        return jsonify(gravadora_criada), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar gravadora: {e}")
        return jsonify({"message": "Erro interno ao criar gravadora"}), 500


@app.route("/gravadora", methods=["GET"])
def get_gravadoras():
    gravadoras = gravadora_service.obter_todas_gravadoras()
    return jsonify(gravadoras), 200

@app.route("/gravadora/<int:id>", methods=["PUT"])
def update_gravadora(id):
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados inválidos"}), 400
    if not dados.get("nome"):
        return jsonify({"message": "Nome do gravadora é obrigatório"}), 400
    if not dados.get("pais_de_origem"):
        return jsonify({"message": "País de Origem é obrigatório"}), 400
    try:
        gravadora_atualizada = gravadora_service.atualizar_gravadora_existente(id, dados)
        if gravadora_atualizada:
            return jsonify(gravadora_atualizada)
        return jsonify({"message": "Gravadora não encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar gravadora: {e}")
        return jsonify({"message": "Erro interno ao atualizar gravadora"}), 500

@app.route("/gravadora/<int:id>", methods=["DELETE"])
def delete_gravadora(id):
    try:
        if gravadora_service.deletar_gravadora_existente(id):
            return jsonify({"message": "Gravadora deletada com sucesso"}), 200
        return jsonify({"message": "Gravadora não encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar gravadora: {e}")
        return jsonify({"message": "Erro interno ao deletar gravadora"}), 500

if __name__ == "__main__":
    with app.app_context():
        db_manager.db.create_all()
    app.run(debug=True)
