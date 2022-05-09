import ast
from typing import List

import astor

from extractor.code_block import CodeBlock


def extract(code: str) -> List[CodeBlock]:
  tree = __get_tree(code)
  print(ast.dump(tree))
  print()

  restored_code = __get_code(tree)
  print(restored_code)
  print()

  return [ CodeBlock(code, "") ]

def __get_tree(code: str) -> ast.AST:
  tree = ast.parse(code)
  walker = astor.TreeWalk()
  walker.walk(tree)
  return tree

def __get_code(tree: ast.AST) -> str:
  return astor.to_source(tree)
