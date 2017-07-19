import unittest
import subprocess
import os
from contextlib import contextmanager


@contextmanager
def cd(dir):
    cwd = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(cwd)


def fixture_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fixtures")


class TestExecution(unittest.TestCase):
    def test_plain_invocation_mco(self):
        with cd(fixture_dir()):
            out = subprocess.check_call(["force_bdss", "test_csv.json"])
            self.assertEqual(out, 0)

    def test_unsupported_file_input(self):
        with cd(fixture_dir()):
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.check_call(["force_bdss", "test_csv_v2.json"])


if __name__ == '__main__':
    unittest.main()
