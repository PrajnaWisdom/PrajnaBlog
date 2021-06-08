from math import ceil
from functools import partial
from fastapi import status
from fastapi.responses import JSONResponse

from app.exc.codes import (
    BIZ_CODE_OK,
    BIZ_CODE_FAIL,
    BIZ_CODE_NOT_EXISTS,
    CODE_MESSAGE,
)


def response(data=None, code=BIZ_CODE_OK, message: str = None):
    if not message:
        message = CODE_MESSAGE.get(code, "成功")
    resp = dict(code=code, message=message, data=data)
    return JSONResponse(content=resp, status_code=status.HTTP_200_OK)


class Response:
    success = response

    response = response

    not_found = partial(response, code=BIZ_CODE_NOT_EXISTS)

    fail = partial(response, code=BIZ_CODE_FAIL)


def paginate(query, page: int = 1, per_page: int = 10):
    count = query.count()
    pages = int(ceil(float(count) / per_page))
    paginate = {
        "total": count,
        "per_page": per_page,
        "page": page,
        "pages": pages
    }
    if count != 0:
        if pages < page:
            return [], paginate
    else:
        return [], paginate
    query = query.offset(per_page * (page - 1)).limit(per_page)
    return query.all(), paginate
