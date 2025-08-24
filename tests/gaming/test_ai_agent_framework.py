import sys
import unittest

MODULES = [
    "tests.gaming.test_ai_agent_framework_setup",
    "tests.gaming.test_ai_agent_framework_execution",
    "tests.gaming.test_ai_agent_framework_validation",
    "tests.gaming.test_ai_agent_framework_cleanup",
]

def load_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for name in MODULES:
        module = __import__(name, fromlist=["*"])
        suite.addTests(loader.loadTestsFromModule(module))
    return suite

def run_all_tests():
    print("🤖 Running AI Agent Framework Tests...")
    result = unittest.TextTestRunner(verbosity=2).run(load_tests())
    print("\n📊 AI AGENT FRAMEWORK TEST RESULTS:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    return result

if __name__ == "__main__":
    sys.exit(0 if run_all_tests().wasSuccessful() else 1)
