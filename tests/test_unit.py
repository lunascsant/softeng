import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from bson import ObjectId
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from app.models.tarefa import Tarefa
from app.models.despesa import Despesa

class TestModelUsuario(unittest.TestCase):
    """
    Teste unitário para o modelo de Usuário
    """
    
    def setUp(self):
        # Configuração inicial para cada teste
        self.usuario_data = {
            "nome": "Teste Unitário",
            "email": "teste@unitario.com",
            "telefone": "31999999999",
            "senha": "senha123",
            "tipo": "padrao"
        }
        
    @patch('app.models.usuario.mongo')
    def test_criacao_usuario(self, mock_mongo):
        # Configurar o mock para simular a inserção no banco
        mock_inserted_id = ObjectId()
        mock_mongo.db.usuarios.insert_one.return_value.inserted_id = mock_inserted_id
        
        # Criar um usuário
        usuario = Usuario.from_dict(self.usuario_data)
        
        # Verificar se o objeto foi criado corretamente
        self.assertEqual(usuario.nome, "Teste Unitário")
        self.assertEqual(usuario.email, "teste@unitario.com")
        self.assertEqual(usuario.telefone, "31999999999")
        self.assertEqual(usuario.tipo, "padrao")
        
        # Verificar se a senha foi hasheada
        self.assertNotEqual(usuario.senha_hash, "senha123")
        
        # Testar o método de salvar
        usuario_id = usuario.save()
        
        # Verificar se o método insert_one foi chamado
        mock_mongo.db.usuarios.insert_one.assert_called_once()
        
        # Verificar se o ID retornado é o esperado
        self.assertEqual(usuario_id, str(mock_inserted_id))
    
    @patch('app.models.usuario.mongo')
    def test_verificacao_senha(self, mock_mongo):
        # Criar um usuário
        usuario = Usuario.from_dict(self.usuario_data)
        
        # Testar verificação de senha correta
        self.assertTrue(usuario.verificar_senha("senha123"))
        
        # Testar verificação de senha incorreta
        self.assertFalse(usuario.verificar_senha("senha_errada"))
    
    @patch('app.models.usuario.mongo')
    def test_busca_usuario_por_email(self, mock_mongo):
        # Configurar o mock para retornar um usuário simulado
        mock_usuario = {
            "_id": ObjectId(),
            "nome": "Teste Unitário",
            "email": "teste@unitario.com",
            "telefone": "31999999999",
            "tipo": "padrao",
            "senha_hash": "hash_da_senha"
        }
        mock_mongo.db.usuarios.find_one.return_value = mock_usuario
        
        # Testar busca por email
        resultado = Usuario.find_by_email("teste@unitario.com")
        
        # Verificar se o método find_one foi chamado com o parâmetro correto
        mock_mongo.db.usuarios.find_one.assert_called_with({"email": "teste@unitario.com"})
        
        # Verificar se o resultado é o esperado
        self.assertEqual(resultado, mock_usuario)

class TestModelTarefa(unittest.TestCase):
    """
    Teste unitário para o modelo de Tarefa
    """
    
    def setUp(self):
        # Configuração inicial para cada teste
        self.tarefa_data = {
            "titulo": "Limpar a cozinha",
            "descricao": "Lavar louça, limpar fogão e bancadas",
            "grupo_id": "6123456789abcdef12345679",
            "responsavel_id": "6123456789abcdef12345678",
            "prazo": datetime.fromisoformat("2025-03-01T12:00:00"),
            "prioridade": "media"
        }
        
    @patch('app.models.tarefa.mongo')
    def test_criacao_tarefa(self, mock_mongo):
        # Configurar o mock para simular a inserção no banco
        mock_inserted_id = ObjectId()
        mock_mongo.db.tarefas.insert_one.return_value.inserted_id = mock_inserted_id
        
        # Criar uma tarefa
        tarefa = Tarefa.from_dict(self.tarefa_data)
        
        # Verificar se o objeto foi criado corretamente
        self.assertEqual(tarefa.titulo, "Limpar a cozinha")
        self.assertEqual(tarefa.descricao, "Lavar louça, limpar fogão e bancadas")
        self.assertEqual(tarefa.grupo_id, "6123456789abcdef12345679")
        self.assertEqual(tarefa.responsavel_id, "6123456789abcdef12345678")
        self.assertEqual(tarefa.prioridade, "media")
        self.assertEqual(tarefa.status, "pendente")  # Status inicial padrão
        
        # Testar o método de salvar
        tarefa_id = tarefa.save()
        
        # Verificar se o método insert_one foi chamado
        mock_mongo.db.tarefas.insert_one.assert_called_once()
        
        # Verificar se o ID retornado é o esperado
        self.assertEqual(tarefa_id, str(mock_inserted_id))
    
    @patch('app.models.tarefa.mongo')
    def test_atualizacao_tarefa(self, mock_mongo):
        # Configurar o mock para simular a atualização no banco
        mock_mongo.db.tarefas.update_one.return_value.modified_count = 1
        
        # Definir um ID de tarefa para testar
        tarefa_id = "6123456789abcdef12345681"
        
        # Definir dados para atualização
        update_data = {
            "status": "concluida",
            "descricao": "Descrição atualizada"
        }
        
        # Testar o método de atualização
        success = Tarefa.update(tarefa_id, update_data)
        
        # Verificar se o método update_one foi chamado com os parâmetros corretos
        mock_mongo.db.tarefas.update_one.assert_called_with(
            {"_id": ObjectId(tarefa_id)},
            {"$set": {
                "status": "concluida", 
                "descricao": "Descrição atualizada",
                "data_conclusao": unittest.mock.ANY  # Verificar que qualquer data foi passada
            }}
        )
        
        # Verificar se o resultado é o esperado
        self.assertTrue(success)
        
    @patch('app.models.tarefa.mongo')
    def test_listar_tarefas_proximas(self, mock_mongo):
        # Configurar o mock para retornar tarefas simuladas
        mock_mongo.db.tarefas.find.return_value.sort.return_value = [
            {
                "_id": ObjectId(),
                "titulo": "Tarefa Próxima 1",
                "prazo": datetime.now()
            },
            {
                "_id": ObjectId(),
                "titulo": "Tarefa Próxima 2",
                "prazo": datetime.now()
            }
        ]
        
        # Testar listagem de tarefas próximas
        grupo_id = "6123456789abcdef12345679"
        dias = 7
        resultado = Tarefa.listar_tarefas_proximas(grupo_id, dias)
        
        # Verificar se o método find foi chamado
        mock_mongo.db.tarefas.find.assert_called_once()
        
        # Verificar se o sort foi chamado
        mock_mongo.db.tarefas.find.return_value.sort.assert_called_with("prazo", 1)
        
        # Verificar se retornou uma lista
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)

