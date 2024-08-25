FROM python:3.12-slim-bookworm as builder

ENV APP_HOME=/app
# run mkdir so that folder owned by mambauser
WORKDIR ${APP_HOME}
COPY api/requirements.txt ./
RUN pip install -r requirements.txt
# Full otel dependencies can be listed and installed by opentelemetry-bootstrap - does make package install blind.
# Better to get a list of libs needed from opentelemetry-bootstrap and then put them in requirements.txt
# RUN opentelemetry-bootstrap --action=install
COPY api ./

FROM builder AS tester
# seperated these out so that failures are clearer to see
RUN pip install pytest-cov flake8
RUN python -m flake8 --max-line-length=119
RUN python -m pytest --cov=./api

FROM builder AS prod
RUN groupadd --system app && \
    useradd -g app --system app && \
    chown -R app:app ${APP_HOME} && \
    chmod -R 755 ${APP_HOME}
USER app

ENV LOG_LEVEL=DEBUG
ENV N_WORKERS=2

CMD opentelemetry-instrument --log_level=${LOG_LEVEL} \
    gunicorn --workers ${N_WORKERS} --worker-class uvicorn.workers.UvicornWorker api.api_app:app --bind 0.0.0.0:6780 --log-level ${LOG_LEVEL}
