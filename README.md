# extract-code-blocks

A script to extract code blocks (such as if, for, while, def, class, etc.) from Python source code based on Abstract Syntax Tree (AST).

## How to Use

```sh
usage: extract.py [-h] [--input INPUT] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Target source code file to extract code blocks
  --output OUTPUT, -o OUTPUT
                        Target JSON file to save the result
```

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

## Example

### Input
```py
if condition1: # condition 1
    if condition2: # condition 2
        if condition3: # condition 3
            # do something here
            do_something()
```

### Output
```json
[
    {
        "type": "If",
        "code": "if condition1: # condition 1\n    if condition2: # condition 2\n        if condition3: # condition 3\n            # do something here\n            do_something()",
        "start": 1,
        "end": 5
    },
    {
        "type": "If",
        "code": "if condition2: # condition 2\n    if condition3: # condition 3\n        # do something here\n        do_something()",
        "start": 2,
        "end": 5
    },
    {
        "type": "If",
        "code": "if condition3: # condition 3\n    # do something here\n    do_something()",
        "start": 3,
        "end": 5
    }
]
```

### Note

`type` can be `[ "FunctionDef", "AsyncFunctionDef", "ClassDef", "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Try" ]`

`start` and `end` is 1-indexed value. Same as the line number displayed in editor.