class TestModelDespesa(unittest.TestCase):
    """
    Teste unitário para o modelo de Despesa
    """
    
    def setUp(self):
        # Configuração inicial para cada teste
        self.despesa_data = {
            "titulo": "Compras do mês",
            "valor": 350.75,
            "grupo_id": "6123456789abcdef12345679",
            "registrado_por": "6123456789abcdef12345678",
            "categoria": "alimentacao",
            "participantes": ["6123456789abcdef12345678", "6123456789abcdef12345680"],
            "descricao": "Compras de supermercado"
        }
        
    @patch('app.models.despesa.mongo')
    def test_criacao_despesa(self, mock_mongo):
        # Configurar o mock para simular a inserção no banco
        mock_inserted_id = ObjectId()
        mock_mongo.db.despesas.insert_one.return_value.inserted_id = mock_inserted_id
        
        # Criar uma despesa
        despesa = Despesa.from_dict(self.despesa_data)
        
        # Verificar se o objeto foi criado corretamente
        self.assertEqual(despesa.titulo, "Compras do mês")
        self.assertEqual(despesa.valor, 350.75)
        self.assertEqual(despesa.grupo_id, "6123456789abcdef12345679")
        self.assertEqual(despesa.categoria, "alimentacao")
        self.assertEqual(len(despesa.participantes), 2)
        self.assertEqual(despesa.status, "pendente")  # Status inicial padrão
        
        # Testar o método de salvar
        despesa_id = despesa.save()
        
        # Verificar se o método insert_one foi chamado
        mock_mongo.db.despesas.insert_one.assert_called_once()
        
        # Verificar se o ID retornado é o esperado
        self.assertEqual(despesa_id, str(mock_inserted_id))
    
    @patch('app.models.despesa.mongo')
    def test_calcular_valor_por_participante(self, mock_mongo):
        # Configurar o mock para retornar uma despesa simulada
        mock_despesa = {
            "_id": ObjectId(),
            "titulo": "Compras do mês",
            "valor": 350.75,
            "participantes": ["user1", "user2", "user3", "user4", "user5"]
        }
        mock_mongo.db.despesas.find_one.return_value = mock_despesa
        
        # Testar o cálculo do valor por participante
        despesa_id = "6123456789abcdef12345682"
        valor_por_participante = Despesa.calcular_valor_por_participante(despesa_id)
        
        # Verificar se o método find_one foi chamado com o parâmetro correto
        mock_mongo.db.despesas.find_one.assert_called_with({"_id": ObjectId(despesa_id)})
        
        # Verificar se o resultado é o esperado (350.75 / 5 = 70.15)
        self.assertAlmostEqual(valor_por_participante, 70.15, places=2)
    
    @patch('app.models.despesa.mongo')
    def test_obter_total_por_categoria(self, mock_mongo):
        # Configurar o mock para retornar um resultado simulado
        mock_resultado = [
            {"_id": "alimentacao", "total": 1250.50},
            {"_id": "limpeza", "total": 450.30},
            {"_id": "internet", "total": 120.00}
        ]
        mock_mongo.db.despesas.aggregate.return_value = mock_resultado
        
        # Testar a obtenção de total por categoria
        grupo_id = "6123456789abcdef12345679"
        resultado = Despesa.obter_total_por_categoria(grupo_id)
        
        # Verificar se o método aggregate foi chamado
        mock_mongo.db.despesas.aggregate.assert_called_once()
        
        # Verificar se o resultado é o esperado
        self.assertEqual(resultado, mock_resultado)
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[0]["_id"], "alimentacao")
        self.assertEqual(resultado[0]["total"], 1250.50)

if __name__ == '__main__':
    unittest.main()