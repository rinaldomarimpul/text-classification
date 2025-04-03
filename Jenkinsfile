pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout kode dari repositori
                checkout scm
                
                // Cek ketersediaan tools
                sh '''
                echo "Memeriksa tool yang tersedia:"
                echo "Git: $(which git || echo 'Tidak tersedia')"
                echo "Docker: $(which docker || echo 'Tidak tersedia')"
                echo "Python: $(which python || echo 'Tidak tersedia')"
                echo "Python3: $(which python3 || echo 'Tidak tersedia')"
                echo "Kubectl: $(which kubectl || echo 'Tidak tersedia')"
                '''
            }
        }
        
        stage('Verify Project Files') {
            steps {
                sh '''
                echo "Daftar file dalam project:"
                ls -la
                
                echo "Memeriksa file konfigurasi:"
                if [ -f "requirements.txt" ]; then
                    echo "requirements.txt ditemukan"
                    cat requirements.txt
                else
                    echo "requirements.txt tidak ditemukan"
                fi
                
                if [ -f "Dockerfile" ]; then
                    echo "Dockerfile ditemukan"
                    cat Dockerfile
                else
                    echo "Dockerfile tidak ditemukan"
                fi
                '''
            }
        }
        
        stage('Check Container Environment') {
            steps {
                sh '''
                echo "Informasi sistem:"
                uname -a
                cat /etc/os-release || echo "Tidak dapat menentukan OS"
                
                echo "Direktori dan akses:"
                df -h
                mount
                '''
            }
        }
    }
    
    post {
        always {
            node(null) {
                // Bersihkan workspace
                cleanWs()
            }
        }
        success {
            node(null) {
                echo 'Pipeline berhasil! Namun perhatikan bahwa ini adalah pipeline minimal untuk diagnostik.'
            }
        }
        failure {
            node(null) {
                echo 'Pipeline gagal. Periksa log untuk detail diagnostic.'
            }
        }
    }
}
