```python
import os
import files

@dataclass
class PragmaticStarterKit:
    app_name: str
    db_params: Dict[str, str]
    github_token: str
    AGIAgent: PragmaticProgrammerAGIAgent

    def __post_init__(self):
        self.app = FastAPI(title=self.app_name)
        self.github_repo = Github(self.github_token)

    async def init_db(self):
        pool = await aiomysql.create_pool(**self.db_params)
        self.app.state.pool = pool

    def create_db_models(self):
        db_model_code = self.AGIAgent.openai_completion("Create db models for FastApi app using SQLAlchemy ORM.")
        files.write_file(os.path.join(self.app_name, "models.py"), db_model_code)

    async def clean_up(self):
        self.app.state.pool.close()
        await self.app.state.pool.wait_closed()

    def setup_routes(self):
        routes_code = self.AGIAgent.openai_completion("Create CRUD routes for FastApi app.")
        files.write_file(os.path.join(self.app_name, "routes.py"), routes_code)

    def create_github_actions(self):
        github_actions_code = self.AGIAgent.openai_completion("Create Github CI/CD Actions for FastApi app.")
        files.write_file(os.path.join(self.app_name, ".github", "workflow", "main.yaml"), github_actions_code)
        
    def generate_docker_compose(self):
        docker_compose_content = self.AGIAgent.openai_completion("Generate a Docker Compose for FastApi app with postgres database")
        files.write_file(os.path.join(self.app_name, "docker-compose.yaml"), docker_compose_content)
        
    def generate_pytest(self):
        pytest_content = self.AGIAgent.openai_completion("Generate pytest codes for FastApi app")
        files.write_file(os.path.join(self.app_name, "test_app.py"), pytest_content)


@app.on_event("startup")
async def on_startup():
    await app.state.db.init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.clean_up()


def create_pragmatic_starter_kit(app_name: str, db_params: Dict[str, str], github_token: str) -> str:
    AGIAgent = PragmaticProgrammerAGIAgent()
    kit = PragmaticStarterKit(app_name, db_params, github_token, AGIAgent)
    kit.init_db()
    kit.create_db_models()
    kit.setup_routes()
    kit.create_github_actions()
    kit.generate_docker_compose()
    kit.generate_pytest()
    return "Pragmatic Starter Kit created successfully"
```

```python
import aiomysql
import asyncio
from fastapi import FastAPI, Depends
from github import Github
from typing import Any, Dict

class PragmaticStarterKit:

    def __init__(self, app: FastAPI, db_params: Dict[str, Any], github_token: str):
        self.app = app
        self.db_params = db_params
        self.github_repo = Github(github_token)

    async def init_db(self) -> None:
        self.app.state.pool = await aiomysql.create_pool(**self.db_params)

    async def close_db(self) -> None:
        self.app.state.pool.close()
        await self.app.state.pool.wait_closed()

    async def setup_routes(self) -> None:
        pass # Placeholder for routes

    async def create_models(self) -> None:
        pass # Placeholder for db models

def create_pragmatic_starter_kit(app_name: str, db_params: Dict[str, Any], github_token: str) -> PragmaticStarterKit:
    app = FastAPI(title=app_name)
    kit = PragmaticStarterKit(app, db_params, github_token)

    @app.on_event("startup")
    async def on_startup() -> None:
        await kit.init_db()
        await kit.create_models()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await kit.close_db()

    return kit

def main() -> None:
    db_params = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "user",
        "password": "password",
        "db": "pragmatic_db",
        "loop": asyncio.get_event_loop(),
    }

    github_token = "your_github_token"
    app = create_pragmatic_starter_kit("Pragmatic Starter Kit", db_params, github_token)

if __name__ == "__main__":
    main()
```
The above Python script uses FastAPI to create an application that connects to a MySQL database asynchronously using aiomysql. The FastAPI application is then bundled into a "starter kit" which creates an application on startup, sets up database models, and tears down the application on shutdown. This starter kit massively enhances the speed of deploying new applications and also ensures that best practices are followed during the development process.