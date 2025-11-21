#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для запуска тестов и проверки покрытия кода
"""
import subprocess
import sys
import os


def check_pytest_cov_available():
    """Проверяет, доступен ли pytest-cov"""
    try:
        import pytest_cov
        return True
    except ImportError:
        return False


def run_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("Запуск тестов...")
    print("=" * 60)
    
    # Базовые аргументы для pytest
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short'
    ]
    
    # Добавляем опции покрытия, если pytest-cov доступен
    has_coverage = check_pytest_cov_available()
    if has_coverage:
        cmd.extend([
            '--cov=app',
            '--cov=database',
            '--cov-report=term-missing',
            '--cov-report=html'
        ])
        print("Проверка покрытия кода включена (pytest-cov установлен)")
    else:
        print("Проверка покрытия кода отключена (pytest-cov не установлен)")
        print("Для включения покрытия установите: pip install pytest-cov")
    
    print("-" * 60)
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ Все тесты прошли успешно!")
        print("=" * 60)
        if has_coverage:
            print("\nОтчет о покрытии кода доступен в папке htmlcov/index.html")
    else:
        print("\n" + "=" * 60)
        print("✗ Некоторые тесты не прошли")
        print("=" * 60)
        sys.exit(1)


def run_specific_test(test_path):
    """Запуск конкретного теста"""
    cmd = [sys.executable, '-m', 'pytest', test_path, '-v']
    subprocess.run(cmd)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_specific_test(sys.argv[1])
    else:
        run_tests()

