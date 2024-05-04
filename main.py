import hashlib
import json

import click
from aiohttp import web


async def healthcheck(request: web.Request):
    return json.dumps({})


async def hash_string(request: web.Request):
    try:
        data = await request.json()
        string_to_hash = data["string"]
    except KeyError:
        return web.json_response({"validation_errors": ["Missing 'string' field"]}, status=400)

    hash_string = hashlib.sha256(string_to_hash.encode("utf-8")).hexdigest()
    return web.json_response({"hash_string": hash_string})


@click.command()
@click.option("--host", default="localhost", help="Хост для запуска сервера")
@click.option("--port", default=8000, help="Порт для запуска сервера")
async def run_server(host, port):
    app = web.Application()
    app.router.add_route("GET", "/healthcheck", healthcheck)
    app.router.add_route("POST", "/hash", hash_string)

    await web.serve(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
