pipeline {
    agent any

    environment {
        BRANCH_PUSH = "${env.GIT_BRANCH ?: 'unknown'}"
        VERSION = "1.0.${env.BUILD_NUMBER}"
        ARTIFACT_NAME = "app-${VERSION}.zip"
    }

    stages {
        stage('Build') {
            steps {
                echo "Building branch from: ${env.BRANCH_PUSH}"
                
                // Example build artifact
                echo "Building version ${VERSION}"
                sh """
                    mkdir -p dist
                    zip -r dist/${ARTIFACT_NAME} .
                """
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

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
            }
        }
    }
}

