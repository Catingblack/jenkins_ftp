#!/usr/bin/env python3
import argparse
import paramiko
import sys
import os

def delete_test_directory(host, port, username, password, dir):
    """Удаление тестовой директории на SFTP сервере"""
    try:
        print("Удаление тестовой директории...")

        # Переходим в корневую директорию
        sftp.chdir(dir)
        
        # Читаем имя созданной ранее директории
        if not os.path.exists('test_directory.txt'):
            print("✗ Файл с именем тестовой директории не найден")
            sys.exit(1)
        
        with open('test_directory.txt', 'r') as f:
            test_dir_name = f.read().strip()
        
        transport = paramiko.Transport((host, int(port)))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        
        # Получаем список всех элементов в текущей директории
        items = sftp.listdir('.')

        for item in items:
            # Проверяем, содержит ли имя 'sftp_test'
            if 'sftp_test' in item.lower():
                print(f"Удаляем директорию: {item}")
                sftp.rmdir(item)
                print(f"✓ Директория '{item}' удалена")     
        sftp.close()
        transport.close()
        
    except Exception as e:
        print(f"✗ Ошибка при удалении директории: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Удаление тестовой директории на SFTP')
    parser.add_argument('--host', required=True, help='SFTP хост')
    parser.add_argument('--port', default=22, help='SFTP порт')
    parser.add_argument('--username', required=True, help='Имя пользователя SFTP')
    parser.add_argument('--password', required=True, help='Пароль SFTP')
    parser.add_argument('--dir', required=True, help='Директория SFTP')
    
    args = parser.parse_args()
    
    delete_test_directory(args.host, args.port, args.username, args.password, args.dir)

if __name__ == "__main__":
    main()
