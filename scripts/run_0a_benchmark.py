#!/usr/bin/env python3
"""Minimal CLI for the Toy Model 0A benchmark.

By default, writes the JSON report to stdout. Pass --output to write to a file
instead; the default path never creates a file, so nothing is versioned in Git
by simply running this script.
"""

from __future__ import annotations

import argparse
import json
import sys

from cosmobox_c_model.models.model0a.benchmark import run_benchmark_0a


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Toy Model 0A benchmark.")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to write the JSON report to (default: stdout).",
    )
    args = parser.parse_args(argv)

    report = run_benchmark_0a()
    payload = json.dumps(report, indent=2, sort_keys=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.write("\n")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
