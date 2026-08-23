from types import SimpleNamespace

from fgn.completion.history import History, hchat


class FakeCompletions:
    def create(self, **kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="reply", function_call=None))])


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_history_import_has_no_provider_actuation_and_hchat_is_explicit():
    history = History([{"role": "user", "content": "hello"}])
    result = hchat(history, prompt="respond", client=FakeClient())
    assert len(history) == 1
    assert result.last() == {"role": "assistant", "content": "reply"}
