def call(cfg) {
    docker.image(cfg.DOCKER_IMAGE).inside(cfg.DOCKER_ARGS) {
        sh '''
            python -m pip install --upgrade pip
            pip install -r requirements.txt
            pip install pre-commit
            pre-commit run --all-files
        '''
    }
}
