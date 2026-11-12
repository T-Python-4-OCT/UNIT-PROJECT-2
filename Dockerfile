FROM oven/bun:1.4.4-slim AS frontend
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY vite.config.js ./
COPY saudi_atlas/projects/frontend ./saudi_atlas/projects/frontend
COPY saudi_atlas/projects/templates ./saudi_atlas/projects/templates
COPY saudi_atlas/projects/data/atlas-map.json ./saudi_atlas/projects/data/atlas-map.json
RUN bun run --bun build

FROM python:3.15.2-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ATLAS_DEBUG=0 \
    PORT=10000 \
    WEB_CONCURRENCY=2
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY --from=frontend /app/saudi_atlas/projects/static/build ./saudi_atlas/projects/static/build

RUN python manage.py compiletranslations \
    && python manage.py collectstatic --noinput --verbosity 0 \
    && useradd --system --no-create-home --uid 10001 atlas

USER atlas
EXPOSE 10000
CMD ["sh", "-c", "exec gunicorn saudi_atlas.wsgi:application --bind 0.0.0.0:${PORT} --access-logfile - --timeout 60"]
