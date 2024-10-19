from typing import Optional, override

from colorama import Fore
from pydantic import BaseModel
from rag.core import Task


class ZoteroQAInput(BaseModel):
    query: str
    exact_search_terms: Optional[list[str]] = None


class UserInputTask(Task[ZoteroQAInput]):
    name = "UserInputTask"

    def __init__(self):
        super().__init__(self.name)

    @override
    def run(self) -> ZoteroQAInput:
        query = input(f"{Fore.BLUE}Query: {Fore.RESET}")
        exact_search_terms = input(f"{Fore.BLUE}Exact search terms, separated by commas (optional): {Fore.RESET}")
        exact_search_terms = exact_search_terms.split(",") if exact_search_terms else None

        return ZoteroQAInput(query=query, exact_search_terms=exact_search_terms)
