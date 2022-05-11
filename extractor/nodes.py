import ast
from typing import Optional


class Node:
  def __init__(self, name: str, field: ast.AST, indent:int, lineno: Optional[int] = None) -> None:
    """
    Params:
      name: Node's name
      field: Node
      indent: Depth of indent (0-indexed)
      lineno: Line number (some node doesn't have)
    """
    self.name = name
    self.field = field
    self.type = type(field).__name__
    self.indent = indent
    self.lineno = lineno
  
  def __str__(self) -> str:
    indent_str = "    " * self.indent
    if self.lineno is not None:
      return indent_str + self.name + ": " + str(self.type) + ", Indent: " + str(self.indent) + ", Line: " + str(self.lineno)
    else:
      return indent_str + self.name + ": " + str(self.type) + ", Indent: " + str(self.indent)

  def __repr__(self) -> str:
    return "Node(" + repr(self.name) + ", " + repr(self.type) + ", " + repr(self.indent) + ", " + repr(self.lineno) + ")"
