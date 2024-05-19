import logging

from app.config.database import async_session
from app.config.log_conf import setup_logging

from app.schemas.log import Log
from app.models.log import Log as LogDB

logger = logging.getLogger(__name__)
setup_logging(__name__)

async def create_log(log: Log):
    log = LogDB(
        timestamp=log.timestamp,
        method=log.method,
        path=log.path,
        query_params=log.query_params,
        status_code=log.status_code,
        response=log.response,
        response_time=log.response_time
    )

    async with async_session() as session:
        try:
            session.add(log)

            await session.commit()
            await session.refresh(log)
        except Exception as e:
            logger.error(f"Error while adding log to database - {e}, data: {log.__dict__}")

    return log
