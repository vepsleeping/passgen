"""
Модуль консольного интерфейса
Содержит класс ConsoleApp для взаимодействия с пользователем
"""

import sys
from generator import PasswordGenerator
from validator import PasswordValidator


class ConsoleApp:
    def __init__(self, input_stream=None, output_stream=None):
        self.input = input_stream if input_stream else sys.stdin
        self.output = output_stream if output_stream else sys.stdout
        self.generator = PasswordGenerator(use_secrets=False)
    
    def _read_line(self, prompt):
        print(prompt, end=' ', file=self.output, flush=True)
        return self.input.readline().strip()
    
    def _read_int(self, prompt, default=0):
        while True:
            value = self._read_line(prompt)
            if value == '':
                return default
            try:
                return int(value)
            except ValueError:
                print("Ошибка: введите целое число", file=self.output)
    
    def _display_menu(self):
        print("\n" + "="*50, file=self.output)
        print("  PassGen - Генератор случайных паролей", file=self.output)
        print("="*50, file=self.output)
        print("Введите параметры пароля:", file=self.output)
        print("  (нажмите Enter, чтобы пропустить параметр)", file=self.output)
        print("-"*50, file=self.output)
    
    def _display_result(self, password):
        print("\n" + "="*50, file=self.output)
        print("  Сгенерированный пароль:", file=self.output)
        print("-"*50, file=self.output)
        print(f"  {password}", file=self.output)
        print("="*50, file=self.output)
        print(f"  Длина пароля: {len(password)} символов", file=self.output)
        print("="*50, file=self.output)
    
    def _display_error(self, message):
        print(f"\n❌ Ошибка: {message}", file=self.output)
    
    def _display_info(self, message):
        print(f"\nℹ️  {message}", file=self.output)
    
    def run(self):
        while True:
            self._display_menu()
            
            print("\nОбщая длина пароля:", file=self.output)
            total_length = self._read_int("(по умолчанию: 12):", 12)
            
            lowercase = self._read_int("Количество строчных букв (по умолчанию: 0):", 0)
            uppercase = self._read_int("Количество заглавных букв (по умолчанию: 0):", 0)
            digits = self._read_int("Количество цифр (по умолчанию: 0):", 0)
            special = self._read_int("Количество специальных символов (по умолчанию: 0):", 0)
            
            password, error = self.generator.generate_password(
                total_length, lowercase, uppercase, digits, special
            )
            
            if password is None:
                self._display_error(error)
                continue
            
            is_valid, report = PasswordValidator.check_compliance(
                password, lowercase, uppercase, digits, special
            )
            
            self._display_result(password)
            
            if not is_valid:
                self._display_error("Сгенерированный пароль не прошёл проверку!")
                print(f"  Отчёт: {report['errors']}", file=self.output)
                continue
            
            self._display_info("Пароль успешно сгенерирован!")
            
            choice = self._read_line("\nСгенерировать ещё один пароль? (y/N):")
            if choice.lower() != 'y':
                print("\nДо свидания!", file=self.output)
                break