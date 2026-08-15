# Plataforma Laser

SaaS modular para gestão de clínicas de estética, com clientes, procedimentos laser e sessões clínicas. A base foi desenhada para multi-tenancy: cada usuário pertence a uma clínica e todas as consultas de negócio são filtradas pelo tenant autenticado.

## Desenvolvimento local

1. Copie `.env.example` para `.env` e ajuste os valores.
2. Crie um ambiente virtual com Python 3.13+ e instale `requirements.txt`.
3. Suba o PostgreSQL com `docker compose up -d db`.
4. Execute `python manage.py migrate` e `python manage.py createsuperuser`.
5. Execute `python manage.py runserver`.

Para rodar os testes sem PostgreSQL local: `DJANGO_TESTING=True DJANGO_DEBUG=True python manage.py test`.

No admin, crie a clínica e associe o usuário a ela. Em produção, use PostgreSQL gerenciado, `DEBUG=False`, HTTPS, segredo externo, `collectstatic` e Gunicorn.

## Arquitetura

Os domínios estão separados em `tenants`, `users`, `clients`, `laser` e `dashboard`. Models usam chaves estrangeiras, constraints e índices tenant-aware. O middleware resolve o tenant na sessão e as views protegidas exigem autenticação Django. A interface usa Bootstrap 5, WhiteNoise e CSS responsivo.

## Qualidade e segurança

Inclui CSRF, cookies HTTP-only, proteção de clickjacking e MIME sniffing, validação de extensão de imagens, ORM Django e escopo por tenant. Antes do deploy, configure limites de upload no proxy, backup do banco, logging estruturado e CI para testes.
