# Deploy recomendado: Render (Web) + Supabase (Postgres) + Cloudinary (mídia)

Este guia configura um deploy com baixo custo, resiliente e fácil de operar: o app roda como um service Docker no Render, o banco é gerenciado pelo Supabase (ou outro Postgres externo) e as imagens ficam no Cloudinary (plano grátis possível).

Resumo dos passos

1. Criar contas: Render, Supabase, Cloudinary.
2. Criar projeto Supabase e copiar `DATABASE_URL`.
3. Criar conta Cloudinary e copiar `CLOUDINARY_URL`.
4. Conectar o repositório Git ao Render e configurar o serviço web (Docker).
5. Definir variáveis de ambiente no Render (SECRET_KEY, DATABASE_URL, CLOUDINARY_URL, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS).
6. Deploy e rodar `python manage.py migrate`, `python manage.py collectstatic --noinput` e `python manage.py createsuperuser` via Shell do Render.
7. Configurar domínio e HTTPS.
8. Monitorar / backups (Supabase) e rotinas de export periódico enquanto estiver começando.

Variáveis de ambiente necessárias

- `DJANGO_SECRET_KEY` — chave secreta segura.
- `DJANGO_DEBUG` — `False` em produção.
- `DJANGO_ALLOWED_HOSTS` — domínios (ex: `minha-app.onrender.com,meudominio.com`).
- `DATABASE_URL` — URL de conexão PostgreSQL (fornecido pelo Supabase). Ex: `postgres://user:pass@db.supabase.co:5432/dbname`.
- `CLOUDINARY_URL` — string de conexão do Cloudinary (formato padrão `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`).
- Opcional: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `SENTRY_DSN`, etc.

Passo a passo (detalhado)

1) Criar e configurar o DB no Supabase
- Crie um novo projeto no Supabase.
- Na página do projeto, acesse Settings → Database → Connection string e copie a `DATABASE_URL`.
- Garanta que as regras de rede permitem conexões do Render (normalmente não é necessário alterar).
- Ative backups automáticos se disponível no seu plano (recomendado para produção).

2) Criar conta no Cloudinary
- Crie uma conta gratuita no Cloudinary.
- No Dashboard → Account details copie `CLOUDINARY_URL`.
- No plano grátis já é possível armazenar e servir imagens; regras de transformação e limites aplicam-se.

3) Conectar repositório ao Render
- No Render dashboard, clique em "New" → "Web Service".
- Conecte o repositório GitHub/GitLab que contém este projeto.
- Escolha "Docker" como ambiente (o projeto já tem `Dockerfile`).
- `Dockerfile path`: `Dockerfile` (root do repo).
- `Start Command`: `gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3` (ou deixe o `render.yaml` usar `startCommand`).
- Escolha `plan: starter` ou `free` temporariamente (starter evita sleep e é recomendado para produção leve).

4) Definir Variáveis de Ambiente no Render
- Na Settings do service, adicione:
  - `DJANGO_SECRET_KEY` → valor seguro (use `openssl rand -hex 32` localmente para gerar).
  - `DJANGO_DEBUG` → `False`
  - `DJANGO_ALLOWED_HOSTS` → seu domínio + `*.onrender.com` ou `minha-app.onrender.com`.
  - `DATABASE_URL` → valor do Supabase.
  - `CLOUDINARY_URL` → valor do Cloudinary.

5) Deploy e migrações
- Faça deploy (o Render fará build via Docker).
- Após sucesso, abra o Shell do serviço (Dashboard → Shell) e rode:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

- Se preferir rodar as migrações automaticamente, crie um `Render` "Start Command" que execute um script `entrypoint.sh` que aplique migrations antes de iniciar o Gunicorn — eu posso ajudar a gerar esse script.

6) Configurar domínio e HTTPS
- No Render, vá em Settings → Custom Domains e adicione seu domínio.
- Aponte o DNS (A/CNAME) conforme instruções do Render. O Render provisiona HTTPS automaticamente.

7) Backups e rotinas de segurança
- Configure backups no Supabase (ou export semanal manual se no plano grátis).
- Agende export periódica do DB: `pg_dump` para um storage seguro (S3, Google Drive manual, etc.).
- Verifique logs e alertas.

8) Observabilidade e manutenção
- Configure logging centralizado (Render já mostra logs básicos). Para produção, considere Sentry para erros e Papertrail/LogDNA para logs.
- Monitore uso de Cloudinary e custos.

Notas e dicas rápidas
- `config/settings.py` já suporta `DATABASE_URL` e `CLOUDINARY_URL` (se `CLOUDINARY_URL` estiver presente, o projeto usará `cloudinary_storage`).
- `requirements.txt` foi atualizado com `dj-database-url` e `django-cloudinary-storage`.
- Se estiver desconfortável com pagar pelo Render Starter, você pode testar tudo com `plan: free` e depois migrar para `starter` quando estiver pronto.

Comandos úteis locais

- Gerar `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- Testar com `DATABASE_URL` local apontando para Supabase:
```bash
export DATABASE_URL="postgres://..."
python manage.py migrate
python manage.py runserver
```

Posso gerar também:
- `entrypoint.sh` para aplicar migrations automaticamente no deploy; e
- um `render.yaml` alternativo já preparado para usar `plan: starter` e sem criar DB no Render.

Quer que eu gere `entrypoint.sh` + versão atualizada de `render.yaml` que assume `DATABASE_URL` externo e instruções de CI para deploy automático?