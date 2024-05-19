import time

import json
from json.decoder import JSONDecodeError

from fastapi import Request
from fastapi.responses import JSONResponse

from app.crud.log import create_log
from app.schemas.log import Log

from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        method, path = request.method, request.scope['path']
        params = request.query_params._dict

        response_body = b""
        try:
            response = await call_next(request)
            async for chunk in response.body_iterator:
                response_body += chunk

            response_body = response_body.decode()
            status_code = response.status_code

            try:
                response_body = json.loads(response_body)

                return JSONResponse(status_code=status_code, content=response_body)

            except JSONDecodeError:
                return Response(content=response_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type)

        except Exception as e:
            status_code, response_body = getattr(e, 'status_code', 500), getattr(e, 'error', f'Uncaught error: {e}')
            return JSONResponse(status_code=status_code, content={
                "error": response_body,
            })

        finally:
            current_time = time.time()
            await create_log(Log(
                timestamp=str(current_time),
                method=method,
                path=path,
                query_params=params,
                status_code=status_code,
                response={"content": response_body},
                response_time=float(current_time - start_time)
            ))
