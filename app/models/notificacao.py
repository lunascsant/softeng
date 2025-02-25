from datetime import datetime
from app import mongo
from bson import ObjectId

class Notificacao:
    def __init__(self, titulo, mensagem, usuario_id, tipo, referencia_id=None, grupo_id=None):
        self.titulo = titulo
        self.mensagem = mensagem
        self.usuario_id = usuario_id
        self.tipo = tipo  # tarefa, despesa, sistema
        self.referencia_id = referencia_id  # ID do objeto relacionado (tarefa, despesa)
        self.grupo_id = grupo_id
        self.data_criacao = datetime.utcnow()
        self.lida = False
        self.data_leitura = None
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "referencia_id": self.referencia_id,
            "grupo_id": self.grupo_id,
            "data_criacao": self.data_criacao,
            "lida": self.lida,
            "data_leitura": self.data_leitura
        }
    
    @staticmethod
    def from_dict(data):
        notificacao = Notificacao(
            titulo=data.get("titulo"),
            mensagem=data.get("mensagem"),
            usuario_id=data.get("usuario_id"),
            tipo=data.get("tipo"),
            referencia_id=data.get("referencia_id"),
            grupo_id=data.get("grupo_id")
        )
        return notificacao
    
    @staticmethod
    def find_by_id(notificacao_id):
        notificacao_data = mongo.db.notificacoes.find_one({"_id": ObjectId(notificacao_id)})
        if not notificacao_data:
            return None
        return notificacao_data
    
    @staticmethod
    def find_by_usuario(usuario_id, only_unread=False):
        query = {"usuario_id": usuario_id}
        if only_unread:
            query["lida"] = False
        
        notificacoes = mongo.db.notificacoes.find(query).sort("data_criacao", -1)
        return list(notificacoes)
    
    def save(self):
        notificacao_dict = self.to_dict()
        result = mongo.db.notificacoes.insert_one(notificacao_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def marcar_como_lida(notificacao_id):
        result = mongo.db.notificacoes.update_one(
            {"_id": ObjectId(notificacao_id)},
            {"$set": {"lida": True, "data_leitura": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def marcar_todas_como_lidas(usuario_id):
        result = mongo.db.notificacoes.update_many(
            {"usuario_id": usuario_id, "lida": False},
            {"$set": {"lida": True, "data_leitura": datetime.utcnow()}}
        )
        return result.modified_count
    
    @staticmethod
    def delete(notificacao_id):
        result = mongo.db.notificacoes.delete_one({"_id": ObjectId(notificacao_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def contar_nao_lidas(usuario_id):
        return mongo.db.notificacoes.count_documents({"usuario_id": usuario_id, "lida": False})