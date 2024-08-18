# using micromamba for speed
FROM python:3.12-slim-bookworm as builder

ENV APP_HOME=/app
# run mkdir so that folder owned by mambauser
WORKDIR ${APP_HOME}
COPY api ./
RUN pip install -r requirements.txt

FROM builder AS tester
RUN pip install pytest-cov flake8 && \
    python -m flake8 --max-line-length=119 && \
    python -m pytest --cov=./api

FROM builder AS prod
RUN groupadd --system app && \
    useradd -g app --system app && \
    chown -R app:app ${APP_HOME} && \
    chmod -R 755 ${APP_HOME}
USER app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.api_app:app", "--bind", "0.0.0.0:6780", "--log-level", "DEBUG"]