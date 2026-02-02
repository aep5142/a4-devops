pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${env.GIT_BRANCH}"
            }
        }

        stage('Test') {
            when { branch 'origin/main' }
            steps { echo 'Running tests on main branch' }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps { echo 'Deploying application from main branch' }
        }

        stage('Feature Checks') {
            when { not { branch 'main' } }
            steps { echo 'Running feature branch checks' }
        }
    }
}
