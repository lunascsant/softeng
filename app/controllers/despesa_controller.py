from app.models.despesa import Despesa
from app.models.usuario import Usuario
from app.models.grupo_republica import GrupoRepublica
from app.models.notificacao import Notificacao
from flask import jsonify, request
from bson import ObjectId
from datetime import datetime

class DespesaController:
    @staticmethod
    def criar_despesa():
        data = request.get_json()
        
        # Verificar se o grupo existe
        grupo_id = data.get("grupo_id")
        grupo = GrupoRepublica.find_by_id(grupo_id)
        if not grupo:
            return jsonify({"error": "Grupo não encontrado"}), 404
        
        # Verificar se o usuário que registrou existe e pertence ao grupo
        registrado_por = data.get("registrado_por")
        usuario = Usuario.find_by_id(registrado_por)
        if not usuario or usuario.get("grupo_id") != grupo_id:
            return jsonify({"error": "Usuário não encontrado no grupo"}), 404
        
        # Verificar participantes
        participantes = data.get("participantes", [])
        if not participantes:
            # Se não informar participantes, dividir entre todos do grupo
            usuarios_grupo = Usuario.find_by_grupo(grupo_id)
            participantes = [str(u.get("_id")) for u in usuarios_grupo]
            data["participantes"] = participantes
        
        # Criar nova despesa
        try:
            despesa = Despesa.from_dict(data)
            despesa_id = despesa.save()
            
            # Calcular valor por participante
            valor_total = float(data.get("valor", 0))
            valor_por_pessoa = valor_total / len(participantes)
            
            # Notificar participantes
            for participante_id in participantes:
                if participante_id != registrado_por:  # Não notificar quem registrou
                    notificacao = Notificacao(
                        titulo=f"Nova despesa: {data.get('titulo')}",
                        mensagem=f"Você foi incluído em uma despesa de R$ {valor_total:.2f}. Sua parte é R$ {valor_por_pessoa:.2f}.",
                        usuario_id=participante_id,
                        tipo="despesa",
                        referencia_id=despesa_id,
                        grupo_id=grupo_id
                    )
                    notificacao.save()
            
            return jsonify({
                "message": "Despesa criada com sucesso",
                "despesa_id": despesa_id,
                "valor_por_pessoa": valor_por_pessoa
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_despesa(despesa_id):
        try:
            despesa = Despesa.find_by_id(despesa_id)
            if not despesa:
                return jsonify({"error": "Despesa não encontrada"}), 404
            
            # Calcular valor por participante
            valor_total = float(despesa.get("valor", 0))
            num_participantes = len(despesa.get("participantes", []))
            valor_por_pessoa = valor_total / num_participantes if num_participantes > 0 else 0
            
            despesa["valor_por_pessoa"] = valor_por_pessoa
            
            return jsonify(despesa), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def atualizar_despesa(despesa_id):
        data = request.get_json()
        
        try:
            # Verificar se a despesa existe
            despesa = Despesa.find_by_id(despesa_id)
            if not despesa:
                return jsonify({"error": "Despesa não encontrada"}), 404
            
            # Atualizar despesa
            success = Despesa.update(despesa_id, data)
            if success:
                # Se houver alteração de valor ou participantes, notificar
                if "valor" in data or "participantes" in data:
                    despesa_atualizada = Despesa.find_by_id(despesa_id)
                    valor_total = float(despesa_atualizada.get("valor", 0))
                    participantes = despesa_atualizada.get("participantes", [])
                    valor_por_pessoa = valor_total / len(participantes) if participantes else 0
                    
                    # Notificar participantes sobre a alteração
                    for participante_id in participantes:
                        notificacao = Notificacao(
                            titulo=f"Despesa atualizada: {despesa_atualizada.get('titulo')}",
                            mensagem=f"Uma despesa que você participa foi atualizada. Sua parte agora é R$ {valor_por_pessoa:.2f}.",
                            usuario_id=participante_id,
                            tipo="despesa",
                            referencia_id=despesa_id,
                            grupo_id=despesa_atualizada.get("grupo_id")
                        )
                        notificacao.save()
                
                return jsonify({
                    "message": "Despesa atualizada com sucesso",
                }), 200
            else:
                return jsonify({"error": "Falha ao atualizar despesa"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_despesa(despesa_id):
        try:
            # Verificar se a despesa existe
            despesa = Despesa.find_by_id(despesa_id)
            if not despesa:
                return jsonify({"error": "Despesa não encontrada"}), 404
            
            # Deletar despesa
            success = Despesa.delete(despesa_id)
            if success:
                # Notificar participantes sobre a remoção
                for participante_id in despesa.get("participantes", []):
                    notificacao = Notificacao(
                        titulo=f"Despesa removida: {despesa.get('titulo')}",
                        mensagem=f"Uma despesa que você participava foi removida.",
                        usuario_id=participante_id,
                        tipo="despesa",
                        referencia_id=despesa_id,
                        grupo_id=despesa.get("grupo_id")
                    )
                    notificacao.save()
                
                return jsonify({"message": "Despesa deletada com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao deletar despesa"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_despesas_por_grupo(grupo_id):
        try:
            despesas = Despesa.find_by_grupo(grupo_id)
            return jsonify(despesas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_despesas_por_participante(usuario_id):
        try:
            despesas = Despesa.find_by_participante(usuario_id)
            return jsonify(despesas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_despesas_por_categoria(grupo_id, categoria):
        try:
            despesas = Despesa.find_by_categoria(grupo_id, categoria)
            return jsonify(despesas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_total_por_categoria(grupo_id):
        try:
            totais = Despesa.obter_total_por_categoria(grupo_id)
            return jsonify(totais), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500