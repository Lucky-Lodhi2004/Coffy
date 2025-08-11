# coffy/nosql/doclist.py
# author: nsarathy

from .atomicity import _atomic_save


class DocList:
    """
    A class to represent a list of documents with additional utility methods.
    Provides methods to iterate, access by index, get length, and convert to JSON.
    """

    def __init__(
        self, docs: list[dict], sort_key: str = None, sort_reverse: bool = False
    ):
        """
        Initialize the DocList with a list of documents.
        docs -- A list of documents (dictionaries) to store in the DocList.
        sort_key -- The key to sort the documents by.
        sort_reverse -- Whether to sort in descending order.
        """
        self._docs = docs
        if sort_key:
            def sort_key_func(doc):
                val = doc.get(sort_key)
                if val is None:
                    return (3, None)
                elif isinstance(val, (int, float)):
                    return (0, val)
                elif isinstance(val, str):
                    return (1, val)
                else:
                    return (2, str(val))
            
            self._docs.sort(key=sort_key_func, reverse=sort_reverse)
            # self._docs.sort(
            #     key=lambda doc: (doc.get(sort_key) is None, doc.get(sort_key)),
            #     reverse=sort_reverse,
            # )

    def __iter__(self):
        """
        Return an iterator over the documents in the DocList.
        """
        return iter(self._docs)

    def __getitem__(self, index):
        """
        Get a document by index.
        index -- The index of the document to retrieve.
        Returns the document at the specified index.
        """
        return self._docs[index]

    def __len__(self):
        """
        Get the number of documents in the DocList.
        Returns the count of documents.
        """
        return len(self._docs)

    def __repr__(self):
        """
        Return a string representation of the DocList.
        If the DocList is empty, it returns "<empty result>".
        Otherwise, it formats the documents as a table with headers.
        """
        if not self._docs:
            return "<empty result>"

        all_keys = []
        for doc in self._docs:
            for key in doc.keys():
                if key not in all_keys:
                    all_keys.append(key)

        keys = all_keys
        header = " | ".join(keys)
        line = "-+-".join("-" * len(k) for k in keys)
        rows = []
        for doc in self._docs:
            row = " | ".join(str(doc.get(k, "")) for k in keys)
            rows.append(row)
        return f"{header}\n{line}\n" + "\n".join(rows)

    def to_json(self, path: str):
        """
        Save the documents in the DocList to a JSON file.
        path -- The file path to save the documents.
        """
        _atomic_save(self._docs, path)

    def as_list(self):
        """
        Convert the DocList to a regular list of documents.
        """
        return self._docs
