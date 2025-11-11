import sys
import signal
import repl as repl
import interpreter

def sigint_handler(sig, frame):
    sys.exit(0)

def main() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
    if len(sys.argv) == 1:
        repl.get_input()
    else:
        interpreter.execute(sys.argv[1])


if __name__ == "__main__":
    main()
