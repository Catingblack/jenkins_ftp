pipeline {

    agent any

    parameters {
        string(name: 'SFTP_HOST', defaultValue: '', description: 'SFTP сервер хост')
        string(name: 'SFTP_USERNAME', defaultValue: '', description: 'Логин SFTP')
        password(name: 'SFTP_PASSWORD', defaultValue: '', description: 'Пароль SFTP')
        string(name: 'SFTP_PORT', defaultValue: '22', description: 'Порт SFTP')
        string(name: 'SFTP_DIR', defaultValue: '/', description: 'Директория SFTP')
        choice(name: 'COLOR', choices: ['black', 'red', 'blue', 'green', 'pink', 'gold'], description: 'Выберите цвет инстанса')
        choice(name: 'PROTOCOL', choices: ['SFTP', 'FTPS'], description: 'Выберите протокол')
        string(name: 'TENANT_ID', defaultValue: '', description: 'tenant_id')
        string(name: 'CLIENT_ID', defaultValue: '', description: 'client_id')
        string(name: 'START_UPLOADING_DATE', defaultValue: '2026-01-12T00:00:00Z', description: 'Дата, с которой будет выгрузка. В формате yyyy-mm-ddTHH:MM:SSZ')
        booleanParam(name: 'EXEC_PBSZ_ENABLED', defaultValue: true, description: 'EXEC_PBSZ_ENABLED')
        booleanParam(name: 'LOCAL_PASSIVE_MODE_ENABLED', defaultValue: true, description: 'LOCAL_PASSIVE_MODE_ENABLED')
        booleanParam(name: 'FORCE_UTF8_CONTROL_ENCODING_ENABLED', defaultValue: true, description: 'FORCE_UTF8_CONTROL_ENCODING_ENABLED')
        booleanParam(name: 'SEND_OPTION_UTF8_ENABLED', defaultValue: true, description: 'SEND_OPTION_UTF8_ENABLED')
    }
    
    environment {
        API_HOST = 'kek'
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

        stage('Вызов api метода для настройки') {
            steps {
                script {
                    sh """
                        export COLOR="${params.COLOR}"
                        export CLIENT_ID="${params.CLIENT_ID}"
                        export API_TOKEN="${params.API_TOKEN}"
                        export TENANT_ID="${params.TENANT_ID}"
                        export PROTOCOL="${params.PROTOCOL}"
                        export SFTP_DIR="${params.SFTP_DIR}"
                        export SFTP_USERNAME="${params.SFTP_USERNAME}"
                        export SFTP_PASSWORD="${params.SFTP_PASSWORD}"
                        export SFTP_HOST="${params.SFTP_HOST}"
                        export SFTP_PORT="${params.SFTP_PORT}"
                        export START_UPLOADING_DATE="${params.START_UPLOADING_DATE}"
                        export EXEC_PBSZ_ENABLED="${params.EXEC_PBSZ_ENABLED}"
                        export LOCAL_PASSIVE_ENABLED="${params.LOCAL_PASSIVE_ENABLED}"
                        export FORCE_UTF8_ENABLED="${params.FORCE_UTF8_ENABLED}"
                        export SEND_UTF8_ENABLED="${params.SEND_UTF8_ENABLED}"
                    
                        ./api_set_sftp.sh
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