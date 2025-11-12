# SLSIP

SLisp, standing for Simplified Lisp (or rather Sh*tty Lisp once you get to look at the code), is an interpreter for a simplifed version of Lisp.

## Installation

Simply clone the directory, and run the following command in the root directory where the `pyproject.toml` is located.

```shell
pip install -e .
```

You can verify that the installation was successful by running the `slisp` command in the terminal.

## Usage

There are two ways to run SLisp programs. The first one is via a REPL. To achieve this, simply run the `slisp` command with no arguments.

```shell
~$ slisp
SLISP v0.1.0
>>> (+ 1 2)
3
```

You can also pass in the path to a slisp file as an argument to the `slisp` command. This will run the file.

```shell
~$ slisp test/helloworld.slisp
Hello World
```

## Examples

Here is a simple example of FizzBuzz. There are more examples under the `test` directory.

```lisp
(defunc fizzbuzz (n) 
    (for i (in-range 1 n) 
        (cond
            ((= 0 (% i 15))
                (print "FizzBuzz")
            )
            ((= 0 (% i 3))
                (print "Fizz")
            )
            ((= 0 (% i 5))
                (print "Buzz")
            )
            (True (print i))
        )
    )
)

;; Run the FizzBuzz game from numbers 1 to 30
(fizzbuzz 31)
```