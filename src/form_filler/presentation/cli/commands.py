"""CLI command implementations."""

import argparse
from pathlib import Path

from form_filler.application.extract_fields import ExtractFieldsUseCase
from form_filler.container import container, setup_container
from form_filler.domain.interfaces import FieldCategorizer, PDFProcessor


def extract_required_info():
    """CLI command to extract required fields from a PDF."""
    parser = argparse.ArgumentParser(
        description="Extract required field information from a PDF form"
    )
    parser.add_argument("pdf", type=Path, help="Path to the PDF form")
    parser.add_argument("--json", type=Path, help="Output JSON file path")
    parser.add_argument("--yaml", type=Path, help="Output YAML file path")
    parser.add_argument(
        "--categorize",
        action="store_true",
        help="Categorize fields by type (personal, address, etc.)",
    )

    args = parser.parse_args()

    # Setup dependency container
    setup_container()

    # Resolve dependencies
    pdf_processor = container.resolve(PDFProcessor)
    categorizer = None
    if args.categorize and container.has(FieldCategorizer):
        categorizer = container.resolve(FieldCategorizer)

    # Create use case
    use_case = ExtractFieldsUseCase(pdf_processor=pdf_processor, categorizer=categorizer)

    # Execute extraction
    pdf_form = use_case.execute(args.pdf)

    # Display results
    print(f"Extracted {pdf_form.field_count} fields from {args.pdf}")

    if args.categorize:
        print("\nFields by category:")
        categories: dict[str, list[str]] = {}
        for field in pdf_form.fields:
            cat = field.category.value if field.category else "uncategorized"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(field.name)

        for category, fields in sorted(categories.items()):
            print(f"  {category}: {len(fields)} fields")
            for field_name in fields[:3]:  # Show first 3 as examples
                print(f"    - {field_name}")
            if len(fields) > 3:
                print(f"    ... and {len(fields) - 3} more")

    # Save outputs if requested
    if args.json:
        if container.has("json_repository"):
            repo = container.resolve("json_repository")
            stub_data = pdf_form.to_stub_dict()
            repo.save(stub_data, args.json)
            print(f"\nSaved JSON stub to {args.json}")

    if args.yaml:
        if container.has("yaml_repository"):
            repo = container.resolve("yaml_repository")
            stub_data = pdf_form.to_stub_dict()
            repo.save(stub_data, args.yaml)
            print(f"Saved YAML stub to {args.yaml}")
