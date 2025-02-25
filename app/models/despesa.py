from datetime import datetime
from app import mongo
from bson import ObjectId

class Despesa:
    def __init__(self, titulo, valor, grupo_id, registrado_por, categoria, participantes, descricao=None, data_despesa=None):
        self.titulo = titulo
        self.valor = float(valor)
        self.grupo_id = grupo_id
        self.registrado_por = registrado_por
        self.categoria = categoria
        self.participantes = participantes  # Lista de IDs de usuários que dividirão a despesa
        self.descricao = descricao
        self.data_despesa = data_despesa or datetime.utcnow()
        self.data_registro = datetime.utcnow()
        self.status = "pendente"  # pendente, pago
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "valor": self.valor,
            "grupo_id": self.grupo_id,
            "registrado_por": self.registrado_por,
            "categoria": self.categoria,
            "participantes": self.participantes,
            "descricao": self.descricao,
            "data_despesa": self.data_despesa,
            "data_registro": self.data_registro,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        despesa = Despesa(
            titulo=data.get("titulo"),
            valor=data.get("valor"),
            grupo_id=data.get("grupo_id"),
            registrado_por=data.get("registrado_por"),
            categoria=data.get("categoria"),
            participantes=data.get("participantes", []),
            descricao=data.get("descricao"),
            data_despesa=data.get("data_despesa")
        )
        return despesa
    
    @staticmethod
    def find_by_id(despesa_id):
        despesa_data = mongo.db.despesas.find_one({"_id": ObjectId(despesa_id)})
        if not despesa_data:
            return None
        return despesa_data
    
    @staticmethod
    def find_by_grupo(grupo_id):
        despesas = mongo.db.despesas.find({"grupo_id": grupo_id})
        return list(despesas)
    
    @staticmethod
    def find_by_participante(usuario_id):
        despesas = mongo.db.despesas.find({"participantes": usuario_id})
        return list(despesas)
    
    @staticmethod
    def find_by_categoria(grupo_id, categoria):
        despesas = mongo.db.despesas.find({"grupo_id": grupo_id, "categoria": categoria})
        return list(despesas)
    
    def save(self):
        despesa_dict = self.to_dict()
        result = mongo.db.despesas.insert_one(despesa_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def update(despesa_id, update_data):
        result = mongo.db.despesas.update_one(
            {"_id": ObjectId(despesa_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(despesa_id):
        result = mongo.db.despesas.delete_one({"_id": ObjectId(despesa_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def calcular_valor_por_participante(despesa_id):
        despesa = Despesa.find_by_id(despesa_id)
        if not despesa:
            return None
        
        num_participantes = len(despesa.get("participantes", []))
        if num_participantes == 0:
            return 0
        
        return despesa.get("valor", 0) / num_participantes
    
    @staticmethod
    def obter_total_por_categoria(grupo_id):
        pipeline = [
            {"$match": {"grupo_id": grupo_id}},
            {"$group": {
                "_id": "$categoria",
                "total": {"$sum": "$valor"}
            }}
        ]
        resultado = mongo.db.despesas.aggregate(pipeline)
        return list(resultado)