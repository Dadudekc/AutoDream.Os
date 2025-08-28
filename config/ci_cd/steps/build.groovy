def call(cfg) {
    sh '''
        python -m pip install --upgrade pip
        pip install -r requirements-testing.txt
        pip install pre-commit
        pre-commit run --all-files
        python tests/v2_standards_checker.py --all-checks --strict
    '''
}
