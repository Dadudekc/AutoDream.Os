def call(cfg) {
    docker.image(cfg.DOCKER_IMAGE).inside(cfg.DOCKER_ARGS) {
        sh """
            mkdir -p ${env.TEST_RESULTS_DIR}
            pytest --junitxml=${env.TEST_RESULTS_DIR}/results.xml --cov --cov-report=html:${env.COVERAGE_DIR}
        """
    }
    junit "${env.TEST_RESULTS_DIR}/results.xml"
    publishHTML(target: [
        reportDir: env.COVERAGE_DIR,
        reportFiles: 'index.html',
        reportName: 'Coverage'
    ])
}
