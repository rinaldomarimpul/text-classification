pipeline {
    agent any
    
    // environment {
    //     // Definisikan variabel lingkungan
    //     APP_NAME = 'text-classification'
    //     DOCKER_HUB_USERNAME = credentials('docker-hub-username')
    //     DOCKER_IMAGE_NAME = "${DOCKER_HUB_USERNAME}/${APP_NAME}"
    //     DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
    // }

    environment {
        // Definisikan variabel lingkungan
        APP_NAME = 'text-classification'
        DOCKER_HUB_USERNAME = credentials('dockerhub-credentials').username
        DOCKER_HUB_PASSWORD = credentials('dockerhub-credentials').password
    }
 
    stages {
        stage('Checkout') {
            steps {
                // Checkout kode dari repositori
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                // Setup environment Python
                sh '''
                python -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                // Jalankan unit test
                sh '''
                . venv/bin/activate
                pytest -xvs tests/test_app.py
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
                // Login ke Docker Hub dan push image (dalam produksi gunakan credentials)
                // Untuk local, komentar bagian ini jika tidak ingin push ke Docker Hub
                /* 
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_HUB_PASSWORD')]) {
                    sh "echo ${DOCKER_HUB_PASSWORD} | docker login -u ${DOCKER_HUB_USERNAME} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                }
                */
                echo "Skip pushing to Docker Hub for local development"
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
                kubectl apply -f kubernetes/namespace.yaml
                kubectl apply -f kubernetes/deployment.yaml
                kubectl apply -f kubernetes/service.yaml
                """
            }
        }
    }
    
    post {
        always {
            // Bersihkan workspace
            cleanWs()
        }
        success {
            echo 'Pipeline berhasil! API siap digunakan.'
        }
        failure {
            echo 'Pipeline gagal. Periksa log untuk detail.'
        }
    }
}
