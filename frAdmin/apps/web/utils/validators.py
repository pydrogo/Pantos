from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

route_validator = RegexValidator(r'^/.*', 'Value must start with /')
# icon_jpg_validate = FileExtensionValidator(['jpg'],message='File must be jpg')
# def validate_image(file):
#     file_size = file.size
#     limit_kb = 150
#     if file_size > limit_kb * 1024:
#         raise ValidationError("Max size of file is %s KB" % limit_kb)