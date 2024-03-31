"""
Web API for converting SVG to PNG

This module has class STP and main function.
- main is the CLI wrapper for STP
- STP is the application itself
"""

from typing import Annotated
import argparse

from fastapi import FastAPI, Query
from fastapi import status, HTTPException, Response
from fastapi.responses import HTMLResponse
import uvicorn

from urllib.request import urlopen
from cairosvg import svg2png


class STP(FastAPI):
    """
    Web API for converting SVG to PNG
    """

    default_index: str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG to PNG</title>
</head>
<body>
    Follow <a href="https://github.com/nakidai/stp">this link</a> for examples.
</body>
</html>"""

    def __init__(self, index: str | None = None) -> None:
        """
        Create App instance

        :argument index: Page if there's no arguemnt
        """
        super().__init__()
        self.index: str = App.default_index if index is None else index

        @self.get("/")
        def app(link: Annotated[str | None, Query()] = None) -> Response:
            """
            Convert SVG to PNG, show self.index if there's no argument

            :argument link: Link to the SVG image
            :return: Converted image or self.index if there's no link
            """
            if link is None:
                return Response(content=self.index, media_type="text/html")

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
    parser.add_argument(
        "-i", "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="IP of your host"
    )
    args = parser.parse_args()

    try:
        uvicorn.run(
            STP(),
            host=args.host,
            port=args.port,
            log_level="info"
        )
    except KeyboardInterrupt:
        pass
