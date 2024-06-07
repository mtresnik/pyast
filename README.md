# pyast
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)]()
[![version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg?style=flat-square)](https://makeapullrequest.com)
<hr>
A python implementation of an abstract syntax tree.

### Sample Code

```python
from pyast.parser import parse_operation
from pyast.constant import Constant
from pyast.variable import Variable

def parse_example():
    to_parse = "a * bc + 123 / sin(3.1415 * n) ^ log_(2, 8) - e"
    operation = parse_operation(to_parse)
    
    # replace variables
    evaluated = operation.evaluate(Variable("a"), Constant(5.0))
    
    # replace functions
    to_replace = parse_operation("sin(3.1415 * n)")
    evaluated2 = operation.evaluate(to_replace, Constant(2.0))

if __name__ == '__main__':
    parse_example()
```