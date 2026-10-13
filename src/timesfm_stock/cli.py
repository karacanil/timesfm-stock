import argparse
import json
from pathlib import Path

from .experiment import collect, evaluate
from .report import report


def main():
    parser = argparse.ArgumentParser(description="Prospective TimesFM 3.0 stock forecast experiment")
    parser.add_argument("command", choices=["forecast", "evaluate", "report", "daily"])
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    if args.command in {"evaluate", "daily"}:
        evaluate(args.output)
    if args.command in {"forecast", "daily"}:
        try:
            config = json.loads(args.config.read_text())
            collect(config, args.output)
        finally:
            if args.command == "daily":
                report(args.output)
    if args.command in {"report", "evaluate"}:
        report(args.output)


if __name__ == "__main__":
    main()
