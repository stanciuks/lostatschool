"""Custom validators for uploaded image files."""

import imghdr

from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
MAX_FILE_SIZE_MB = 5


def validate_file_extension(file):
    """Validate that the file has an allowed image extension."""
    ext = file.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")


def validate_file_size(file):
    """Validate that the file size does not exceed the allowed maximum."""
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"File size cannot exceed {MAX_FILE_SIZE_MB} MB.",
        )


def validate_real_image(file):
    """Validate that the uploaded file is an actual image file."""
    file_type = imghdr.what(file)
    if file_type not in ALLOWED_EXTENSIONS:
        raise ValidationError("Uploaded file is not a valid image.")
