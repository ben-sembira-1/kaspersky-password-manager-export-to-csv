from pathlib import Path
import pytest
import convert


def test_extract_sections_from_txt_format():
    entry1 = "content: abc\nmore stuff"
    entry2 = "hey there -> abc\n:>)"
    entry3 = "more stuff"
    entry4 = "def a():\nreturn 0"
    entry5 = "pure\nrandom\nstuff"
    entry6 = "surely_random"
    websites_text = \
        f"""\
{entry1}

---

{entry2}\
"""
    applications_text = \
        f"""\
{entry3}

---

{entry4}\
"""
    notes_text = \
        f"""\
{entry5}

---

{entry6}\
"""
    raw = \
        f"""\
Websites

{websites_text}

---

Applications

{applications_text}

---

Notes

{notes_text}

---

"""
    assert convert.extract_websites_from_txt_format(raw) == websites_text
    assert convert.extract_applications_from_txt_format(
        raw) == applications_text
    assert convert.extract_notes_from_txt_format(raw) == notes_text


@pytest.mark.parametrize("line,key,value", [
    ("key1: value", "key1", "value"),
    ("key2: ", "key2", ""),
    ("key3: a b c", "key3", "a b c"),
    ("key4: a: b", "key4", "a: b"),
])
def test_key_value_from_line(line: str, key: str, value: str):
    assert convert.key_value_from_line(line) == (key, value)


def test_colon_separated_format_parser():
    raw = \
        """

key1: value number 1
key2: value2
key3: 1234



"""
    assert convert.parse_colon_separated_key_value_pairs(raw) == {
        "key1": "value number 1",
        "key2": "value2",
        "key3": "1234"
    }


def test_parsing_txt_format():
    txt_format = Path("example.txt").read_text()
    assert convert.extract_entries_from_txt_format(txt_format) == convert.KasperskyPasswordManagerEntriesSet(
        websites=[
            convert.KasperskyWebsiteEntry(
                website_name="Account Jetbrains",
                website_url="https://account.jetbrains.com",
                login_name="",
                login="userName1",
                password="password1",
                comment=""
            ),
            convert.KasperskyWebsiteEntry(
                website_name="accounts.google.com",
                website_url="https://accounts.google.com",
                login_name="",
                login="userName2.1",
                password="password2.1",
                comment=""
            ),
            convert.KasperskyWebsiteEntry(
                website_name="accounts.google.com",
                website_url="https://accounts.google.com",
                login_name="",
                login="userName2.2",
                password="password2.2",
                comment=""
            ),
        ],
        applications=[
            convert.KasperskyApplicationEntry(
                application_name="Dji.com",
                login_name="",
                login="userName3",
                password="password3",
                comment=""
            ),
            convert.KasperskyApplicationEntry(
                application_name="App2",
                login_name="",
                login="userName4",
                password="password4",
                comment=""
            ),
            convert.KasperskyApplicationEntry(
                application_name="App3",
                login_name="",
                login="userName5",
                password="password5",
                comment=""
            ),
        ],
        notes=[
            convert.KasperskyNoteEntry(
                note_name="My lovely note",
                text="1234"
            )
        ]
    )
