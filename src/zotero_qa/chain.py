from zotero_qa.input import UserInputTask

from rag.core import Chain


zotero_qa_chain = Chain(
    UserInputTask(),
    name="ZoteroQAChain"
)
