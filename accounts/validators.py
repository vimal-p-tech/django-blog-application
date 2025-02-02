from django.core.exceptions import ValidationError

def validate_username(value):
    if not value.isalnum():
        raise ValidationError(
            f'{value} is not a valid username. Usernames must be alphanumeric.'
        )
    
def validate_username_length(value):
    if len(value) < 5:
        raise ValidationError('Username must be at least 5 characters long.')

def validate_username_characters(value):
    if not value.isalnum():
        raise ValidationError('Username must contain only alphanumeric characters.')