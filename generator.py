"""
Модуль генератора паролей
Содержит класс PasswordGenerator для создания случайных паролей
"""

import random
import secrets
import string


class PasswordGenerator:
    CHAR_SETS = {
        'lowercase': string.ascii_lowercase,          # abcdefghijklmnopqrstuvwxyz
        'uppercase': string.ascii_uppercase,          # ABCDEFGHIJKLMNOPQRSTUVWXYZ
        'digits': string.digits,                      # 0123456789
        'special': "!@#$%^&*()_-+=<>?/.,;:[]{}|"     # Специальные символы
    }
    
    def __init__(self, use_secrets=False):
        self.use_secrets = use_secrets
        self._random_choice = secrets.choice if use_secrets else random.choice
    
    def validate_params(self, total_length, lowercase_count, uppercase_count, 
                        digits_count, special_count):
        if total_length < 0:
            return False, "Общая длина пароля не может быть отрицательной"
        if lowercase_count < 0:
            return False, "Количество строчных букв не может быть отрицательным"
        if uppercase_count < 0:
            return False, "Количество заглавных букв не может быть отрицательным"
        if digits_count < 0:
            return False, "Количество цифр не может быть отрицательным"
        if special_count < 0:
            return False, "Количество специальных символов не может быть отрицательным"
        
        total_needed = lowercase_count + uppercase_count + digits_count + special_count
        if total_needed == 0:
            return False, "Пароль должен содержать хотя бы один символ"
        if total_needed > total_length:
            return False, f"Сумма критериев ({total_needed}) превышает общую длину пароля ({total_length})"
        
        return True, ""
    
    def _generate_char_sequence(self, count, char_set):
        if count <= 0 or not char_set:
            return ""
        return ''.join(self._random_choice(char_set) for _ in range(count))
    
    def generate_password(self, total_length, lowercase_count=0, uppercase_count=0, 
                          digits_count=0, special_count=0):
        is_valid, error = self.validate_params(
            total_length, lowercase_count, uppercase_count, digits_count, special_count
        )
        if not is_valid:
            return None, error
        
        password_chars = []
        
        password_chars.extend(self._generate_char_sequence(
            lowercase_count, self.CHAR_SETS['lowercase']
        ))
        
        password_chars.extend(self._generate_char_sequence(
            uppercase_count, self.CHAR_SETS['uppercase']
        ))
        
        password_chars.extend(self._generate_char_sequence(
            digits_count, self.CHAR_SETS['digits']
        ))
        
        password_chars.extend(self._generate_char_sequence(
            special_count, self.CHAR_SETS['special']
        ))
        
        remaining = total_length - (lowercase_count + uppercase_count + digits_count + special_count)
        if remaining > 0:
            all_chars = ''.join(self.CHAR_SETS.values())
            password_chars.extend(self._generate_char_sequence(remaining, all_chars))
        
        random.shuffle(password_chars)
        
        password = ''.join(password_chars)
        
        return password, ""
    
    def generate_multiple_passwords(self, count, total_length, lowercase_count=0, 
                                uppercase_count=0, digits_count=0, special_count=0):
        passwords = []
        errors = []
        for i in range(count):
            password, error = self.generate_password(total_length, lowercase_count, uppercase_count, digits_count, special_count)
            if password is not None:
                passwords.append(password)
            else:
                errors.append(f"Пароль #{i+1}: {error}")
        return passwords, errors