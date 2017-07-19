import unittest
import subprocess
import os
from contextlib import contextmanager


@contextmanager
def cd(dir):
    cwd = os.curdir
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


if __name__ == '__main__':
    unittest.main()
