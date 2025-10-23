pipeline {
  agent any

  environment {
    DOCKER_USER = 'loksjain25'
    REPO_NAME   = 'flask-cicd'
    IMAGE       = "${DOCKER_USER}/${REPO_NAME}"
    TAG         = "${env.BUILD_NUMBER}"
    DOCKERHUB_CRED  = 'dockerhub-creds'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Test') {
      steps {
        sh '''
          cd app
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -c "import flask; print('Flask OK')"
        '''
      }
    }

    stage('Docker Build') {
      steps {
        sh '''
          docker build -t ${IMAGE}:${TAG} -t ${IMAGE}:latest app
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh '''
            echo "$PASS" | docker login -u "$USER" --password-stdin
            docker push ${IMAGE}:${TAG}
            docker push ${IMAGE}:latest
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl apply -f k8s/namespace.yaml
          kubectl apply -f k8s/rbac-jenkins.yaml
          sed "s|DOCKER_USER/flask-cicd:latest|${IMAGE}:${TAG}|g" k8s/deployment.yaml | kubectl apply -f -
          kubectl apply -f k8s/service.yaml
          kubectl -n demo annotate deploy flask-app app/version="${BUILD_NUMBER}" --overwrite
          kubectl -n demo rollout status deploy/flask-app
        '''
      }
    }
  }

  post {
    always { echo "Build #${env.BUILD_NUMBER} finished with status: ${currentBuild.currentResult}" }
  }
}
