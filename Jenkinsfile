pipeline {
agent any

```
stages {

    stage('Checkout') {
        steps {
            git branch: 'main',
                url: 'https://github.com/SahilChougala28/ai-defect-detection-system.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh 'docker build -t ai-defect-detection .'
        }
    }

    stage('Stop Old Container') {
        steps {
            sh 'docker stop defect-app || true'
            sh 'docker rm defect-app || true'
        }
    }

    stage('Deploy New Container') {
        steps {
            sh 'docker run -d -p 8000:8000 --name defect-app ai-defect-detection'
        }
    }
}

post {
    success {
        echo 'Deployment Successful!'
    }
    failure {
        echo 'Deployment Failed!'
    }
}
```

}
