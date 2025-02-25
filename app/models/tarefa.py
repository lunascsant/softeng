from datetime import datetime, timedelta
from app import mongo
from bson import ObjectId

class Tarefa:
    def __init__(self, titulo, descricao, grupo_id, responsavel_id, prazo=None, prioridade="media"):
        self.titulo = titulo
        self.descricao = descricao
        self.grupo_id = grupo_id
        self.responsavel_id = responsavel_id
        self.prazo = prazo
        self.prioridade = prioridade  # baixa, media, alta
        self.status = "pendente"  # pendente, em_andamento, concluida
        self.data_criacao = datetime.utcnow()
        self.data_conclusao = None
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "grupo_id": self.grupo_id,
            "responsavel_id": self.responsavel_id,
            "prazo": self.prazo,
            "prioridade": self.prioridade,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "data_conclusao": self.data_conclusao
        }
    
    @staticmethod
    def from_dict(data):
        tarefa = Tarefa(
            titulo=data.get("titulo"),
            descricao=data.get("descricao"),
            grupo_id=data.get("grupo_id"),
            responsavel_id=data.get("responsavel_id"),
            prazo=data.get("prazo"),
            prioridade=data.get("prioridade", "media")
        )
        return tarefa
    
    @staticmethod
    def find_by_id(tarefa_id):
        tarefa_data = mongo.db.tarefas.find_one({"_id": ObjectId(tarefa_id)})
        if not tarefa_data:
            return None
        return tarefa_data
    
    @staticmethod
    def find_by_grupo(grupo_id):
        tarefas = mongo.db.tarefas.find({"grupo_id": grupo_id})
        return list(tarefas)
    
    @staticmethod
    def find_by_responsavel(responsavel_id):
        tarefas = mongo.db.tarefas.find({"responsavel_id": responsavel_id})
        return list(tarefas)
    
    def save(self):
        tarefa_dict = self.to_dict()
        result = mongo.db.tarefas.insert_one(tarefa_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def update(tarefa_id, update_data):
        if update_data.get("status") == "concluida" and "data_conclusao" not in update_data:
            update_data["data_conclusao"] = datetime.utcnow()
            
        result = mongo.db.tarefas.update_one(
            {"_id": ObjectId(tarefa_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(tarefa_id):
        result = mongo.db.tarefas.delete_one({"_id": ObjectId(tarefa_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def listar_tarefas_proximas(grupo_id, dias=7):
        data_limite = datetime.utcnow() + timedelta(days=dias)
        tarefas = mongo.db.tarefas.find({
            "grupo_id": grupo_id,
            "prazo": {"$lte": data_limite},
            "status": {"$ne": "concluida"}
        }).sort("prazo", 1)
        return list(tarefas)