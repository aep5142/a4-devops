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

        stage('Setup Python Env') {
            steps {
                sh '''
                # Create a virtual environment in the workspace
                python3 -m venv venv
                
                # Activate it
                source venv/bin/activate

                # Upgrade pip just in case
                pip install --upgrade pip

                # Install all packages from requirements.txt
                pip install -r app/requirements.txt
                '''
            }
        }

        stage("Compose Docker") { 
            steps {
                """
                docker-compose up --build
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
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate abortPipeline: true
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to Quality Gate: ${qg.status}"
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
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: false
            }
        }
    }

    post {
    success {
        slackSend(
            color: 'good',
            message: "✅ Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (Branch: ${env.BRANCH_PUSH})"
        )
    }
    failure {
            script {
                // We add the Build URL so you can click directly to the error logs
                def buildUrl = "${env.BUILD_URL}console"
                slackSend(
                    tokenCredentialId: 'slack-v4',
                    channel: '#all-a4devopswp',
                    color: 'danger',
                    message: "❌ Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}\nBranch: ${env.BRANCH_PUSH}\nDuration: ${currentBuild.durationString}\nCheck logs here: ${buildUrl}"
                )
            }
}
}
}

