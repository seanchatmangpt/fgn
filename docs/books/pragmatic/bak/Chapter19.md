```python
from typing import Dict
from fastapi import FastAPI
import aiomysql
from github import Github

class PragmaticStarterKit:
    def __init__(self, app_name: str, db_params: dict, github_token: str):
        self.app = FastAPI(title=app_name)
        self.db_params = db_params
        self.github_repo = Github(github_token)

    async def init_db(self):
        pool = await aiomysql.create_pool(**self.db_params)
        self.app.state.pool = pool

    def create_db_models(self):
        # Code for creating database models

    async def clean_up(self):
        self.app.state.pool.close()
        await self.app.state.pool.wait_closed()

    def setup_routes(self):
        # Code for setting up routes

    def create_github_actions(self):
        # Code for creating github actions

@app.on_event("startup")
async def on_startup():
    await app.state.db.init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.clean_up()

def create_pragmatic_starter_kit(app_name: str, db_params: Dict[str, str], github_token: str) -> str:
    kit = PragmaticStarterKit(app_name, db_params, github_token)
    kit.init_db()
    kit.create_db_models()
    kit.setup_routes()
    kit.create_github_actions()
```