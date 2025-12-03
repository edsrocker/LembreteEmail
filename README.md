# LembreteEmail

Sistema de envio de lembrete de pagamentos por email, incluindo agendamento de boletos e registro de entregas.

## Objetivo
Criar um serviço capaz de:
- Receber dados de clientes e boletos (valor, vencimento, identificador).
- Agendar lembretes por email próximos ao vencimento.
- Gerenciar reenvios, acompanhamento de falhas e opt-out.

## Estrutura inicial do repositório
- `src/`: código-fonte do serviço (API, jobs agendados, integrações de email).
- `tests/`: testes automatizados.
- `templates/`: modelos HTML de email.
- `docs/`: documentação técnica (fluxos, arquitetura, requisitos).
- `infra/`: scripts/manifests de infraestrutura (ex.: Docker, pipelines).

## Executando localmente
1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. (Opcional) Copie `.env.example` para `.env` e ajuste as variáveis de email/banco.
4. Suba a API FastAPI em modo de desenvolvimento:
   ```bash
   uvicorn src.app.main:app --reload
   ```
5. Acesse `http://localhost:8000/docs` para testar as rotas de clientes, boletos e lembretes.

## Stack sugerida
- **Backend**: Python com FastAPI para expor APIs (clientes/boletos) e documentação automática.
- **Agendamentos**: APScheduler para rodar tarefas periódicas (envio de lembretes e reenvios).
- **Envio de email**: provedor transacional (AWS SES/SendGrid/Mailgun) com SDK oficial e fallback SMTP.
- **Templates**: Jinja2 para compor emails HTML e texto.
- **Banco de dados**: PostgreSQL com SQLAlchemy para modelar clientes, boletos e histórico de envios.
- **Observabilidade**: logs estruturados, métricas e alertas para falhas de entrega.

## Próximos passos recomendados
1. **Configurar ambiente local**
   - Criar `.env.example` com chaves de email (ex.: `SES_ACCESS_KEY`, `SES_SECRET_KEY`), dados do banco (`DATABASE_URL`) e configurações de agendamento (timezone, horários de envio).
   - Configurar ambiente virtual Python (poetry/pip) e dependências base (`fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `apscheduler`, `jinja2`, `python-dotenv`).
2. **Criar API inicial**
   - Endpoints para CRUD de clientes e boletos.
   - Endpoint para disparo manual de lembrete de boleto.
3. **Implementar agendamento**
   - Job para verificar boletos próximos do vencimento e enfileirar emails.
   - Regras de retry e limite de reenvio.
4. **Templates e envio**
   - Montar template HTML responsivo em `templates/`.
   - Camada de serviço de email com provider + fallback SMTP.
5. **Testes e observabilidade**
   - Testes unitários para camada de domínio e serviço de email.
   - Logs estruturados e métricas (tempo de envio, falhas, opt-outs).
6. **CI/CD e deploy**
   - Workflow GitHub Actions para lint/test/build.
   - Dockerfile e docker-compose para ambiente local com PostgreSQL.

## Como contribuir
1. Crie um branch a partir de `main`.
2. Abra um Pull Request descrevendo mudanças e testes executados.
3. Mantenha cobertura de testes e lint passando no CI.
