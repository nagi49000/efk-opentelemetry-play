from fastapi import FastAPI
import datetime
import logging
from pydantic import BaseModel
# for sending logs through OTEL
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


class HelloWorldResponse(BaseModel):
    message: str


class ParrotRequestParams(BaseModel):
    n_repeat: int
    sep: str
    parrot_str: str


class ParrotRequest(BaseModel):
    header: str
    parrot_request: ParrotRequestParams


class ParrotBackResponseResults(BaseModel):
    time: str
    parrot: str


class ParrotBackResponse(BaseModel):
    header: str
    results: ParrotBackResponseResults


def get_gunicorn_logger(name="gunicorn.error"):
    logger = logging.getLogger(name)  # dirty way of wiring into the gunicorn logger

    # added in an OTEL handler to the logger
    # Create and set the logger provider
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)
    # Create the OTLP log exporter that sends logs to configured destination
    exporter = OTLPLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    # Attach OTLP handler to root logger
    handler = LoggingHandler(logger_provider=logger_provider)
    logger.addHandler(handler)

    # overwrite the root logger with the gunicorn logger
    root_logger = logging.getLogger()
    root_logger.handlers = logger.handlers
    root_logger.setLevel(logger.level)
    return logger


def create_app(logger_name="gunicorn.error"):
    logger = get_gunicorn_logger(name=logger_name)
    app = FastAPI(title="simple test app")

    @app.get("/hello_world", response_model=HelloWorldResponse)
    async def hello_world():
        logger.debug('/hello_world')
        return {"message": "Hello World"}

    @app.post("/parrot_back", response_model=ParrotBackResponse)
    async def parrot_back(p: ParrotRequest):
        p_dict = p.model_dump()
        logger.debug(f'/parrot_back: {p_dict}')
        params = p_dict['parrot_request']
        r_dict = {
            'header': p_dict['header'],
            'results': {
                'time': datetime.datetime.now(datetime.UTC).isoformat(timespec='seconds'),
                'parrot': 'parrot back ' + params['sep'].join([params['parrot_str']]*params['n_repeat'])
            }
        }
        return r_dict

    return app
