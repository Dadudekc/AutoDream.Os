return [
    PYTHON_VERSION: '3.9',
    COVERAGE_THRESHOLD: '80',
    PIP_CACHE_DIR: '.pip-cache',
    TEST_RESULTS_DIR: 'test-results',
    COVERAGE_DIR: 'htmlcov',
    ARTIFACT_EXPIRATION: '7',
    DOCKER_IMAGE: 'python:3.9-slim',
    DOCKER_ARGS: '-v /var/run/docker.sock:/var/run/docker.sock'
]
