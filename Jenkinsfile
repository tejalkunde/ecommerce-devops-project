pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tejalkunde/ecommerce-devops-project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ecommerce-flask .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                docker stop ecommerce-container || true
                docker rm ecommerce-container || true
                docker run -d --name ecommerce-container -p 5000:5000 ecommerce-flask
                '''
            }
        }
    }
}
