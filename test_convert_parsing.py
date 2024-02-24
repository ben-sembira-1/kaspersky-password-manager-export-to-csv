from pathlib import Path
import pytest
import convert


def test_parsing_txt_format():
    txt_format = Path("example.txt").read_text()
    assert convert.extract_passwords_from_txt_format(txt_format) == convert.KasperskyPasswordManagerEntriesSet(
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
