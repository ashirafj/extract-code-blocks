from extractor import extractor

if __name__ == "__main__":
  code = """
class CLASS1:
  def __init__(self):
    pass
  
  def METHOD1(self):
    def INNER1():
      pass
    INNER1()

def fizz_buzz(n):
  if not isinstance(n, int) or n < 1:
    raise ValueError("n must be a positive integer")

  for i in range(1, n + 1):
    if i % 15 == 0:
      print("FizzBuzz")
    elif i % 3 == 0:
      print("Fizz")
    elif i % 5 == 0:
      print("Buzz")
    else:
      print(i)
  else:
    print("FizzBuzz End")

if __name__ == "__main__":
  try:
    while (True):
      fizz_buzz(100)
  except KeyboardInterrupt:
    print("Canceled")
  finally:
    print("Script End")
"""
  print(code)
  blocks = extractor.extract(code, debug_print=True)

  for block in blocks:
    print("Type:", block.block_type)
    print(block.code)
    print()
