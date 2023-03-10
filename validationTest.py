import unittest
from django.core.exceptions import ValidationError
import validations as v

class MyTestCase(unittest.TestCase):

    # validate_weight test
    def test_validate_weight(self):
        valid = [1, 100]
        error = [0, -120]

        for i in valid:
            v.validate_weight(i)

        for j in error:
            with self.assertRaises(ValidationError, msg='Weight cannot be zero or a negative value.'):
                v.validate_weight(j)

    # validate_height test
    def test_validate_height(self):
        valid = [1, 100]
        error = [0, -120]

        for i in valid:
            v.validate_height(i)

        for j in error:
            with self.assertRaises(ValidationError, msg='Height cannot be zero or a negative value.'):
                v.validate_height(j)

    # validate_cellphone_number() test
    def test_validate_cellphone_number(self):
        error = [997703286540, 639112323232223]

        v.validate_cellphone_number(639770328654)

        for i in error:
            with self.assertRaises(ValidationError, msg='Cellphone number should be exactly 12 digits and start with 639.'):
                v.validate_cellphone_number(i)

    # validate_telephone_number() test
    def test_validate_telephone_number(self):
        error = [63232123123, 282821232123]

        v.validate_telephone_number(63282821721)

        for i in error:
            with self.assertRaises(ValidationError, msg='Telephone number should be exactly 11 digits and start with 6328.'):
                v.validate_telephone_number(i)

    # validate_email() test
    def test_validate_email(self):
        valid = ["jifidelino@gmail.com", "ira@dlsu.com", "john@yahoo.com"]
        error = ["johnyahoo.com", "john@yahoo."]

        for i in valid:
            v.validate_email(i)

        for j in error:
            with self.assertRaises(ValidationError, msg='Invalid email format.'):
                v.validate_email(j)

    # validate_username() test
    def test_validate_username(self):
        valid = ["RaFidelino", "IraFidelino12", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
        error = ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Ira Fidelino12", "@IraFidelino12"]

        for i in valid:
            v.validate_username(i)

        for j in error:
            with self.assertRaises(ValidationError, msg='Username should only contain letters and numbers and be at least 10 characters.'):
                v.validate_username(j)

    # validate_password() test
    def test_validate_password(self):
        valid = ["Ira_Fidelino1", "@ira2Fidelino"]
        error = ["JohnIr@", "IIRAFIDELINO", "irafidelino", "irafidelino", "ira fidelino", "iraFidelino2", "irafidelino@"]

        for i in valid:
            v.validate_password(i)

        for j in error:
            with self.assertRaises(ValidationError, msg='Password should contain letters, numbers, and special characters and be at least 10 characters.'):
                v.validate_password(j)

    # validate_license() test
    def test_license(self):
        v.validate_license("1234567")

        with self.assertRaises(ValidationError, msg='It looks like you entered the wrong info. Please be sure to enter a registered license number.'):
            v.validate_license("12345678")

if __name__ == '__main__':
    unittest.main()
