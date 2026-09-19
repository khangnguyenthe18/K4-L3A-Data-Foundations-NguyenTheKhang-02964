from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """
    A text document with optional metadata.

    Fields:
        id:       Unique identifier string.
        content:  The raw text content.
        metadata: Arbitrary key-value metadata (e.g. source, date, author).
    """

    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
