# MoradiApp API - Descrição

Estrutura MVC Completa:

Models: Implementação de todas as classes do diagrama (Usuario, GrupoRepublica, Tarefa, Despesa, Relatorio, Notificacao, RegraCasa)
Controllers: Lógica de negócios para cada modelo
Routes: APIs RESTful para acessar as funcionalidades


Características Implementadas:

Autenticação com JWT
Conexão com MongoDB
Validação de dados e tratamento de erros
Notificações para ações importantes
Relatórios financeiros
Sistema de gerenciamento de regras da casa


Configuração para Implantação:

Dockerfile para containerização
docker-compose.yml para orquestração de serviços

Endpoints para Teste:

Exemplos documentados de chamadas para todos os recursos principais da API

## Para executar o projeto com o Docker

docker-compose up -d

Isso iniciará tanto o servidor MongoDB quanto o backend Flask. A API estará disponível em http://localhost:5000.

## Para testes de desenvolvimento sem Docker, você precisará:

Ter o MongoDB instalado e rodando na sua máquina
Instalar as dependências com pip install -r requirements.txt
Executar o servidor com python main.py

# MoradiApp API - Endpoints para teste

## Endpoints de Autenticação

### Registrar Usuário
```
POST /api/usuarios/registrar
```
Body:
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "31999999999",
  "senha": "senha123",
  "tipo": "padrao"
}
```

### Login
```
POST /api/usuarios/login
```
Body:
```json
{
  "email": "joao@example.com",
  "senha": "senha123"
}
```
Resposta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Login realizado com sucesso",
  "usuario": {
    "email": "joao@example.com",
    "id": "6123456789abcdef12345678",
    "nome": "João Silva",
    "tipo": "padrao",
    "grupo_id": "6123456789abcdef12345679"
  }
}
```

## Grupos de República

### Criar Grupo
```
POST /api/grupos
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "nome": "República dos Estudantes",
  "endereco": "Rua da Universidade, 123",
  "admin_id": "6123456789abcdef12345678",
  "max_moradores": 8,
  "descricao": "República próxima ao campus universitário"
}
```

### Adicionar Usuário ao Grupo
```
POST /api/grupos/6123456789abcdef12345679/usuarios
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "usuario_id": "6123456789abcdef12345680",
  "tipo": "padrao"
}
```

## Tarefas

### Criar Tarefa
```
POST /api/tarefas
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "titulo": "Limpar a cozinha",
  "descricao": "Lavar louça, limpar fogão e bancadas",
  "grupo_id": "6123456789abcdef12345679",
  "responsavel_id": "6123456789abcdef12345678",
  "prazo": "2025-03-01T12:00:00",
  "prioridade": "media"
}
```

### Listar Tarefas do Grupo
```
GET /api/tarefas/grupo/6123456789abcdef12345679
```
Headers:
```
Authorization: Bearer <token-jwt>
```

### Atualizar Status da Tarefa
```
PUT /api/tarefas/6123456789abcdef12345681
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "status": "concluida"
}
```

## Despesas

### Registrar Despesa
```
POST /api/despesas
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "titulo": "Compras do mês",
  "valor": 350.75,
  "grupo_id": "6123456789abcdef12345679",
  "registrado_por": "6123456789abcdef12345678",
  "categoria": "alimentacao",
  "participantes": ["6123456789abcdef12345678", "6123456789abcdef12345680"],
  "descricao": "Compras de supermercado"
}
```

### Listar Despesas do Grupo
```
GET /api/despesas/grupo/6123456789abcdef12345679
```
Headers:
```
Authorization: Bearer <token-jwt>
```

### Gerar Relatório Financeiro
```
GET /api/relatorios/financeiro/grupo/6123456789abcdef12345679?inicio=2025-01-01&fim=2025-03-01&criado_por=6123456789abcdef12345678
```
Headers:
```
Authorization: Bearer <token-jwt>
```

## Regras da Casa

### Criar Regra
```
POST /api/regras
```
Headers:
```
Authorization: Bearer <token-jwt>
```
Body:
```json
{
  "titulo": "Silêncio após 22h",
  "descricao": "Evitar barulho nos quartos e áreas comuns após as 22h",
  "grupo_id": "6123456789abcdef12345679",
  "criado_por": "6123456789abcdef12345678",
  "categoria": "convivencia"
}
```

### Listar Regras do Grupo
```
GET /api/regras/grupo/6123456789abcdef12345679
```
Headers:
```
Authorization: Bearer <token-jwt>
```

# Testes Unitários

python3 -m unittest tests/test_unit.py

1. TestModelUsuario
Testa a funcionalidade do modelo Usuario:

test_criacao_usuario: Verifica se um usuário é criado corretamente, se os dados são armazenados adequadamente, se a senha é hasheada (não armazenada em texto plano) e se o método save() funciona como esperado.
test_verificacao_senha: Testa o método de verificação de senha, confirmando que ele retorna True para senhas corretas e False para senhas incorretas.
test_busca_usuario_por_email: Verifica se o método estático find_by_email() funciona corretamente, buscando um usuário pelo endereço de email.

2. TestModelTarefa
Testa a funcionalidade do modelo Tarefa:

test_criacao_tarefa: Verifica se uma tarefa é criada corretamente com todos os atributos esperados, e se o método save() funciona como esperado.
test_atualizacao_tarefa: Testa se o método de atualização de tarefas funciona corretamente, verificando se os campos são atualizados e se a data de conclusão é definida quando o status é alterado para "concluída".
test_listar_tarefas_proximas: Verifica se o método para listar tarefas com prazos próximos funciona corretamente, filtrando por grupo e retornando tarefas ordenadas por prazo.

3. TestModelDespesa
Testa a funcionalidade do modelo Despesa:

test_criacao_despesa: Verifica se uma despesa é criada corretamente com todos os atributos esperados, e se o método save() funciona como esperado.
test_calcular_valor_por_participante: Testa se o cálculo do valor por participante (dividindo o valor total pelo número de participantes) funciona corretamente.
test_obter_total_por_categoria: Verifica se o método para obter o total de despesas por categoria funciona corretamente, usando agregação do MongoDB.

Características gerais dos testes:

Mocks: Todos os testes usam patch do unittest.mock para substituir o acesso ao MongoDB por objetos simulados, evitando a necessidade de um banco de dados real para testes.
setUp: Cada classe de teste tem um método setUp que é executado antes de cada teste, preparando os dados necessários.
Assert methods: São usados diversos métodos de verificação como assertEqual, assertTrue, assertFalse e assertAlmostEqual para validar os resultados esperados.