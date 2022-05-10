import ast
from typing import Optional

class Node:
  def __init__(self, name: str, field: ast.AST, indent:int, line_number: Optional[int] = None) -> None:
    self.name = name
    self.field = field
    self.indent = indent
    self.line_number = line_number
    print(self)
  
  def __str__(self) -> str:
    indent_str = "    " * self.indent
    if self.name == "body":
      return indent_str + self.name + ": " + str(type(self.field)) + ", Indent: " + str(self.indent) + ", Line: " + str(self.line_number)
    else:
      return indent_str + self.name + ": " + str(type(self.field)) + ", Indent: " + str(self.indent)

  def __repr__(self) -> str:
    return "Node(" + repr(self.name) + ", " + repr(type(self.field).__name__) + ", " + repr(self.indent) + ", " + repr(self.line_number) + ")"
