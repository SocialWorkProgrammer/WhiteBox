pipeline {
    agent any

    // tools {
    //     jdk ("jdk17")
    // }
    environment {
        // SSH_CREDENTIALS_ID = "${env.SSH_CREDENTIALS_ID}"
        SSH_CREDENTIALS_ID = "credentails-ssh"
        REMOTE_SERVER = "j11a104.p.ssafy.io"
        FRONTEND_DIR = 'frontend'
        BACKEND_DIR = 'backend'
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        // 1. 현재 빌드가 진행 중인 브랜치 정보 출력
        stage('Print Branch Info') {
            steps {
                script {
                    // echo "Using SSH_CREDENTIALS_ID: ${env.SSH_CREDENTIALS_ID}" 
                    echo "Current GIT_BRANCH: ${env.GIT_BRANCH}"
                    def branch = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                    echo "Current branch: ${branch}"
                    echo "REMOTE_SERVER: ${env.REMOTE_SERVER}"
                    echo "BRANCH_NAME: ${env.BRANCH_NAME}"
                }
            }
        }

        // 2. 코드 체크아웃
        stage('Checkout') {
            when {
                anyOf {
                    // expression { env.GIT_BRANCH == 'origin/FE-Develop' }
                    // expression { env.GIT_BRANCH == 'origin/BE-Develop' }
                    expression { env.GIT_BRANCH == 'origin/master' }
                    expression { env.GIT_BRANCH == 'origin/jenkins-test' }
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        git branch: 'master', credentialsId: 'jenkins', url: 'https://lab.ssafy.com/s11-ai-image-sub1/S11P21A104.git'
                    } else if (env.BRANCH_NAME == 'FE-Develop') {
                        git branch: 'FE-Develop', credentialsId: 'jenkins', url: 'https://lab.ssafy.com/s11-ai-image-sub1/S11P21A104.git'
                    } else if (env.BRANCH_NAME == 'BE-Develop') {
                        git branch: 'BE-Develop', credentialsId: 'jenkins', url: 'https://lab.ssafy.com/s11-ai-image-sub1/S11P21A104.git'
                    } else if (env.BRANCH_NAME == 'jenkins-test') {
                        git branch: 'jenkins-test', credentialsId: 'jenkins', url: 'https://lab.ssafy.com/s11-ai-image-sub1/S11P21A104.git'
                    }
                }
            }
        }

        // 3. 디렉토리 리스트 출력
        stage('List Directory') {
            steps {
                sh 'mkdir -p frontend'
                sh 'mkdir -p backend/whitebox'
                sh 'ls -l'
                sh 'ls -l frontend'
                sh 'ls -l backend/whitebox'
            }
        }

        // 4. Docker 이미지 빌드
        stage('Build Docker Images') {
            when {
                anyOf {
                    expression { env.GIT_BRANCH == 'origin/FE-Develop'}
                    expression { env.GIT_BRANCH == 'origin/BE-Develop'}
                    expression { env.GIT_BRANCH == 'origin/master'}
                    expression { env.GIT_BRANCH == 'origin/jenkins-test' }
                }
            }
            steps {
                script {
                    sh 'docker pull geunwook/frontend1:latest'
                    // 백엔드 dir로 이동해 Gradle 빌드 실행
                    dir('backend/whitebox') {
                        sh 'chmod +x gradlew'
                        sh './gradlew build'
                    }
                    sh 'ls -l backend/whitebox/build/libs/'
                    // sh 'docker build -t geunwook/backend backend/whitebox'
                    sh 'docker pull geunwook/backend'
                    sh 'docker pull geunwook/backend-ai1'
                }
            }
        }

        // 5. 원격 서버에 배포
        stage('Deploy to Remote Server') {
            when {
                anyOf {
                    expression { env.GIT_BRANCH == 'origin/FE-Develop' }
                    expression { env.GIT_BRANCH == 'origin/BE-Develop' }
                    expression { env.GIT_BRANCH == 'origin/master' }
                    expression { env.GIT_BRANCH == 'origin/jenkins-test' }
                }
            }
            steps {
                script {
                    sshagent([SSH_CREDENTIALS_ID]) {
                        sh '''
                        docker save geunwook/frontend1:latest | ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_SERVER} 'docker load'
                        docker save geunwook/backend | ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_SERVER} 'docker load'
                        docker save geunwook/backend-ai1 | ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_SERVER} 'docker load'

                        scp -o StrictHostKeyChecking=no ${DOCKER_COMPOSE_FILE} ubuntu@${REMOTE_SERVER}:/home/ubuntu

                        ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_SERVER} << EOF
                            cd /home/ubuntu
                            docker-compose -f ${DOCKER_COMPOSE_FILE} down
                            docker-compose -f ${DOCKER_COMPOSE_FILE} up -d
EOF
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            // 파이프라인 실행 후 워크스페이스 정리 (불필요한 파일 삭제)
            cleanWs()
        }
    }
}