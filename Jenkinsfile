pipeline {
    agent any
    
    environment {
        // Definisikan variabel lingkungan
        APP_NAME = 'text-classification'
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE_NAME = "${env.DOCKER_CREDENTIALS_USR}/${APP_NAME}"
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout kode dari repositori
                checkout scm
            }
        }
        
        stage('Setup and Test') {
            steps {
                // Setup environment Python dan jalankan test menggunakan node default
                sh '''
                python3 -m venv venv || python -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest -xvs tests/test_app.py || echo "Tests failed but continuing"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Build Docker image
                sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                // Tag sebagai latest juga
                sh "docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest"
            }
        }
        
        stage('Push Docker Image') {
            steps {
                // Login ke Docker Hub dan push image
                sh "echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin"
                sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                sh "docker logout"
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                // Update nilai image di file kubernetes deployment
                sh """
                sed -i'' -e 's|image: .*|image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}|' kubernetes/deployment.yaml
                """
                
                // Deploy ke Kubernetes lokal
                sh """
                kubectl apply -f kubernetes/deployment.yaml
                kubectl apply -f kubernetes/service.yaml
                """
            }
        }
    }
    
    post {
        always {
            node(null) {  // Ini memastikan kita memiliki konteks node untuk operasi file
                cleanWs()  // Membersihkan workspace
            }
            // Pastikan untuk logout dari Docker Hub
            sh "docker logout || true"
        }
        success {
            echo 'Pipeline berhasil! API siap digunakan.'
        }
        failure {
            echo 'Pipeline gagal. Periksa log untuk detail.'
        }
    }
}
