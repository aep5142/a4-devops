pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Test') {
            when { branch 'main' }
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
