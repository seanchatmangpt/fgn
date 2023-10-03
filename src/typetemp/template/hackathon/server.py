import asyncio
from aiohttp import web


async def handle(request):
    return web.Response(text="Hello, Advanced World")


app = web.Application()
app.router.add_get("/", handle)


def run_advanced_server():
    web.run_app(app)


if __name__ == "__main__":
    run_advanced_server()
    # Test the server is running
    import requests

    response = requests.get("http://localhost:8000")
    assert response.status_code == 200
    assert response.text == "Hello, Advanced World"
