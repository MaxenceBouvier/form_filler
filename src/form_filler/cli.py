"""Command-line interface for Form Filler utilities."""

import sys


def extract_required_info() -> None:
    """Extract required field information from a PDF form.

    Usage:
        extract-required-info form.pdf
    """
    print("extract-required-info: Not yet implemented")
    print("This command will analyze a PDF form and extract metadata about required fields.")
    sys.exit(1)


def update_user_info() -> None:
    """Update user information database.

    Usage:
        update-user-info --only-new    # default: adds only fields not in user info file
        update-user-info --review      # interactive mode to review/update existing values
    """
    print("update-user-info: Not yet implemented")
    print("This command will manage a persistent user information store (JSON/YAML file).")
    sys.exit(1)


def fill_in_pdf() -> None:
    """Fill a PDF form with user data.

    Usage:
        fill-in-pdf --input form.pdf --user my_info.json
    """
    print("fill-in-pdf: Not yet implemented")
    print("This command will populate PDF form fields with user data.")
    print("Output will be named as {original_pdf_name}_autofilled.pdf")
    sys.exit(1)
