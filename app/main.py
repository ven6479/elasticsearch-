from fastapi import FastAPI
from queue import Queue
from contextlib import asynccontextmanager

import logging
from logging.handlers import QueueHandler, QueueListener
from logging import StreamHandler

from app.config.log_conf import setup_logging
from app.services.elastic.main import es, Elastic
from app.routers.search import router as SearchRouter
from app.middlewares.log import LoggingMiddleware

logger = logging.getLogger(__name__)
setup_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Elastic().check_connection()

    que = Queue()

    logger.addHandler(QueueHandler(que))

    listener = QueueListener(que, StreamHandler())
    listener.start()
    logger.debug(f'Logger has started')

    yield

    logger.debug(f"Logger has stopped")

    await es.close()
    listener.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(SearchRouter)
app.add_middleware(LoggingMiddleware)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
