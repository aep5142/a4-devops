pipeline {
    agent any

    environment {
        BRANCH_PUSH = "${env.GIT_BRANCH ?: 'unknown'}"
        VERSION = "1.0.${env.BUILD_NUMBER}"
        ARTIFACT_NAME = "app-${VERSION}.zip"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    def scmInfo = checkout scm
                    env.BRANCH_PUSH = scmInfo.GIT_BRANCH
                }
            }
        }

        stage('Build') {
            steps {
                echo "Building branch from: ${env.BRANCH_PUSH}"
                sh """
                    mkdir -p dist
                    zip -r dist/${ARTIFACT_NAME} app/ uv.lock
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                    /opt/homebrew/bin/sonar-scanner \
                        -Dsonar.projectKey=a4-devops \
                        -Dsonar.sources=app \
                        -Dsonar.exclusions=**/.git/**,**/__pycache__/**,**/.venv/**,**/dist/** \
                        -Dsonar.scm.disabled=true
                    """
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: false
            }
        }
    }

    post {
        success {
            script {
                // Forzamos el uso de la API de hooks para evitar errores de autodescubrimiento del plugin
                slackSend(
                    baseUrl: 'https://hooks.slack.com/services/',
                    tokenCredentialId: 'slack-v3-a4',
                    channel: '#a4_devops_aep',
                    color: 'good',
                    message: "✅ Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (Branch: ${env.BRANCH_PUSH})"
                )
            }
        }
        failure {
            script {
                slackSend(
                    baseUrl: 'https://hooks.slack.com/services/',
                    tokenCredentialId: 'slack-v3-a4',
                    channel: '#a4_devops_aep',
                    color: 'danger',
                    message: "❌ Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (Branch: ${env.BRANCH_PUSH})"
                )
            }
        }
    }
}