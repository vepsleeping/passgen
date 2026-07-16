import unittest
from generator import PasswordGenerator
from validator import PasswordValidator


class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PasswordGenerator(use_secrets=False)
    
    def test_generate_password_valid(self):
        password, error = self.generator.generate_password(
            total_length=10,
            lowercase_count=3,
            uppercase_count=2,
            digits_count=2,
            special_count=1
        )
        
        self.assertIsNotNone(password)
        self.assertEqual(error, "")
        self.assertEqual(len(password), 10)
        
        # Проверка через валидатор
        is_valid, report = PasswordValidator.check_compliance(
            password, 3, 2, 2, 1
        )
        self.assertTrue(is_valid, f"Пароль не прошёл проверку: {report}")
    
    def test_generate_password_minimal(self):
        password, error = self.generator.generate_password(
            total_length=1,
            lowercase_count=1
        )
        
        self.assertIsNotNone(password)
        self.assertEqual(error, "")
        self.assertEqual(len(password), 1)
        self.assertTrue(password.islower())
    
    def test_validate_params_negative_length(self):
        is_valid, error = self.generator.validate_params(
            total_length=-1,
            lowercase_count=0,
            uppercase_count=0,
            digits_count=0,
            special_count=0
        )
        self.assertFalse(is_valid)
        self.assertIn("отрицательной", error)
    
    def test_validate_params_sum_exceeds_total(self):
        is_valid, error = self.generator.validate_params(
            total_length=5,
            lowercase_count=3,
            uppercase_count=3,
            digits_count=0,
            special_count=0
        )
        self.assertFalse(is_valid)
        self.assertIn("превышает", error)
    
    def test_validate_params_empty_password(self):
        is_valid, error = self.generator.validate_params(
            total_length=0,
            lowercase_count=0,
            uppercase_count=0,
            digits_count=0,
            special_count=0
        )
        self.assertFalse(is_valid)
        self.assertIn("хотя бы один символ", error)
    
    def test_generate_with_remaining_chars(self):
        password, error = self.generator.generate_password(
            total_length=15,
            lowercase_count=3,
            uppercase_count=2,
            digits_count=2,
            special_count=1
        )
        
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 15)
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in PasswordValidator.CHAR_SETS['special'] for c in password)
        
        self.assertTrue(has_lowercase)
        self.assertTrue(has_uppercase)
        self.assertTrue(has_digit)
        self.assertTrue(has_special)
    
    def test_generator_with_secrets(self):
        secure_gen = PasswordGenerator(use_secrets=True)
        password, error = secure_gen.generate_password(
            total_length=20,
            lowercase_count=5,
            uppercase_count=5,
            digits_count=5,
            special_count=5
        )
        
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 20)
        
        is_valid, report = PasswordValidator.check_compliance(
            password, 5, 5, 5, 5
        )
        self.assertTrue(is_valid, f"Пароль не прошёл проверку: {report}")

    def test_generate_multiple_passwords(self):
        passwords, errors = self.generator.generate_multiple_passwords(
            count=3,
            total_length=10,
            lowercase_count=2,
            uppercase_count=2,
            digits_count=2,
            special_count=1
        )
        
        self.assertEqual(len(passwords), 3)
        self.assertEqual(errors, [])
        
        for pwd in passwords:
            self.assertEqual(len(pwd), 10)
            is_valid, report = PasswordValidator.check_compliance(
                pwd, 2, 2, 2, 1
            )
            self.assertTrue(is_valid, f"Пароль {pwd} не прошёл проверку")


class TestPasswordValidator(unittest.TestCase):
    def test_check_compliance_valid(self):
        is_valid, report = PasswordValidator.check_compliance(
            "Abcd123!@", 3, 1, 3, 2
        )
        self.assertTrue(is_valid)
        self.assertEqual(report['errors'], [])
    
    def test_check_compliance_missing_lowercase(self):
        is_valid, report = PasswordValidator.check_compliance(
            "ABC123!@#", 3, 3, 3, 3
        )
        self.assertFalse(is_valid)
        self.assertIn("строчных", str(report['errors']))
    
    def test_check_compliance_empty_password(self):
        is_valid, report = PasswordValidator.check_compliance("", 0, 0, 0, 0)
        self.assertFalse(is_valid)
        self.assertEqual(report, "Пароль пуст")  # Исправлено: ожидаем строку
    
    def test_check_compliance_invalid_chars(self):
        is_valid, report = PasswordValidator.check_compliance(
            "Hello World", 0, 0, 0, 0
        )
        self.assertFalse(is_valid)
        self.assertIn("недопустимые символы", str(report['errors']))


if __name__ == "__main__":
    unittest.main()