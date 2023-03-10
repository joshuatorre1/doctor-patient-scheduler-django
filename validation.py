import re
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_birthday(value):
    if value > datetime.date.today():
        raise ValidationError(
            _('Invalid birthday. Please enter your real birthday.'),
            params={'value': value},
        )


def validate_weight(value):
    if value <= 0:
        raise ValidationError(
            _('Weight cannot be zero or a negative value.'),
            params={'value': value},
        )


def validate_height(value):
    if value <= 0:
        raise ValidationError(
            _('Height cannot be zero or a negative value.'),
            params={'value': value},
        )


def validate_cellphone_number(value):
    if len(str(value)) != 12 or str(value)[0:3] != "639":
        raise ValidationError(
            _('Cellphone number should be exactly 12 digits and start with 639.'),
            params={'value': value},
        )


def validate_telephone_number(value):
    if len(str(value)) != 11 or str(value)[0:4] != "6328":
        raise ValidationError(
            _('Telephone number should be exactly 11 digits and start with 6328.'),
            params={'value': value},
        )


def validate_email(value):
    emailPattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

    if not(emailPattern.match(value) or len(value) > 50):
        raise ValidationError(
            _('Invalid email format.'),
            params={'value': value},
        )


def validate_username(value):
    if not(value.isalnum()) or len(value) < 10 or len(value) > 50:
        raise ValidationError(
            _('Username should only contain letters and numbers and be at least 10 characters.'),
            params={'value': value},
        )


def validate_password(value):
    specialChar = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    if (any(char.isupper() for char in value) and any(char.islower() for char in value) and any(
            char.isdigit() for char in value) and specialChar.search(value) != None and len(value) > 9):
        pass
    else:
        raise ValidationError(
            _('Password should contain uppercase and lower case letters, numbers, and special characters and be at least 10 characters.'),
            params={'value': value},
        )


def validate_consultation_fee(value):
    if value < 0:
        raise ValidationError(
            _('Consultation fee cannot be a negative value.'),
            params={'value': value},
        )


def validate_license(value):
    if len(str(value)) != 7 or int(value) < 0:
        raise ValidationError(
            _('It looks like you entered the wrong info. Please be sure to enter a registered license number.'),
            params={'value': value},
        )


def validate_date(value):
    if value < datetime.date.today():
        raise ValidationError(
            _('Invalid date. Please enter a date in the future.'),
            params={'value': value},
        )


def validate_time(value):
    if value <= 0:
        raise ValidationError(
            _('Consultation time cannot be a negative value.'),
            params={'value': value},
        )

