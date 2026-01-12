pipeline {

    agent any

    parameters {
        string(name: 'SFTP_HOST', defaultValue: '', description: 'SFTP сервер хост')
        string(name: 'SFTP_USERNAME', defaultValue: '', description: 'Логин SFTP')
        password(name: 'SFTP_PASSWORD', defaultValue: '', description: 'Пароль SFTP')
        string(name: 'SFTP_PORT', defaultValue: '22', description: 'Порт SFTP')
        string(name: 'SFTP_DIR', defaultValue: '/', description: 'Директория SFTP')
    }
    
    environment {
        API_HOST = ''
        // Опционально: можно использовать credentials из Jenkins
        // SFTP_CREDENTIALS = credentials('sftp-credentials')
    }
    
    stages {

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Проверка подключения SFTP') {
            steps {
                script {
                    def pythonScript = 'sftp_connection_test.py'
                    
                    // Выполняем Python скрипт для проверки подключения
                    sh """
                    venv/bin/python ${pythonScript} \
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
                    venv/bin/python ${pythonScript} \
                        --host "${params.SFTP_HOST}" \
                        --port "${params.SFTP_PORT}" \
                        --username "${params.SFTP_USERNAME}" \
                        --password "${params.SFTP_PASSWORD}" \
                        --dir "${params.SFTP_DIR}"
                    """
                }
            }
        }
        
        stage('Проверка удаления директории') {
            steps {
                script {
                    def pythonScript = 'sftp_delete_directory.py'
                    
                    sh """
                    venv/bin/python ${pythonScript} \
                        --host "${params.SFTP_HOST}" \
                        --port "${params.SFTP_PORT}" \
                        --username "${params.SFTP_USERNAME}" \
                        --password "${params.SFTP_PASSWORD}" \
                        --dir "${params.SFTP_DIR}"
                    """
                }
            }
        }

        stage('Запрос дополнительных параметров') {
            when {
                expression { return currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    // Используем input для запроса дополнительных параметров
                    def additionalParams = input(
                        message: 'Введите параметры для API вызова',
                        parameters: [
                            string(name: 'API_HOST', description: 'API хост')
                        ]
                    )
                    
                    // Сохраняем параметры в переменные для использования в следующем этапе
                    env.API_HOST = additionalParams.API_HOST
                }
            }
        }

        stage('Выполнение API метода') {
            when {
                expression { return currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    // Выполняем API метод с полученными параметрами
                    echo "Выполнение API метода на хосте: ${env.API_HOST}"
                                        
                    // Или можно использовать Python скрипт для API вызова
                    sh """
                        venv/bin/python api_set_sftp.py \
                            --host "${env.API_HOST}"
                    """
                }
            }
        }
        
    }
    
    post {
        success {
            echo 'Все проверки SFTP выполнены успешно'
        }
        failure {
            echo 'Произошла ошибка в процессе выполнения'
        }
        cleanup {
            echo 'Очистка завершена'
        }
    }
}