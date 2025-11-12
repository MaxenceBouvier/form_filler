"""
Generate a stub mapping from a PDF form.

This script inspects an AcroForm‑enabled PDF using PyPDFForm and
emits a dictionary of all field names with sensible default values.

* Text fields -> ""
* Boolean/checkbox fields -> False

The resulting stub can be saved as JSON and/or YAML and used as input
for manual editing or AI‑powered filling.  See README.md for details.
"""

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]  # YAML output will be disabled if PyYAML isn't installed

try:
    from PyPDFForm import PdfWrapper
except ImportError as exc:
    raise SystemExit(
        "PyPDFForm is required for this script. Install it with `pip install PyPDFForm`."
    ) from exc


def build_stub(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a dict of field_name -> default value based on the schema."""
    stub: dict[str, Any] = {}
    properties = schema.get("properties", {})
    for field_name, meta in properties.items():
        field_type = meta.get("type")
        # If the type is a list, pick the first
        if isinstance(field_type, list):
            field_type = field_type[0]
        if field_type == "boolean":
            stub[field_name] = False
        else:
            # default to empty string for text/numeric fields
            stub[field_name] = ""
    return stub


def write_json(data: dict[str, Any], path: Path) -> None:
    """Write a dict to a JSON file with UTF‑8 encoding and indentation."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_yaml(data: dict[str, Any], path: Path) -> None:
    """Write a dict to a YAML file.  Requires PyYAML."""
    if yaml is None:
        raise RuntimeError(
            "PyYAML is not installed. Install it with `pip install pyyaml` to enable YAML output."
        )
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def parse_args(argv: Any = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path(__file__).parent / "2025 Swiss Tax Questionnaire (Departure)_A_EN.pdf",
        help="Path to the source PDF form (defaults to the included questionnaire)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path("stub.json"),
        help="Filename for the JSON stub (default: stub.json)",
    )
    parser.add_argument(
        "--yaml",
        type=Path,
        default=Path("stub.yaml"),
        help="Filename for the YAML stub (default: stub.yaml)"
        + (" (requires PyYAML)" if yaml is not None else " (YAML output disabled)"),
    )
    return parser.parse_args(argv)


def main(argv: Any = None) -> None:
    args = parse_args(argv)
    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")

    # Inspect the form
    wrapper = PdfWrapper(str(args.pdf))
    schema = wrapper.schema
    stub = build_stub(schema)

    # Write JSON
    write_json(stub, args.json)
    print(f"Wrote JSON stub to {args.json}")

    # Write YAML if requested and supported
    if yaml is not None:
        write_yaml(stub, args.yaml)
        print(f"Wrote YAML stub to {args.yaml}")
    else:
        print(
            "PyYAML not installed; YAML output skipped. Install with `pip install pyyaml` and rerun."
        )


if __name__ == "__main__":
    main()
