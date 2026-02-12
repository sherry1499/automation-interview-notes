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
                sh 'pip install pytest'
            }
        }

        stage('运行测试') {
            steps {
                sh 'pytest test_demo.py -v'
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