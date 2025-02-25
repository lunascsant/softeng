from datetime import datetime
from app import mongo
from bson import ObjectId

class Relatorio:
    def __init__(self, titulo, grupo_id, tipo, criado_por, periodo_inicio=None, periodo_fim=None, parametros=None):
        self.titulo = titulo
        self.grupo_id = grupo_id
        self.tipo = tipo  # financeiro, tarefas, atividades
        self.criado_por = criado_por
        self.data_criacao = datetime.utcnow()
        self.periodo_inicio = periodo_inicio
        self.periodo_fim = periodo_fim or datetime.utcnow()
        self.parametros = parametros or {}  # parâmetros adicionais para o relatório
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "grupo_id": self.grupo_id,
            "tipo": self.tipo,
            "criado_por": self.criado_por,
            "data_criacao": self.data_criacao,
            "periodo_inicio": self.periodo_inicio,
            "periodo_fim": self.periodo_fim,
            "parametros": self.parametros
        }
    
    @staticmethod
    def from_dict(data):
        relatorio = Relatorio(
            titulo=data.get("titulo"),
            grupo_id=data.get("grupo_id"),
            tipo=data.get("tipo"),
            criado_por=data.get("criado_por"),
            periodo_inicio=data.get("periodo_inicio"),
            periodo_fim=data.get("periodo_fim"),
            parametros=data.get("parametros")
        )
        return relatorio
    
    @staticmethod
    def find_by_id(relatorio_id):
        relatorio_data = mongo.db.relatorios.find_one({"_id": ObjectId(relatorio_id)})
        if not relatorio_data:
            return None
        return relatorio_data
    
    @staticmethod
    def find_by_grupo(grupo_id):
        relatorios = mongo.db.relatorios.find({"grupo_id": grupo_id})
        return list(relatorios)
    
    def save(self):
        relatorio_dict = self.to_dict()
        result = mongo.db.relatorios.insert_one(relatorio_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def delete(relatorio_id):
        result = mongo.db.relatorios.delete_one({"_id": ObjectId(relatorio_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def gerar_relatorio_financeiro(grupo_id, periodo_inicio=None, periodo_fim=None):
        match_query = {"grupo_id": grupo_id}
        
        if periodo_inicio or periodo_fim:
            match_query["data_despesa"] = {}
            if periodo_inicio:
                match_query["data_despesa"]["$gte"] = periodo_inicio
            if periodo_fim:
                match_query["data_despesa"]["$lte"] = periodo_fim
        
        pipeline = [
            {"$match": match_query},
            {"$group": {
                "_id": "$categoria",
                "total": {"$sum": "$valor"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"total": -1}}
        ]
        
        resultado_categorias = list(mongo.db.despesas.aggregate(pipeline))
        
        # Total geral
        pipeline_total = [
            {"$match": match_query},
            {"$group": {
                "_id": None,
                "total": {"$sum": "$valor"},
                "count": {"$sum": 1}
            }}
        ]
        
        resultado_total = list(mongo.db.despesas.aggregate(pipeline_total))
        
        return {
            "categorias": resultado_categorias,
            "total": resultado_total[0] if resultado_total else {"total": 0, "count": 0}
        }