import sys
import signal
import repl as repl

def sigint_handler(sig, frame):
    sys.exit(0)

def main() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
    if len(sys.argv) == 1:
        repl.get_input()


if __name__ == "__main__":
    main()
