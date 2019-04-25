#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import logging; logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web, web_runner

def index(request):
    return web.Response(body=b'Awesome', content_type='text/html')

async def init():
    app = web_runner.AppRunner(app=web.Application()).app()
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app._make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()