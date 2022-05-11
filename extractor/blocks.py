from typing import List

from extractor.nodes import Node


class Block:
  def __init__(self, block_type: str , nodes: List[Node], code: str):
    """
    Params:
      block_type: Type of the code block including [ "FunctionDef", "AsyncFunctionDef", "ClassDef", "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Try" ]
      nodes: Inner nodes of the code block
      code: Raw code that is corresponding to the code block
    """
    self.block_type = block_type
    self.nodes = nodes
    self.code = code

  def __str__(self):
    return self.code
  
  def __repr__(self):
    return "Block(" + repr(self.block_type) + ", " + repr(self.nodes) + ", " + repr(self.code) + ")"
