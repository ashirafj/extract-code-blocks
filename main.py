from extractor import extractor

if __name__ == "__main__":
  filename = "samples/sample.py"
  with open(filename, "r") as f:
    code = f.read()
  blocks = extractor.extract(code)

  for block in blocks:
    print("Comment")
    print(block.comment)
    print("Code")
    print(block.code)
