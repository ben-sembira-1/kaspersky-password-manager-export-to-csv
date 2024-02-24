from dataclasses import dataclass
from pathlib import Path
import sys
from typing import List

from pandas import DataFrame


@dataclass
class KasperskyWebsiteEntry:
    website_name: str
    website_url: str
    login_name: str
    login: str
    password: str
    comment: str


@dataclass
class KasperskyApplicationEntry:
    application_name: str
    login_name: str
    login: str
    password: str
    comment: str


@dataclass
class KasperskyNoteEntry:
    note_name: str
    text: str


@dataclass
class KasperskyPasswordManagerEntriesSet:
    websites: List[KasperskyWebsiteEntry]
    applications: List[KasperskyApplicationEntry]
    notes: List[KasperskyNoteEntry]


def extract_passwords_from_txt_format(txt_file_content: str) -> KasperskyPasswordManagerEntriesSet:
    raise NotImplementedError()


def create_df_from_passwords(passwords: KasperskyPasswordManagerEntriesSet) -> DataFrame:
    raise NotImplementedError()


def convert_txt_file_to_google_passwords_compatible_csv(txt_file_path: Path):
    passwords = extract_passwords_from_txt_format(txt_file_path.read_text())
    passwords_table = create_df_from_passwords(passwords)
    passwords_table.to_csv(f"{txt_file_path.name}.csv")


def main(arguments: List[str]):
    assert len(arguments) == 2, f"USAGE: {__file__} dd-mm-yyyy.txt"
    txt_file_path = Path(arguments[1])
    assert txt_file_path.exists(
    ), f"The file {txt_file_path.as_uri} does not exist"
    convert_txt_file_to_google_passwords_compatible_csv(txt_file_path)


if __name__ == "__main__":
    main(sys.argv)
