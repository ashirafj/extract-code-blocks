from extractor import extractor

if __name__ == "__main__":
  filepath = input()
  with open(filepath, "r") as f:
    code = f.read()
  blocks = extractor.extract(code)

  for block in blocks:
    print("Type:", block.type)
    print(block.code)
    print()
  