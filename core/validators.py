import imghdr
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
MAX_FILE_SIZE_MB = 5

def validate_file_extension(file):
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")

def validate_file_size(file):
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {MAX_FILE_SIZE_MB} MB.")

def validate_real_image(file):
    # Temporary read
    file_type = imghdr.what(file)
    if file_type not in ALLOWED_EXTENSIONS:
        raise ValidationError("Invalid image file.")
