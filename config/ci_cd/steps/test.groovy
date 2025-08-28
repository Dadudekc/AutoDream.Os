def call(cfg) {
    sh """
        mkdir -p ${env.TEST_RESULTS_DIR}
        python -m pytest tests/ \\
            --cov=src \\
            --cov-report=xml \\
            --cov-report=html \\
            --cov-report=term-missing \\
            --cov-fail-under=${env.COVERAGE_THRESHOLD} \\
            --junitxml=${env.TEST_RESULTS_DIR}/results.xml
    """
    junit "${env.TEST_RESULTS_DIR}/results.xml"
    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
}
