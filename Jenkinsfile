pipeline {
    agent any

    environment {
        BRANCH_PUSH = "${env.GIT_BRANCH ?: 'unknown'}"
    }

    stages {
        stage('Build') {
            steps {
                echo "Building branch from: ${env.BRANCH_PUSH}"
            }
        }

        stage('Test') {
            when {
                expression { env.BRANCH_PUSH == 'origin/main' }
            }
            steps {
                echo 'Running tests on main branch'
            }
        }

        stage('Deploy') {
            when {
                expression { env.BRANCH_PUSH == 'origin/main' }
            }
            steps {
                echo 'Deploying application from main branch'
            }
        }

        stage('Feature Checks') {
            when {
                expression { env.BRANCH_PUSH != 'origin/main' }
            }
            steps {
                echo 'Running feature branch checks'
            }
        }
    }
}

