import pyperclip


def paste_into_fgn():
    # print(f"Pasting into fgn {pyperclip.paste()}")
    return pyperclip.paste()


def copy_into_clipboard(text):
    # print(f"Copying into clipboard {text}")
    pyperclip.copy(text)
