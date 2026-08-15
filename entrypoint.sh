#!/bin/sh
set -e

# Entrypoint: aplica migrações, coleciona estáticos e inicia Gunicorn.
# Faz tentativas de conexão ao DB para lidar com startups lentas do serviço de banco.

MAX_TRIES=12
SLEEP_SECONDS=5
n=0

echo "Aguardando o banco de dados..."
until [ "$n" -ge $MAX_TRIES ]
do
  if python - <<'PY'
import os
import sys
import dj_database_url
from psycopg import connect, OperationalError

try:
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        sys.exit(2)
    conn = connect(db_url, connect_timeout=3)
    conn.close()
    sys.exit(0)
except OperationalError:
    sys.exit(1)
except Exception:
    sys.exit(3)
PY
  then
    echo "Banco disponível."
    break
  fi
  n=$((n+1))
  echo "Tentativa $n/$MAX_TRIES: banco indisponível. Dormindo $SLEEP_SECONDS s..."
  sleep $SLEEP_SECONDS
done

if [ "$n" -ge $MAX_TRIES ]; then
  echo "Não foi possível conectar ao banco após $MAX_TRIES tentativas. Saindo." >&2
  exit 1
fi

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
