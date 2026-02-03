pipeline {
    agent any   // default agent for Build, Sonar, Archive

    environment {
        BRANCH_PUSH = "${env.GIT_BRANCH ?: 'unknown'}"
        VERSION = "1.0.${env.BUILD_NUMBER}"
        ARTIFACT_NAME = "app-${VERSION}.zip"
        SLACK_WEBHOOK = credentials('slack-v3-a4')
    }

    stages {

        stage('Build') {
            steps {
                echo "Building branch from: ${env.BRANCH_PUSH}"
                echo "Building version ${VERSION}"
                echo "Testing with agent any!!"
                echo "Slack webhook is ${SLACK_WEBHOOK}"

                sh """
                    mkdir -p dist
                    zip -r dist/${ARTIFACT_NAME} app/ uv.lock
                """
            }
        }

        stage('Test') {
            // agent { label 'test' }
            when {
                expression { env.BRANCH_PUSH == 'test-branch' }
            }
            steps {
                echo 'Running tests not in main branch!'
                // sh 'pytest'  (example)
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
            /opt/homebrew/bin/sonar-scanner \
                -Dsonar.projectKey=a4-devops \
                -Dsonar.sources=app \
                -Dsonar.exclusions=**/__pycache__/**,**/*.pyc,**/.env,**/node_modules/**
            """
        }
        }
}

        /*
        stage('Quality Gate') {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate abortPipeline: true
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate: ${qg.status}"
                        }
                    }
                }
            }
        }
        */



        stage('Deploy') {
            // agent { label 'deploy' }  // 👈 DEPLOY AGENT
            when {
                expression { env.BRANCH_PUSH == 'deploy-branch' }
            }
            steps {
                echo "Deploying ${ARTIFACT_NAME}"
                // sh './deploy.sh'
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
                // We use only the minimal required fields to let the plugin handle the URL logic
                slackSend(
                    color: 'good',
                    tokenCredentialId: 'slack-v3-a4',
                    channel: '#a4_devops_aep', 
                    message: "✅ Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (Branch: ${env.BRANCH_PUSH})",
                    failOnError: true
                )
            }
        }
        failure {
            script {
                slackSend(
                    color: 'danger',
                    tokenCredentialId: 'slack-v3-a4',
                    channel: '#a4_devops_aep',
                    message: "❌ Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (Branch: ${env.BRANCH_PUSH})",
                    failOnError: true
                )
            }
        }
    }
}

