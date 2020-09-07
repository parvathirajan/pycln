"""
Pycln import statements nodes utility.
"""
import ast
from dataclasses import dataclass
from typing import List, Optional

# Constants.
DOT = "."


@dataclass(frozen=True)
class NodePosition:

    """Node position class."""

    #: Line numbers are 1-indexed.
    line: int

    #: Column numbers are 0-indexed.
    col: Optional[int] = None

    def __hash__(self):
        if self.col:
            return hash(self.line + self.col)
        return hash(self.line)


@dataclass(frozen=True)
class NodeLocation:

    """Node location class."""

    #: Line - Column.
    start: NodePosition

    #: Line - None.
    end: NodePosition

    def __hash__(self):
        return hash(hash(self.start) + hash(self.end))

    def __len__(self):
        return (self.end.line - self.start.line) + 1


@dataclass
class BaseImport:

    """Custom `ast.AST` node."""

    #: Location contains:
    #:  - `ast.AST.lineno`.
    #:  - `ast.AST.col_offset`.
    #:  - `ast.AST.end_lineno`.
    #:
    #: `ast.AST.end_col_offset` not included.
    location: NodeLocation

    #: `ast.Import.names`.
    names: List[ast.alias]


@dataclass
class Import(BaseImport):

    """Custom `ast.Import` node."""

    def __hash__(self):
        return hash(self.location)


@dataclass
class ImportFrom(BaseImport):

    """Custom `ast.ImportFrom` node."""

    #: `ast.ImportFrom.module`.
    module: Optional[str]

    #: `ast.ImportFrom.level`.
    level: int

    @property
    def relative_name(self) -> str:
        """Node relative name."""
        dots = DOT * self.level
        if self.module:
            return f"{dots}{self.module}"
        return dots

    def __hash__(self):
        return hash(self.location)
