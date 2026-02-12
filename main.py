import sys
from dramatiq.cli import main

if __name__ == "__main__":
    sys.argv = ["dramatiq", "tasks"]
    main()
