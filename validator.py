"""
Модуль валидатора паролей
Содержит класс PasswordValidator для проверки паролей
"""

import string


class PasswordValidator:
    CHAR_SETS = {
        'lowercase': set(string.ascii_lowercase),
        'uppercase': set(string.ascii_uppercase),
        'digits': set(string.digits),
        'special': set("!@#$%^&*()_-+=<>?/.,;:[]{}|")
    }
    
    @classmethod
    def check_compliance(cls, password, required_lowercase=0, required_uppercase=0,
                         required_digits=0, required_special=0):
        if not password:
            return False, "Пароль пуст"
        
        counts = {
            'lowercase': 0,
            'uppercase': 0,
            'digits': 0,
            'special': 0,
            'other': 0
        }
        
        for char in password:
            if char in cls.CHAR_SETS['lowercase']:
                counts['lowercase'] += 1
            elif char in cls.CHAR_SETS['uppercase']:
                counts['uppercase'] += 1
            elif char in cls.CHAR_SETS['digits']:
                counts['digits'] += 1
            elif char in cls.CHAR_SETS['special']:
                counts['special'] += 1
            else:
                counts['other'] += 1
        
        errors = []
        if counts['lowercase'] < required_lowercase:
            errors.append(f"строчных букв: {counts['lowercase']} < {required_lowercase}")
        if counts['uppercase'] < required_uppercase:
            errors.append(f"заглавных букв: {counts['uppercase']} < {required_uppercase}")
        if counts['digits'] < required_digits:
            errors.append(f"цифр: {counts['digits']} < {required_digits}")
        if counts['special'] < required_special:
            errors.append(f"специальных символов: {counts['special']} < {required_special}")
        
        if counts['other'] > 0:
            errors.append(f"найдены недопустимые символы: {counts['other']} шт.")
        
        report = {
            'length': len(password),
            'counts': counts,
            'errors': errors
        }
        
        return len(errors) == 0, report