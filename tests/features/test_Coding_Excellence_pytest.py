from pytest_bdd import given, scenarios, then, when


scenarios("Coding_Excellence.feature")


def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    return all(number % candidate for candidate in range(2, int(number**0.5) + 1))


def play_guessing_game(guess: int, secret: int = 42) -> bool:
    return guess == secret


def handle_get(path: str) -> tuple[int, bytes]:
    if path == "/":
        return 200, b"Hello, world"
    return 404, b"Not found"


@given("a set of requirements", target_fixture="function_state")
def function_requirements():
    return {"number": 7}


@when("the code is written")
def write_code(function_state):
    function_state["is_prime"] = is_prime(function_state["number"])


@then("the functions should perform as expected")
def verify_function(function_state):
    assert function_state["is_prime"] is True


@given("a game concept", target_fixture="game_state")
def game_concept():
    return {"secret": 42, "guess": 42}


@when("the code is executed")
def execute_game(game_state):
    game_state["result"] = play_guessing_game(
        game_state["guess"],
        game_state["secret"],
    )


@then("the CLI game should be playable")
def verify_game(game_state):
    assert game_state["result"] is True


@given("server requirements", target_fixture="server_state")
def server_requirements():
    return {"path": "/"}


@when("the server is set up")
def setup_server(server_state):
    status, body = handle_get(server_state["path"])
    server_state.update(status=status, body=body)


@then("it should handle requests and responses correctly")
def verify_server(server_state):
    assert server_state == {"path": "/", "status": 200, "body": b"Hello, world"}
