import unittest
from unittest.mock import MagicMock # Para criar objetos mock
# Precisamos ajustar o sys.path para importar de 'app'
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.service.musica_service import MusicaService
from app.models.musica import Musica # Apenas para criar dados de teste


class TestMusicaService(unittest.TestCase):
    
    def setUp(self):
        # Configurações antes de cada teste
        self.mock_musica_repo = MagicMock() # Cria um mock para o repositório
        self.musica_service = MusicaService(self.mock_musica_repo)
        # Dados de exemplo para os mocks
        self.musica_data = {
            "id": 1,
            "titulo": "Test Song",
            "id_artista": 4,
            "genero": "Pop",
            "ano": 2020,
            "duracao": 200
        }
        
    def test_obter_todas_musicas(self):
        self.mock_musica_repo.listar_todas.return_value = [self.musica_data]
        musicas = self.musica_service.obter_todas_musicas()
        self.assertEqual(len(musicas), 1)
        self.assertEqual(musicas[0]["titulo"], "Test Song")
        self.mock_musica_repo.listar_todas.assert_called_once()
        
    def test_criar_nova_musica_sucesso(self):
        # Configura o mock para retornar a música criada
        self.mock_musica_repo.adicionar_musica.return_value = self.musica_data
        musica_criada = self.musica_service.criar_nova_musica(self.musica_data)
        self.assertIsNotNone(musica_criada)
        self.assertEqual(musica_criada["titulo"], "Test Song")
        self.mock_musica_repo.adicionar_musica.assert_called_once_with(self.musica_data)
        
    def test_criar_nova_musica_campos_obrigatorios_faltando(self):
        # Testar a validação do serviço
        dados_invalidos = {"titulo": "", "artista_nome": "Artista"}
        with self.assertRaises(ValueError) as cm:
            self.musica_service.criar_nova_musica(dados_invalidos)
            self.assertEqual(str(cm.exception), "Título e nome do artista são obrigatórios.")
            self.mock_musica_repo.adicionar_musica.assert_not_called()
    
if __name__ == '__main__':
    unittest.main()