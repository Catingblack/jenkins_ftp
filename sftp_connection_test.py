#!/usr/bin/env python3
import argparse
import paramiko
import sys
import os

def test_sftp_connection(host, port, username, password):
    """Тестирование подключения к SFTP серверу"""
    try:
        print(f"Попытка подключения к {host}:{port} с пользователем {username}")
        
        # Создаем транспорт SSH
        transport = paramiko.Transport((host, int(port)))
        transport.connect(username=username, password=password)
        
        # Создаем SFTP клиент
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Проверяем подключение, получая текущую директорию
        current_dir = sftp.getcwd()
        print(f"Успешное подключение. Текущая директория: {current_dir}")
        
        # Закрываем соединение
        sftp.close()
        transport.close()
        
        print("✓ Подключение к SFTP успешно проверено")
        return True
        
    except paramiko.AuthenticationException:
        print("✗ Ошибка аутентификации. Проверьте логин и пароль.")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"✗ Ошибка SSH: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Ошибка подключения: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Проверка подключения к SFTP серверу')
    parser.add_argument('--host', required=True, help='SFTP хост')
    parser.add_argument('--port', default=22, help='SFTP порт')
    parser.add_argument('--username', required=True, help='Имя пользователя SFTP')
    parser.add_argument('--password', required=True, help='Пароль SFTP')
    
    args = parser.parse_args()
    
    test_sftp_connection(args.host, args.port, args.username, args.password)

if __name__ == "__main__":
    main()
