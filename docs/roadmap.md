# Roadmap inicial

## Fundamentos
- Definir provedor de email principal e secundário (fallback SMTP) e criar contas de teste.
- Garantir configuração de domínio com SPF/DKIM para melhorar entregabilidade.
- Preparar `.env.example` com variáveis necessárias.

## Milestone 1: API e persistência
- Criar projeto FastAPI com rotas para clientes e boletos.
- Modelar banco em PostgreSQL com SQLAlchemy + Alembic (migrações).
- Implementar camada de serviço para cadastro e consulta de boletos.

## Milestone 2: Lembretes e agendamentos
- Implementar APScheduler para rodar tarefas periódicas.
- Job que identifica boletos com vencimento em N dias e enfileira envio de email.
- Regras de retry exponencial para falhas de entrega.

## Milestone 3: Envio de emails
- Serviço de email com SDK do provedor (ex.: AWS SES) e fallback SMTP.
- Templates HTML/TXT com Jinja2; armazenar em `templates/`.
- Logar resultado dos envios e armazenar histórico no banco.

## Milestone 4: Observabilidade e segurança
- Logs estruturados e métricas básicas (tempo de envio, taxa de falha, opt-out).
- Endpoints protegidos com autenticação (token ou API key).
- Sanitização de dados pessoais e política de retenção alinhada à LGPD.

## Milestone 5: CI/CD e deploy
- GitHub Actions executando lint, testes e build.
- Dockerfile + docker-compose para rodar app, banco e worker localmente.
- Pipeline de deploy para ambiente de staging/produção.
