from app.models.relatorio import Relatorio
from app.models.grupo_republica import GrupoRepublica
from app.models.usuario import Usuario
from flask import jsonify, request
from bson import ObjectId
from datetime import datetime

class RelatorioController:
    @staticmethod
    def criar_relatorio():
        data = request.get_json()
        
        # Verificar se o grupo existe
        grupo_id = data.get("grupo_id")
        grupo = GrupoRepublica.find_by_id(grupo_id)
        if not grupo:
            return jsonify({"error": "Grupo não encontrado"}), 404
        
        # Verificar se o usuário existe e pertence ao grupo
        criado_por = data.get("criado_por")
        usuario = Usuario.find_by_id(criado_por)
        if not usuario or usuario.get("grupo_id") != grupo_id:
            return jsonify({"error": "Usuário não encontrado no grupo"}), 404
        
        # Criar novo relatório
        try:
            relatorio = Relatorio.from_dict(data)
            relatorio_id = relatorio.save()
            
            return jsonify({
                "message": "Relatório criado com sucesso",
                "relatorio_id": relatorio_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_relatorio(relatorio_id):
        try:
            relatorio = Relatorio.find_by_id(relatorio_id)
            if not relatorio:
                return jsonify({"error": "Relatório não encontrado"}), 404
            
            return jsonify(relatorio), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_relatorio(relatorio_id):
        try:
            # Verificar se o relatório existe
            relatorio = Relatorio.find_by_id(relatorio_id)
            if not relatorio:
                return jsonify({"error": "Relatório não encontrado"}), 404
            
            # Deletar relatório
            success = Relatorio.delete(relatorio_id)
            if success:
                return jsonify({"message": "Relatório deletado com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao deletar relatório"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_relatorios_por_grupo(grupo_id):
        try:
            relatorios = Relatorio.find_by_grupo(grupo_id)
            return jsonify(relatorios), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def gerar_relatorio_financeiro(grupo_id):
        try:
            # Extrair parâmetros da query string
            periodo_inicio = request.args.get('inicio')
            periodo_fim = request.args.get('fim')
            
            # Converter para datetime se fornecido
            if periodo_inicio:
                periodo_inicio = datetime.fromisoformat(periodo_inicio)
            if periodo_fim:
                periodo_fim = datetime.fromisoformat(periodo_fim)
            
            resultado = Relatorio.gerar_relatorio_financeiro(grupo_id, periodo_inicio, periodo_fim)
            
            # Criar registro do relatório no banco
            titulo = f"Relatório Financeiro - {datetime.utcnow().strftime('%d/%m/%Y')}"
            relatorio = Relatorio(
                titulo=titulo,
                grupo_id=grupo_id,
                tipo="financeiro",
                criado_por=request.args.get('criado_por'),
                periodo_inicio=periodo_inicio,
                periodo_fim=periodo_fim
            )
            relatorio_id = relatorio.save()
            
            # Adicionar ID do relatório ao resultado
            resultado["relatorio_id"] = relatorio_id
            
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500