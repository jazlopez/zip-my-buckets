# Jaziel Lopez, Software Engineer
# ITCoEMX, Tijuana Area, BC, MX
# jaziel @ jlopez.mx
# jlopez.mx

import tempfile
import logging

logging.basicConfig(format="%(asctime)s [%(module)s - %(funcName)s:%(lineno)s] %(levelname)s: %(message)s", level=logging.INFO)

class Generator(object):

    def __init__(self):

        self._bucket = None
        self._profile = None
        self._temp_directory = None

        logging.info("initialization values for backup generator done")

    @property
    def bucket(self):
        if not self._bucket:
            raise RuntimeError("bucket name is not assigned and cannot be empty")

        return self._bucket

    @property
    def profile(self):
        if not self._profile:
            raise RuntimeError("profile name is not assigned and cannot be empty")

        return self._profile

    @property
    def temp_directory(self):
        if not self._temp_directory:
            raise RuntimeError("make_temporary_directory function should be called first")

        return self._temp_directory

    @bucket.setter
    def bucket(self, value):
        self._bucket  = value

    @profile.setter
    def profile(self, value):
        self._profile  = value

    def make_temporary_directory(self):
        """
        :return:
        """
        self._temp_directory = tempfile.TemporaryDirectory()
        logging.info("temporary directory used as swap space created at: %s", self.temp_directory)


if __name__ == '__main__':
    pass
