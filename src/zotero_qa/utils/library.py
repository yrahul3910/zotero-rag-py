import os
import platform
import sqlite3

from pathlib import Path
from typing import Generator

from pydantic import BaseModel


class ZoteroItemMetadata(BaseModel):
    libraryKey: str
    title: str
    abstract: str


def get_zotero_library_path() -> Path:
    cur_os = platform.system()

    match cur_os:
        case "Darwin" | "Linux":
            return Path(os.path.expanduser("~/Zotero/"))
        case "Windows":
            # Assume Windows 7+
            return Path(os.path.expanduser("~\\Zotero\\"))
        case _:
            raise ValueError(f"Unsupported OS: {cur_os}")


def parse_zotero_library() -> Generator[ZoteroItemMetadata]:
    lib_path = Path(get_zotero_library_path() / "zotero.sqlite")
    conn = sqlite3.connect(lib_path)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT items.key AS libraryKey,
           MAX(CASE WHEN fieldsCombined.fieldName = 'title' THEN itemDataValues.value END) AS title,
           MAX(CASE WHEN fieldsCombined.fieldName = 'abstract' THEN itemDataValues.value END) AS abstract
        FROM items
        INNER JOIN itemData ON items.itemID = itemData.itemID
        INNER JOIN fieldsCombined ON itemData.fieldID = fieldsCombined.fieldID
        INNER JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE fieldsCombined.fieldName IN ('title', 'abstract')
        GROUP BY items.key
        LIMIT 5;
    """)

    if cursor.rowcount == 0:
        raise ValueError("Zotero library is empty.")

    for row in cursor.fetchall():
        yield ZoteroItemMetadata(libraryKey=row[0], title=row[1], abstract=row[2])
