from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.elastic.main import ElasticInitOperations
from app.services.elastic.main import ElasticDataOperations
from app.services.elastic.utils import get_records
from app.config.settings import INITIAL_DATA_DIR

router = APIRouter()


@router.post('/setup')
async def initial_setup():
    elastic_init = ElasticInitOperations()
    elastic_data = ElasticDataOperations()

    await elastic_init.check_connection()
    records = await get_records(INITIAL_DATA_DIR)

    await elastic_init.create_index()
    await elastic_data.add_data(records)

    return JSONResponse(content={
        "status": "successful"
    })


@router.post('/search')
async def search(query: str):
    es = ElasticDataOperations()

    result = await es.search_data(query)

    if not len(result):
        body = {
            "detail": "Not found"
        }
        status_code = 404
    else:
        body = {
            "content": result
        }
        status_code = 200

    return JSONResponse(
        status_code=status_code,
        content=body
    )


