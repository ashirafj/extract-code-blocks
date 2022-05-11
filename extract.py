from extractor import extractor
from argparse import ArgumentParser, FileType
import json

def main():
  parser = ArgumentParser()
  parser.add_argument("--input", "-i", type=FileType("r", encoding="utf8"), default="-", help="Target source code file to extract code blocks")
  parser.add_argument("--output", "-o", type=FileType("w", encoding="utf8"), default="-", help="Target JSON file to save the result")
  args = parser.parse_args()
  code = args.input.read()
  blocks = extractor.extract(code)
  output_data = [ { "type": block.type, "code": block.code, "start": block.start_line, "end": block.end_line } for block in blocks ]
  json.dump(output_data, args.output)

if __name__ == "__main__":
  main()
