class Block:
  def __init__(self, type: str, code: str):
    """
    Params:
      type: Type of the code block including [ "FunctionDef", "AsyncFunctionDef", "ClassDef", "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Try" ]
      code: Raw code that is corresponding to the code block
    """
    self.type = type
    self.code = code

  def __str__(self):
    return self.code
  
  def __repr__(self):
    return "Block(" + repr(self.type) + ", " + repr(self.code) + ")"
