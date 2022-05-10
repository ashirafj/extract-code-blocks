import ast
from typing import Optional


class Node:
  def __init__(self, name: str, field: ast.AST, indent:int, lineno: Optional[int] = None) -> None:
    self.name = name
    self.field = field
    self.field_name = type(field).__name__
    self.indent = indent
    self.lineno = lineno
    print(self)
  
  def __str__(self) -> str:
    indent_str = "    " * self.indent
    if self.lineno is not None:
      return indent_str + self.name + ": " + str(self.field_name) + ", Indent: " + str(self.indent) + ", Line: " + str(self.lineno)
    else:
      return indent_str + self.name + ": " + str(self.field_name) + ", Indent: " + str(self.indent)

  def __repr__(self) -> str:
    return "Node(" + repr(self.name) + ", " + repr(self.field_name) + ", " + repr(self.indent) + ", " + repr(self.lineno) + ")"
