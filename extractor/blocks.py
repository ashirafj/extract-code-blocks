class Block:
  def __init__(self, type: str, code: str, start_line: int, end_line: int):
    """
    Params:
      type: Type of the code block including [ "FunctionDef", "AsyncFunctionDef", "ClassDef", "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Try" ]
      code: Raw code that is corresponding to the code block
      start_line: Line number that starts the code block
      end_line: Line number that ends the code block
    """
    self.type = type
    self.code = code
    self.start_line = start_line
    self.end_line = end_line

  def __str__(self):
    return self.code
  
  def __repr__(self):
    return "Block(" + repr(self.type) + ", " + repr(self.start_line) + "-" + repr(self.end_line) + ", " + repr(self.code) + ")"
