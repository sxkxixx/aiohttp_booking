from aiohttp.web import Application, run_app

app = Application()

run_app(app, host='localhost', port=8000)
