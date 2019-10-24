from starlette.responses import JSONResponse
from starlette.status import (HTTP_201_CREATED, HTTP_404_NOT_FOUND,
                              HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT)


def DoesNoExist():
    return JSONResponse({"error": "Query didn't find a result"}, status_code=HTTP_404_NOT_FOUND)

def ValidationError():
    return JSONResponse({"error": "Error validating data"}, status_code=HTTP_400_BAD_REQUEST)

