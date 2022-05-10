from typing import List

from extractor.nodes import Node


class Block:
  def __init__(self, block_type: str , nodes: List[Node], code: str):
    self.block_type = block_type
    self.nodes = nodes
    self.code = code
