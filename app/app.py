# Main app. Routing API logic.

import asyncio
import fastapi
import fastapi.templating
import json

from typing import Annotated

app = fastapi.FastAPI()
templates = fastapi.templating.Jinja2Templates('templates')


@app.get('/', response_class=fastapi.responses.HTMLResponse)
async def get_index(request: fastapi.Request):
    return templates.TemplateResponse(
        'index.html',
        context={
            'request': request,
            'var': 'test data'
        }
    )