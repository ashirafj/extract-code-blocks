import ast
from typing import List, Tuple

import astor

from extractor.blocks import Block
from extractor.nodes import Node


def extract(code: str, keep_indent: bool = False, debug_print: bool = False) -> List[Block]:
  """
  Extract all code blocks from Python source code based on abstract syntax tree.
  
  Note that this function extracts all inner code of a code block.
  It means that the lower code block appears in all higher code blocks.

  Example:
    Input:
    "
      if condition1:
        if condition2:
          if condition3:
            do_something()
    "
    Output:
    ["
      if condition1:
        if condition2:
          if condition3:
            do_something()
    ","
      if condition2:
        if condition3:
          do_something()
    ","
      if condition3:
        do_something()
    "]

  Params:
    code: Target source code to extract code blocks
    keep_indent: Whether to keep original indent depth in the result's code blocks. If False, the indent in the code blocks is reset to zero. Default is False.
    debug_print: Whether to output abstract syntax tree's nodes. Default is False.
  
  Returns:
    A list of code blocks.
    Each code block contains type of the code block, original source code of the code block, and line numbers representing the range.
  """
  tree = __get_tree(code)
  if debug_print:
    print(__get_formatted_tree_str(tree))
    print()

  all_nodes = __iter_child_nodes(tree)
  if debug_print:
    for node in all_nodes:
      print(node)
    print()

  blocks = __extract_blocks(all_nodes, code, keep_indent)
  return blocks

def __iter_child_nodes(tree: ast.AST, indent: int = 0) -> List[Node]:
  nodes = []

  for name, field in ast.iter_fields(tree):
    if isinstance(field, ast.AST):
      nodes += __iter_inner_child_nodes(name, field, indent)
    elif isinstance(field, list):
      for item in field:
        if isinstance(item, ast.AST):
          nodes += __iter_inner_child_nodes(name, item, indent)
  
  return nodes

def __iter_inner_child_nodes(name, field, indent) -> List[Node]:
  if "lineno" in field._attributes:
    lineno = field.lineno
    return [Node(name, field, indent, lineno)] + __iter_child_nodes(field, indent + 1)
  else:
    return [Node(name, field, indent)] + __iter_child_nodes(field, indent + 1)

def __extract_blocks(nodes: List[Node], code: str, keep_indent: bool) -> List[Block]:
  blocks = []
  for pos in range(len(nodes)):
    if __is_block(nodes[pos]):
      blocks.append(__extract_block(nodes, pos, code, keep_indent))
  return blocks

def __extract_block(nodes: List[Node], pos: int, code: str, keep_indent: bool) -> Block:
  base_node = nodes[pos]
  block_nodes = [base_node]
  for i in range(pos+1, len(nodes)):
    node = nodes[i]
    if node.indent > base_node.indent:
      block_nodes.append(node)
    else:
      break
  start_line, end_line = __get_range(block_nodes) # 0-indexed
  correspond_code = __get_correspond_code(code, keep_indent, start_line, end_line)
  return Block(base_node.type, correspond_code, start_line + 1, end_line + 1) # 1-indexed

def __get_range(nodes: List[Node]) -> Tuple[int, int]:
  linenos = [ node.lineno for node in nodes if node.lineno is not None ]
  start_line = min(linenos) - 1
  end_line = max(linenos) - 1
  return (start_line, end_line)

def __get_correspond_code(code: str, keep_indent: bool, start_line: int, end_line: int) -> str:
  code_lines = code.split("\n")
  correspond_code_lines = code_lines[start_line:end_line+1]

  if keep_indent:
    correspond_code = "\n".join(correspond_code_lines)
  else:    
    first_line = correspond_code_lines[0]
    indent_size = len(first_line) - len(first_line.lstrip())
    correspond_code_lines = [ line[indent_size:] for line in correspond_code_lines ]
    correspond_code = "\n".join(correspond_code_lines)
  return correspond_code

def __is_block(node: Node) -> bool:
  BLOCKS = [ "FunctionDef", "AsyncFunctionDef", "ClassDef", "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Try" ]
  # "body" excludes some improper code blocks like "elif"
  return node.type in BLOCKS and node.name == "body"

def __get_tree(code: str) -> ast.AST:
  tree = ast.parse(code)
  walker = astor.TreeWalk()
  walker.walk(tree)
  return tree

def __get_tree_str(tree: ast.AST) -> str:
  return ast.dump(tree, include_attributes=True, annotate_fields=True)

def __get_formatted_tree_str(tree: ast.AST) -> str:
  # TODO: refactoring
  tree_str = __get_tree_str(tree)
  INDENT_SIZE = 4
  current_indent_size = 0
  result_str = ""
  pos = 0
  while pos < len(tree_str):
    char = tree_str[pos]
    next_pos = pos + 1
    is_final = next_pos == len(tree_str)
    next_char = tree_str[next_pos] if not is_final else None

    if (char == "[" and next_char != "]"):
      current_indent_size += INDENT_SIZE
      result_str += "["
      result_str += "\n" + " " * current_indent_size
    elif (char == "(" and next_char != ")"):
      current_indent_size += INDENT_SIZE
      result_str += "("
      result_str += "\n" + " " * current_indent_size
    
    elif (char == "(" and next_char == ")"):
      result_str += "()"
      pos += 1
    elif (char == "[" and next_char == "]"):
      result_str += "[]"
      pos += 1
    
    elif char == "]":
      current_indent_size -= INDENT_SIZE
      result_str += "\n" + " " * current_indent_size
      result_str += "]"
    elif char == ")":
      current_indent_size -= INDENT_SIZE
      result_str += "\n" + " " * current_indent_size
      result_str += ")"
    
    elif char == "," and next_char == " ":
      result_str += ","
      result_str += "\n" + " " * current_indent_size
      pos += 1
    
    else:
      result_str += char

    pos += 1
    
  return result_str
