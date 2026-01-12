#!/usr/bin/env python3

import requests
import argparse
import sys

def call_api(host, path):
    """
    Выполнить простой GET запрос к API
    
    Args:
        host (str): Хост API (например, https://api.example.com)
        path (str): Путь API (например, /test)
    """
    # Формируем URL
    url = f"{host.rstrip('/')}/{path.lstrip('/')}"
    
    print(f"Выполняю запрос к: {url}")
    
    try:
        # Выполняем GET запрос
        response = requests.get(url, timeout=30)
        
        # Выводим результат
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Запрос успешен")
            
            # Пытаемся показать JSON или текст
            try:
                data = response.json()
                print("Ответ (JSON):")
                print(data)
            except:
                print("Ответ (текст):")
                print(response.text[:500])  # Ограничиваем вывод
        else:
            print("✗ Ошибка запроса")
            print(f"Текст ошибки: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Ошибка подключения: {e}")
        sys.exit(1)

def main():
    # Парсим аргументы
    parser = argparse.ArgumentParser(description='Выполнить API запрос')
    parser.add_argument('--host', required=True, help='Хост API')
    parser.add_argument('--path', required=True, help='Путь API')
    
    args = parser.parse_args()
    
    # Выполняем запрос
    call_api(args.host, args.path)

if __name__ == '__main__':
    main()