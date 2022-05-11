# extract-code-blocks

A script to extract code blocks (such as if, for, while, def, class, etc.) from Python source code based on Abstract Syntax Tree (AST).

## How to Use

### Input

`extract.py` reads the source code from a specified file by an argument.

```sh
python extract.py -i code.py
```

or, it also receives the target source code by pipe (standard input).

```sh
cat code.py | python extract.py
```

### Output

`extract.py` saves the result to a specified file as JSON format.

```sh
cat code.py | python extract.py -o result.json
```

or, it also supports output in standard output.

```sh
cat code.py | python extract.py > result.json
```
