pipeline {
    agent any
    
    parameters {
        string(name: 'SFTP_HOST', defaultValue: '', description: 'SFTP сервер хост')
        string(name: 'SFTP_USERNAME', defaultValue: '', description: 'Логин SFTP')
        password(name: 'SFTP_PASSWORD', defaultValue: '', description: 'Пароль SFTP')
        string(name: 'SFTP_PORT', defaultValue: '22', description: 'Порт SFTP')
    }
    
    environment {
        PP_NAME = 'my-app'
        // Опционально: можно использовать credentials из Jenkins
        // SFTP_CREDENTIALS = credentials('sftp-credentials')
    }
    
    stages {

        stage('Подготовка окружения') {
            steps {
                script {
                    // Создаем файл requirements.txt
                    sh '''
                    cat > requirements.txt << 'EOF'
                    paramiko>=2.7.0
                    EOF
                    '''
                    
                    // Устанавливаем зависимости
                    sh 'pip install -r requirements.txt'
                    
                    // Альтернативно, для виртуального окружения:
                    // sh '''
                    // python3 -m venv venv
                    // source venv/bin/activate
                    // pip install -r requirements.txt
                    // '''
                }
            }
        }

        stage('Проверка параметров') {
            steps {
                script {
                    if (!params.SFTP_HOST?.trim() || !params.SFTP_USERNAME?.trim() || !params.SFTP_PASSWORD?.trim()) {
                        error("Все параметры (хост, логин, пароль) должны быть заполнены")
                    }
                }
            }
        }
        
        stage('Проверка подключения SFTP') {
            steps {
                script {
                    def pythonScript = 'sftp_connection_test.py'
                    
                    // Выполняем Python скрипт для проверки подключения
                    sh """
                    python3 ${pythonScript} \
                        --host "${params.SFTP_HOST}" \
                        --port "${params.SFTP_PORT}" \
                        --username "${params.SFTP_USERNAME}" \
                        --password "${params.SFTP_PASSWORD}"
                    """
                }
            }
        }
        
        stage('Проверка создания директории') {
            steps {
                script {
                    def pythonScript = 'sftp_create_directory.py'
                    
                    sh """
                    python3 ${pythonScript} \
                        --host "${params.SFTP_HOST}" \
                        --port "${params.SFTP_PORT}" \
                        --username "${params.SFTP_USERNAME}" \
                        --password "${params.SFTP_PASSWORD}"
                    """
                }
            }
        }
        
        stage('Проверка удаления директории') {
            steps {
                script {
                    def pythonScript = 'sftp_delete_directory.py'
                    
                    sh """
                    python3 ${pythonScript} \
                        --host "${params.SFTP_HOST}" \
                        --port "${params.SFTP_PORT}" \
                        --username "${params.SFTP_USERNAME}" \
                        --password "${params.SFTP_PASSWORD}"
                    """
                }
            }
        }
        
        stage('Выполнение API метода') {
            steps {
                script {
                    // Пример выполнения API GET запроса
                    sh """
                    curl -X GET "https://api.example.com/kek" \
                         -H "Content-Type: application/json"
                    """
                    
                    // Или с использованием инструментов Jenkins
                    // httpRequest url: 'https://api.example.com/kek', httpMode: 'GET'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Все проверки SFTP выполнены успешно и API метод вызван'
        }
        failure {
            echo 'Произошла ошибка в процессе выполнения'
        }
        cleanup {
            echo 'Очистка завершена'
        }
    }
}
