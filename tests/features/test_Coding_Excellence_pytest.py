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


def test_functions_perform_as_expected():
    assert is_prime(7)
    assert not is_prime(1)
    assert not is_prime(9)


def test_cli_game_contract():
    assert play_guessing_game(42)
    assert not play_guessing_game(41)


def test_request_response_contract():
    assert handle_get("/") == (200, b"Hello, world")
    assert handle_get("/missing") == (404, b"Not found")
