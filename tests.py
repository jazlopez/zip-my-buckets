# Jaziel Lopez, Software Engineer
# ITCoEMX, Tijuana Area, BC, MX
# jaziel @ jlopez.mx
# jlopez.mx

import unittest
import logging
from src import backups

logging.basicConfig(format="%(asctime)s [%(module)s - %(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                            level=logging.INFO)


class TestCaseBackupArguments(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.backups = backups.Generator()

    def setUp(self) -> None:
        self.backups.bucket = "s3://foo"
        self.backups.profile = "default"

    def test_raise_exception_as_bucket_name_should_be_defined(self):
        self.backups.bucket = None

        with self.assertRaises(RuntimeError, msg="bucket name should be defined"):
            logging.info("bucket name %s", self.backups.bucket)

    def test_raise_exception_as_profile_name_should_be_defined(self):
        self.backups.profile = None

        with self.assertRaises(RuntimeError,  msg="profile name should be defined"):
            logging.info("profile name %s", self.backups.profile)

    def test_bucket_name_is_declared_as_uri(self):
        self.assertRegex(self.backups.bucket, "^s3://", msg="bucket name should prefixed with s3://")

    def test_profile_name_is_valid(self):
        self.assertIsNotNone(self.backups.profile)

    def test_make_temporary_directory_should_not_throw_errors(self):

        self.backups.make_temporary_directory()
        self.assertIsNotNone(self.backups.temp_directory)

    def test_make_temporary_directory_should_be_called(self):

        with self.assertRaises(RuntimeError, msg="call make temporary function first"):
            logging.info("temp directory: %s", self.backups.temp_directory)

    def test_tokenize_command(self):

        self.assertNotEqual(len(self.backups.tokenize_command()), 0)

if __name__ == '__main__':
    unittest.main()




