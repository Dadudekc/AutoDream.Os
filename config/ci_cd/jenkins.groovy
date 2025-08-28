def cfg = load 'config/ci_cd/config.groovy'
def buildStep = load 'config/ci_cd/vars/build.groovy'
def testStep = load 'config/ci_cd/vars/test.groovy'
def deployStep = load 'config/ci_cd/vars/deploy.groovy'

pipeline {
    agent any

    environment {
        PYTHON_VERSION    = cfg.PYTHON_VERSION
        PIP_CACHE_DIR     = "${WORKSPACE}/${cfg.PIP_CACHE_DIR}"
        COVERAGE_THRESHOLD = cfg.COVERAGE_THRESHOLD
        TEST_RESULTS_DIR   = "${WORKSPACE}/${cfg.TEST_RESULTS_DIR}"
        COVERAGE_DIR       = "${WORKSPACE}/${cfg.COVERAGE_DIR}"
        ARTIFACT_EXPIRATION = cfg.ARTIFACT_EXPIRATION
    }

    options {
        timeout(time: 2, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Build') {
            steps {
                script { buildStep(cfg) }
            }
        }

        stage('Test') {
            steps {
                script { testStep(cfg) }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                script { deployStep(cfg) }
            }
        }
    }
}
