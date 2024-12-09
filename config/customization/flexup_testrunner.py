import os
import unittest
from redgreenunittest.django.runner import RedGreenDiscoverRunner

class FlexUpTestRunner(RedGreenDiscoverRunner):
    IGNORED_DIRS = {'__pycache__', 'migrations', '.git', '.venv', 'venv', 'env'}

    def build_suite(self, test_labels=None, **kwargs):
        suite = unittest.TestSuite()

        # Get all tests from default discovery (which looks for test_*.py)
        suite.addTests(super().build_suite(test_labels))

        # Custom discovery logic
        if not test_labels:
            test_labels = ['.']

        for test_label in test_labels:
            # print(f"\nSearching for tests in: {test_label}")

            for root, dirs, files in os.walk(test_label):
                # Skip directories we want to ignore
                dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRS]

                # print(f"\nExamining directory: {root}")
                # print(f"Files found: {files}")

                try:
                    # Make sure the directory is a Python package
                    if not os.path.exists(os.path.join(root, '__init__.py')):
                        # print(f"Skipping {root} - no __init__.py found")
                        continue

                    # If we're in a 'tests' directory, look for all .py files
                    if os.path.basename(root) == 'tests':
                        # print(f"Found 'tests' directory: {root}")
                        python_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
                        # print(f"Looking for test files: {python_files}")

                        for test_file in python_files:
                            try:
                                module_name = f"{test_label}.tests.{test_file[:-3]}"
                                # print(f"Attempting to load tests from: {module_name}")
                                module = __import__(module_name, fromlist=['*'])
                                for item in dir(module):
                                    obj = getattr(module, item)
                                    if isinstance(obj, type) and issubclass(obj, unittest.TestCase) and obj != unittest.TestCase:
                                        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(obj))
                            except Exception as e:
                                # print(f"Error loading {test_file}: {str(e)}")
                                continue

                except ImportError as e:
                    # print(f"Import error in {root}: {str(e)}")
                    continue
                except Exception as e:
                    # print(f"Error processing {root}: {str(e)}")
                    continue

        total_tests = suite.countTestCases()
        # print(f"\nTotal tests found: {total_tests}")
        return suite