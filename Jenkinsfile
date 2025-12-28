pipeline {
    agent any

    environment {
        // Define any global environment variables here if needed
        // Note: .env files are respected by the containers at runtime, not build time usually
        // unless explicitly used in Dockerfile (e.g. ARG)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test Microservices') {
            parallel {
                stage('LogCollector') {
                    steps {
                        script {
                            echo 'Building LogCollector...'
                            sh 'docker build -t devsecops/logcollector ./logcollector'
                            // Optional: Run unit tests inside a temporary container
                            // sh 'docker run --rm devsecops/logcollector npm test'
                        }
                    }
                }
                stage('LogParser') {
                    steps {
                        script {
                            echo 'Building LogParser...'
                            sh 'docker build -t devsecops/logparser ./logparser'
                        }
                    }
                }
                stage('VulnDetector') {
                    steps {
                        script {
                            echo 'Building VulnDetector...'
                            // Note folder name spelling: vulndetcteur
                            sh 'docker build -t devsecops/vulndetector ./vulndetcteur'
                        }
                    }
                }
                stage('FixSuggester') {
                    steps {
                        script {
                            echo 'Building FixSuggester...'
                            sh 'docker build -t devsecops/fixsuggester ./FixSuggester'
                        }
                    }
                }
                stage('ReportGenerator') {
                    steps {
                        script {
                            echo 'Building ReportGenerator...'
                            sh 'docker build -t devsecops/reportgenerator ./ReportGenerator'
                        }
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    echo 'Building Dashboard...'
                    sh 'docker build -t devsecops/dashboard ./dashboard'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build successful! Docker images are ready.'
        }
        failure {
            echo 'Build failed. Please check logs.'
        }
        cleanup {
            // Optional: Prune dangling images to save space
            // sh 'docker image prune -f'
        }
    }
}
