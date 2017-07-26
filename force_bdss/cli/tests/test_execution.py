import unittest
import subprocess
import os
from contextlib import contextmanager

from force_bdss.tests import fixtures


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
        with cd(fixtures.dirpath()):
            out = subprocess.check_call(["force_bdss", "test_csv.json"])
            self.assertEqual(out, 0)

    def test_plain_invocation_evaluate(self):
        with cd(fixtures.dirpath()):
            proc = subprocess.Popen([
                "force_bdss", "--evaluate", "test_csv.json"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            proc.communicate(b"1")
            retcode = proc.wait()
            self.assertEqual(retcode, 0)

    def test_unsupported_file_input(self):
        with cd(fixtures.dirpath()):
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.check_call(["force_bdss", "test_csv_v2.json"])

    def test_corrupted_file_input(self):
        with cd(fixtures.dirpath()):
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.check_call(["force_bdss",
                                       "test_csv_corrupted.json"])


if __name__ == '__main__':
    unittest.main()
