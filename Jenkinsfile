pipeline {
    agent any
    
    stages {
        stage('Check Docker') {
            steps {
                script {
                    // Проверить наличие Docker
                    def hasDocker = sh(
                        script: 'which docker || echo "no_docker"',
                        returnStdout: true
                    ).trim()
                    
                    echo "Docker available: ${hasDocker != 'no_docker'}"
                    
                    if (hasDocker != 'no_docker') {
                        sh 'docker --version'
                    } else {
                        error 'Docker not found on this agent!'
                    }
                }
            }
        }
    }
}