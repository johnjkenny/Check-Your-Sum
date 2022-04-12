#!/usr/bin/env python3


__author__ = 'John J Kenny'
__version__ = '1.0.0'


from argparse import ArgumentParser
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
from genericpath import isfile

from PrettifyLogging.prettify_logging import PrettifyLogging


class CheckSum(PrettifyLogging):
    def __init__(self, **kwargs):
        super().__init__()
        self.hash_algorithm = None
        self.name = kwargs['name'] if 'name' in kwargs else 'check-your-sum.log'
        self.ingest = kwargs['ingest'] if 'ingest' in kwargs else None
        self.ingest_type = str(kwargs['ingest_type']).lower() if 'ingest_type' in kwargs else None
        self.hash_type = kwargs['hash_type'] if 'hash_type' in kwargs else None
        self.verify_sum = kwargs['verify_sum'] if 'verify_sum' in kwargs else None
        self.hashes = {'md5': md5, 'sha1': sha1, 'sha224': sha224, 'sha256': sha256, 'sha384': sha384, 'sha512': sha512}
        self.log = self.configure()

    def get_hash_algorithm(self, hash_type: str = 'sha256'):
        if self.hash_type is not None:
            try:
                return self.hashes[hash_type.lower()]()
            except KeyError:
                self.log.error('Hash algorithm "{}" not found. Please use one of the following: {}'.format(
                    hash_type.lower(), ', '.join(list(self.hashes.keys()))))
        self.log.error('Hash algorithm "{}" not found. Please use one of the following: {}'.format(
            self.hash_type, ', '.join(list(self.hashes.keys()))))
        return None

    def create_hash(self):
        self.hash_algorithm = self.get_hash_algorithm(self.hash_type)
        if self.hash_algorithm is not None:
            error_found = self._run_ingest_type()
            if not error_found:
                return self._create_digest()
        return None, None

    def _run_ingest_type(self):
        if self.ingest_type == 'file':
            return self._try_read_file()
        if self.ingest_type == 'string':
            return self._encode_string()
        self.log.error('Ingest type not found. Please use one of the following: file, string')
        return True

    def _create_digest(self):
        digest = self.hash_algorithm.hexdigest()
        if self.verify_sum is not None:
            if digest == self.verify_sum:
                self.print_message('{}: {} == Checksum: {}'.format(
                    self.hash_algorithm.name, digest, self.verify_sum), 'green')
                return digest, True
            self.print_message('{}: {} != Checksum {}'.format(
                self.hash_algorithm.name, digest, self.verify_sum), 'red')
            return digest, False
        self.print_message('{}: {}'.format(self.hash_algorithm.name, digest), 'cyan')
        return digest, None

    def create_all_hashes(self):
        self.verify_sum = None
        hash_dict = dict()
        for hash_type in self.hashes:
            self.hash_type = hash_type
            hash_dict[hash_type] = self.create_hash()[0]
        return hash_dict

    def _try_read_file(self):
        if isinstance(self.ingest, str) and isfile(self.ingest):
            try:
                with open(self.ingest, 'rb') as file:
                    def read_file_chunk():
                        return file.read(4096)
                    for file_chunk in iter(read_file_chunk, b''):
                        self.hash_algorithm.update(file_chunk)
                return False
            except Exception:
                self.log.exception('Error reading file {}'.format(self.ingest))
                return True
        self.log.error('File not found: {}, Type: {}'.format(self.ingest, type(self.ingest)))
        return True

    def _encode_string(self):
        if isinstance(self.ingest, str):
            self.hash_algorithm.update(self.ingest.encode('utf-8'))
            return False
        self.log.error('String not found: {}, Type: {}'.format(self.ingest, type(self.ingest)))
        return True


class ArgParser(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.hash_types = list(CheckSum().hashes.keys())
        self.hash_types.append('all')
        self.description = 'Check-Your-Sum - A simple command line utility to check the integrity of files and stings'
        self._add_arguments()
        self.args = vars(self.parse_args())

    def _add_arguments(self):
        self.add_argument('-i', '--ingest', help='File or string to be hashed', required=True)
        self.add_argument('-it', '--ingest_type', nargs='?', choices=['file', 'string'], default='file',
                          help='Type of ingest (default: %(default)s)')
        self.add_argument('-ht', '--hash_type', nargs='?', choices=self.hash_types, default='sha256',
                          help='hash name (default: %(default)s)')
        self.add_argument('-vs', '--verify_sum', help='Verify the hash of the file or string')


if __name__ == '__main__':
    PARSER = ArgParser()
    if PARSER.args:
        CHECK_SUM = CheckSum(**PARSER.args)
        if CHECK_SUM.hash_type == 'all':
            CHECK_SUM.create_all_hashes()
        else:
            CHECK_SUM.create_hash()
