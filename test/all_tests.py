import unittest

if __name__ == '__main__':
    test_dir = '.'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)