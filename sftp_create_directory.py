#!/usr/bin/env python3
import argparse
import paramiko
import sys
import uuid
import time

def create_test_directory(host, port, username, password):
    """Создание тестовой директории на SFTP сервере"""
    try:
        print("Создание тестовой директории...")
        
        # Генерируем уникальное имя директории
        test_dir_name = f"jenkins_test_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        
        transport = paramiko.Transport((host, int(port)))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Создаем директорию
        sftp.mkdir(test_dir_name)
        print(f"✓ Директория '{test_dir_name}' успешно создана")
        
        # Сохраняем имя созданной директории для последующего удаления
        with open('test_directory.txt', 'w') as f:
            f.write(test_dir_name)
        
        sftp.close()
        transport.close()
        
        return test_dir_name
        
    except Exception as e:
        print(f"✗ Ошибка при создании директории: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Создание тестовой директории на SFTP')
    parser.add_argument('--host', required=True, help='SFTP хост')
    parser.add_argument('--port', default=22, help='SFTP порт')
    parser.add_argument('--username', required=True, help='Имя пользователя SFTP')
    parser.add_argument('--password', required=True, help='Пароль SFTP')
    
    args = parser.parse_args()
    
    create_test_directory(args.host, args.port, args.username, args.password)

if __name__ == "__main__":
    main()
