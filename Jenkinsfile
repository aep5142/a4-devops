pipeline {
    agent any   // default agent for Build, Sonar, Archive

    environment {
        BRANCH_PUSH = "${env.GIT_BRANCH ?: 'unknown'}"
        VERSION = "1.0.${env.BUILD_NUMBER}"
        ARTIFACT_NAME = "app-${VERSION}.zip"
    }

    stages {

        stage('Build') {
            steps {
                echo "Building branch from: ${env.BRANCH_PUSH}"
                echo "Building version ${VERSION}"
                echo "Testing with agent any!!"

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

        stage('Quality Gate') {
            steps {
                script {
                    timeout(time: 10, unit: 'MINUTES') {
                def qg = waitForQualityGate abortPipeline: false
                if (qg.status != 'OK') {
                    error "Pipeline aborted due to quality gate: ${qg.status}"
                }
            }
            }
        }
        }


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
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
            }
        }
    }
}

