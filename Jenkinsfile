pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = "loksjain25/flask-cicd"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Loksjain/python_cicd.git'
            }
        }

        stage('Build Docker Image') {
    steps {
        script {
            sh 'docker build -t loksjain25/flask-cicd:5 -f app/Dockerfile .'
        }
    }
}

        stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                          usernameVariable: 'DOCKERHUB_USER',
                                          passwordVariable: 'DOCKERHUB_PASS')]) {
            sh '''
            echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin
            docker push loksjain25/flask-cicd:5
            '''
        }
    }
}


        stage('Deploy to Kubernetes') {
    steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
            sh '''
                kubectl config use-context docker-desktop
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
            '''
        }
    }
}
    }
}
