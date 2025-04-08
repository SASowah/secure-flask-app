pipeline {
    agent { label 'jenkins-agent' }

    environment {
        ANSIBLE_PLAYBOOK = 'app_server.yml'
        INVENTORY_FILE = 'hosts_inventory1.ini'
        ARTIFACT_NAME = "secure-flask-app.tar.gz"
        HASH_FILE = "hash.txt"
        DUCKDNS_TOKEN = credentials('duckdns-token')
        DUCKDNS_DOMAIN = 'secureflask.duckdns.org'
        EMAIL_RECIPIENTS = "samsoo18@yahoo.com, tola.komaiya@gmail.com"
        TEST_SERVER_URL = "https://secureflask.duckdns.org"
        APP_SERVER_IP = '13.48.26.31'
        APP_SERVER_USER = 'ubuntu'
        APP_SERVER_HOST = 'app-server'
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    git branch: "dev",
                        url: 'https://github.com/SASowah/secure-flask-app.git'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'ls -l src/requirements.txt'
                    sh 'pip3 install -r src/requirements.txt'
                }
            }
        }

        stage('Static Analysis (Code Quality)') {
            steps {
                script {
                    sh 'pip3 install pylint'
                    sh 'pylint src/'
                }
            }
        }

        stage('Archive Application') {
            steps {
                sh 'tar -czf secure-flask-app.tar.gz src/'
                sh 'sha256sum $ARTIFACT_NAME | awk \'{print $1}\' > $HASH_FILE'
                archiveArtifacts artifacts: 'secure-flask-app.tar.gz, hash.txt', fingerprint: true
            }
        }

        stage('Verify Artifact Integrity') {
            steps {
                sh '''
                    CALCULATED_HASH=$(sha256sum $ARTIFACT_NAME | awk '{print $1}')
                    EXPECTED_HASH=$(cat $HASH_FILE)

                    if [ "$CALCULATED_HASH" != "$EXPECTED_HASH" ]; then
                        echo "❌ Artifact integrity verification failed!"
                        exit 1
                    else
                        echo "✅ Artifact integrity verified!"
                    fi
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sshagent (credentials: ['app-server']) {
                    sh '''
                        echo "Starting Ansible deployment..."
                        ansible-playbook -i $INVENTORY_FILE $ANSIBLE_PLAYBOOK || {
                            echo "❌ Ansible deployment failed!"
                            exit 1
                        }
                    '''
                }
            }
        }

stage('Update DuckDNS IP') {
    steps {
        script {
            sh """
            curl -k "https://www.duckdns.org/update?domains=${DUCKDNS_DOMAIN}&token=${DUCKDNS_TOKEN}&ip=${APP_SERVER_IP}"
            """
        }
    }
}

//stage('Test Deployment') {
//   steps {
//        script {
//            sh """
//           ssh ${APP_SERVER_USER}@${APP_SERVER_IP} '
//                for i in {1..5}; do
//                    if curl -sfk ${TEST_SERVER_URL}; then
//                        exit 0
//                    fi
//                    sleep 10
//                done
//                echo "❌ App did not become reachable after 5 attempts"
//                exit 1
//            '
//            """
//        }
//    }
//}

        stage('Cleanup and Rollback (If Necessary)') {
            when {
                expression {
                    return currentBuild.result == 'FAILURE'
                }
            }
            steps {
                script {
                    echo "Rolling back deployment due to failure..."
                    // Implement rollback logic here if needed
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment complete! Visit your app at https://secureflask.duckdns.org.'
            mail to: EMAIL_RECIPIENTS,
                 subject: "Deployment Success: secure-flask-app",
                 body: "The deployment of secure-flask-app was successful!"
        }
        failure {
            echo '❌ Build Failed! Check logs for issues.'
            mail to: EMAIL_RECIPIENTS,
                 subject: "Deployment Failed: secure-flask-app",
                 body: "The deployment of secure-flask-app has failed. Please check the logs for details."
        }
    }
}
