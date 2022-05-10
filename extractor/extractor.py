import ast
from typing import List

import astor

from extractor.code_block import CodeBlock
from extractor.nodes import Node


def extract(code: str) -> List[CodeBlock]:
  tree = __get_tree(code)
  print(__get_formatted_tree_str(tree))
  print()

  restored_code = __get_code(tree)
  print(restored_code)
  print()

  all_nodes = __iter_child_nodes(tree)
  print(all_nodes)

  return [ CodeBlock(code, "") ]

def __iter_child_nodes(tree, indent=1) -> List[Node]:
  if indent == 1:
    print(tree)
  
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
  if name == "body":
    lineno = field.lineno
    # print(indent_str + name + ": " + str(type(field)) + ", Line: " + str(lineno))
    return [Node(name, field, indent, lineno)] + __iter_child_nodes(field, indent + 1)
  else:
    # print(indent_str + name + ": " + str(type(field)))
    return [Node(name, field, indent)] + __iter_child_nodes(field, indent + 1)

def __get_tree(code: str) -> ast.AST:
  tree = ast.parse(code)
  walker = astor.TreeWalk()
  walker.walk(tree)
  return tree

def __get_code(tree: ast.AST) -> str:
  return astor.to_source(tree)

def __get_tree_str(tree: ast.AST) -> str:
  return ast.dump(tree, include_attributes=True, annotate_fields=True)

def __get_formatted_tree_str(tree: ast.AST) -> str:
  tree_str = __get_tree_str(tree)
  INDENT_SIZE = 4
  current_indent_size = 0
  result_str = ""
  pos = 0
  while pos < len(tree_str):
    char = tree_str[pos]
    previous_pos = pos - 1
    next_pos = pos + 1
    is_first = pos == 0
    is_final = next_pos == len(tree_str)
    previous_char = tree_str[previous_pos] if not is_first else None
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
