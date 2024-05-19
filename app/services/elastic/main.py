import logging
from typing import List

from app.config.settings import ELASTIC_CREDS
from app.services.elastic.settings import SETTINGS
from app.config.log_conf import setup_logging

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import BadRequestError
from elasticsearch import ConflictError

es = AsyncElasticsearch(**ELASTIC_CREDS)
im = SETTINGS

logger = logging.getLogger(__name__)
setup_logging(__name__)

index_name = 'test_search20'


class Elastic:
    def __init__(self):
        self.__instance = es
        self.__mappings = im
        self.__index_name = index_name

    @property
    def instance(self):
        return self.__instance

    @property
    def mappings(self):
        return self.__mappings

    @property
    def index_name(self):
        return self.__index_name

    async def check_connection(self):
        state = await self.instance.ping(error_trace=True)

        if state is False:
            logger.error("Elastic is unavailable")
            raise AssertionError(f"Elastic is unavailable")

        logger.debug("Elastic is on")
        return True


class ElasticInitOperations(Elastic):

    async def exists_index(self):
        has_index = await self.instance.indices.exists(index=self.index_name)
        return has_index.body is True

    async def create_index(self):
        has_index = await self.exists_index()

        if has_index is False:
            try:
                response = await self.instance.indices.create(index=self.index_name, body=self.mappings)
                if response.meta.status == 200:
                    logging.info(f"Index created: {self.index_name} mappings: {self.mappings}")

            except BadRequestError as e:
                logger.error(f"Incorrect request, detail: {e}")
            except Exception as e:
                logger.error(f"Uncaught error, detail - {e}")


class ElasticDataOperations(Elastic):
    search_field = 'name_normalized'

    async def add_data(self, records: List[dict[str, str]]):
        for record in records:
            try:
                response = await self.instance.index(index=self.index_name, document=record, id=record.get('id', 0),
                                                     op_type='create')
                if response.body['result'] == "created":
                    logger.info(f"Add record to index {self.index_name}: {record}")
                else:
                    logger.error(f"Failed to add on index {self.index_name}: {record}")

            except ConflictError as e:
                logger.error(f"Duplicated document - {record}. Error - {e}")
            except Exception as e:
                logger.error(f"Uncaught error while adding document {self.index_name}: {record} Error {e}")
                continue

    async def search_data(self, search_query):
        query = {
            "match": {
                self.search_field: {
                    "query": search_query,
                    "fuzziness": "AUTO",
                    "operator": "or",
                    "prefix_length": 1
                }
            }
        }
        result = await self.instance.search(index=self.index_name, query=query)

        logging.debug(f"Search /input: {search_query} /output: {result}")

        hits = result['hits']

        score_possible = hits['max_score'] or 1 / 100 * 60  # 60% from max_score
        results = [{
            "id": i['_source']['id'],
            "name": i['_source']['name']
        } for i in hits['hits'] if i['_score'] >= score_possible]

        return results
