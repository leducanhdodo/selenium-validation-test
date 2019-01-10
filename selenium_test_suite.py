import unittest
from validation_test import ValidationTest

val_test = unittest.TestLoader().loadTestsFromTestCase(ValidationTest)

# create a test suite
test_suite = unittest.TestSuite([val_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
