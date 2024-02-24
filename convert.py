from pydantic import BaseModel, Field
from pathlib import Path
import sys
from typing import Dict, List, Tuple

from pandas import DataFrame


def key_value_from_line(key_value: str) -> Tuple[str, str]:
    splitted = key_value.split(sep=": ", maxsplit=1)
    if len(splitted) == 1:
        return splitted[0], ""

    key, value = splitted
    return key, value


def parse_colon_separated_key_value_pairs(entry: str) -> Dict[str, str]:
    stripped = entry.strip("\n")
    lines = stripped.splitlines()
    key_value_pairs = [key_value_from_line(line) for line in lines]
    return {pair[0]: pair[1] for pair in key_value_pairs}


def parse_entries_section(txt: str) -> List[Dict[str, str]]:
    entries = txt.split("---")
    return [parse_colon_separated_key_value_pairs(entry) for entry in entries]


class KasperskyWebsiteEntry(BaseModel):
    website_name: str = Field(alias="Website name")
    website_url: str = Field(alias="Website URL")
    login_name: str = Field(alias="Login name")
    login: str = Field(alias="Login")
    password: str = Field(alias="Password")
    comment: str = Field(alias="Comment")


class KasperskyApplicationEntry(BaseModel):
    application_name: str = Field(alias="Application")
    login_name: str = Field(alias="Login name")
    login: str = Field(alias="Login")
    password: str = Field(alias="Password")
    comment: str = Field(alias="Comment")


class KasperskyNoteEntry(BaseModel):
    note_name: str = Field(alias="Name")
    text: str = Field(alias="Text")


class KasperskyPasswordManagerEntriesSet(BaseModel):
    websites: List[KasperskyWebsiteEntry]
    applications: List[KasperskyApplicationEntry]
    notes: List[KasperskyNoteEntry]


WEBSITES_IDENTIFIER = "Websites\n\n"
APPLICATIONS_IDENTIFIER = "\n\n---\n\nApplications\n\n"
NOTES_IDENTIFIER = "\n\n---\n\nNotes\n\n"


def extract_websites_from_txt_format(text_file_content: str) -> str:
    start_index = text_file_content.find(
        WEBSITES_IDENTIFIER) + len(WEBSITES_IDENTIFIER)
    end_index = text_file_content.find(APPLICATIONS_IDENTIFIER)
    return text_file_content[start_index: end_index].strip("\n")


def extract_applications_from_txt_format(text_file_content: str) -> str:
    start_index = text_file_content.find(
        APPLICATIONS_IDENTIFIER) + len(APPLICATIONS_IDENTIFIER)
    end_index = text_file_content.find(NOTES_IDENTIFIER)
    return text_file_content[start_index: end_index].strip("\n")


def extract_notes_from_txt_format(text_file_content: str) -> str:
    EOF_IDENTIFIER = "\n\n---\n"
    start_index = text_file_content.find(
        NOTES_IDENTIFIER) + len(NOTES_IDENTIFIER)
    end_index = text_file_content.rfind(EOF_IDENTIFIER)
    return text_file_content[start_index:end_index].strip("\n")


def extract_passwords_from_txt_format(txt_file_content: str) -> KasperskyPasswordManagerEntriesSet:
    websites_dicts = parse_entries_section(
        extract_websites_from_txt_format(txt_file_content))
    applications_dicts = parse_entries_section(
        extract_applications_from_txt_format(txt_file_content))
    notes_dicts = parse_entries_section(
        extract_notes_from_txt_format(txt_file_content))
    print(f"{notes_dicts=}")

    return KasperskyPasswordManagerEntriesSet(
        websites=[KasperskyWebsiteEntry(
            **entry) for entry in websites_dicts],
        applications=[KasperskyApplicationEntry(
            **entry) for entry in applications_dicts],
        notes=[KasperskyNoteEntry(
            **entry) for entry in notes_dicts],
    )


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
