"""
Fill a PDF form using data from JSON or YAML.

This script reads a dictionary of field values from a JSON or YAML file and
writes them into an AcroForm PDF.  It relies on PyPDFForm for high‑level
form filling, supports Adobe appearance regeneration, and optionally
flattens the output (removes the form fields).

See README.md for usage instructions.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

try:
    from PyPDFForm import PdfWrapper  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "PyPDFForm is required for this script. Install it with `pip install PyPDFForm`."
    ) from exc


def load_data(path: Path) -> Dict[str, Any]:
    """Load a dict from a JSON or YAML file based on extension."""
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError(
                "PyYAML is not installed. Install it with `pip install pyyaml` or use a JSON file."
            )
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    # default to JSON
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args(argv: Any = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path(__file__).parent / "2025 Swiss Tax Questionnaire (Departure)_A_EN.pdf",
        help="Path to the source PDF form (defaults to the included questionnaire)",
    )
    parser.add_argument(
        "--data",
        type=Path,
        required=True,
        help="Path to JSON or YAML file containing field values",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("filled.pdf"),
        help="Filename for the output PDF (default: filled.pdf)",
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten the form (remove fields) to make the output non‑editable",
    )
    return parser.parse_args(argv)


def main(argv: Any = None) -> None:
    args = parse_args(argv)
    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")
    if not args.data.exists():
        raise SystemExit(f"Data file not found: {args.data}")

    data = load_data(args.data)
    # Ensure keys are strings
    if not isinstance(data, dict):
        raise SystemExit("Data file must contain a JSON/YAML object at its top level")

    wrapper = PdfWrapper(str(args.pdf), adobe_mode=True)
    # Fill and optionally flatten
    filled = wrapper.fill(data, flatten=args.flatten)
    filled.write(str(args.output))
    print(f"Wrote filled PDF to {args.output}")


if __name__ == "__main__":
    main()