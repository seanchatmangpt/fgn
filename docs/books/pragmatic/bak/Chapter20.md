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