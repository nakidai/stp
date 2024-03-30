from typing import Annotated
import argparse

from fastapi import FastAPI, Query
from fastapi import status, HTTPException, Response
from fastapi.responses import HTMLResponse
import uvicorn

from urllib.request import urlopen
from cairosvg import svg2png


app = FastAPI()

@app.get("/")
def root(link: Annotated[str | None, Query()] = None) -> Response:
    if link is None:
        return Response(content="Hello, world!", media_type="text/html")

    try:
        svg = urlopen(link).read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot download file: {e}"
        )
    try:
        png = svg2png(bytestring=svg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot convert file: {e}"
        )

    return Response(content=png, media_type="image/png")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="stp",
        description="SVG to PNG web converter"
    )
    parser.add_argument(
        "-p", "--port",
        default=8000,
        type=int,
        metavar="PORT",
        help="Port where app should be run"
    )
    args = parser.parse_args()

    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=args.port,
            log_level="info"
        )
    except KeyboardInterrupt:
        pass
