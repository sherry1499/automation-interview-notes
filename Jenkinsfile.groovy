pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                git branch: 'main', url: 'https://github.com/sherry1499/automation-interview-notes.git'
            }
        }

        stage('安装依赖') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install pytest requests
                '''
            }
        }

        stage('单元测试') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest-cov
                    pytest test_demo.py --cov=test_demo --cov-report=term-missing -v
                '''
            }
        }

        stage('接口测试') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_login_api.py test_ask_api.py test_add_user_api.py -v -s
                '''
            }
        }

        stage('回归测试-用户管理') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_regression.py -m user_manage -v -s
                '''
            }
        }

        stage('回归测试-智能对话') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_regression.py -m dialogue -v -s
                '''
            }
        }
    }

    post {
        success {
            echo '测试通过！'
        }
        failure {
            echo '测试失败！'
        }
    }
}