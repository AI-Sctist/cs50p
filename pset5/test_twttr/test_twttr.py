from twttr import shorten


def test_shorten_blank():
    assert shorten("") == ""


def test_shorten_all_char():
    default = []
    shorter = []

    for i in range(32, 126):
        default.append(chr(i))
        if chr(i) not in "aeiouAEIOU":
            shorter.append(chr(i))

    assert shorten("".join(default)) == "".join(shorter)
