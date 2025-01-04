import sys
import re
import os
import argparse
import importlib
import logging

from aiohttp import web

from mediview-3d_server.mediview-3d_api import mediview-3dApi
from mediview-3d_server.rpc_server import RpcServer
from mediview-3d_server.chunking import CHUNK_SIZE


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host", default="localhost", help="Hostname for server to listen on"
    )
    parser.add_argument(
        "-P", "--port", default=4014, help="Port for server to listen on"
    )
    parser.add_argument(
        "--verbose", default=False, action="store_true", help="Enable verbose logging."
    )
    parser.add_argument("api_script", help="Python file that exposes ServerApi")
    return parser.parse_args()


def import_api_script(api_script_file: str):
    api_script_file = os.path.abspath(api_script_file)
    import_target = os.path.basename(api_script_file)

    script_filename, _, instance_name = import_target.partition(":")
    instance_name = instance_name or "mediview-3d"
    module_name = re.sub(r"\.py$", "", script_filename)

    sys.path.append(os.path.dirname(api_script_file))
    module = importlib.import_module(module_name)

    instance = module
    for attr_name in instance_name.split("."):
        instance = getattr(instance, attr_name)
    return instance


def run_server(
    api: mediview-3dApi,
    *,
    host: str,
    port: int,
    debug: bool = False,
    **kwargs,
):
    rpc_server = RpcServer(api, async_mode="aiohttp", **kwargs)

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    async def stop(app):
        await rpc_server.teardown()

    async def start():
        app = web.Application(client_max_size=CHUNK_SIZE)
        rpc_server.sio.attach(app)
        rpc_server.setup()
        app.on_shutdown.append(stop)
        return app

    web.run_app(start(), host=host, port=port)


def main(args):
    mediview-3d_api = import_api_script(args.api_script)

    if not isinstance(mediview-3d_api, mediview-3dApi):
        raise TypeError("Imported instance is not a mediview-3dApi")

    run_server(
        mediview-3d_api,
        host=args.host,
        port=args.port,
        debug=args.verbose,
        # socketio.AsyncServer kwargs
        async_handlers=True,
        cors_allowed_origins="*",
        logger=args.verbose,
        engineio_logger=args.verbose,
        max_http_buffer_size=CHUNK_SIZE,
    )


if __name__ == "__main__":
    main(parse_args())
