# stdlib
import contextlib
import importlib
import os
import sys
from datetime import datetime
# local
from membership.models.integrity_test import IntegrityTest


__all__ = [
    'integrity_tests',
    'output_errors',
    'register',
]


class _TestRunner:  # pragma: no cover

    def __init__(self):
        self._tests = {}

    def _import_tests(self):
        path_chunks = self.__module__.split('.')[:-1]

        path_chunks.append('tests')
        path_to_tests = '/'.join(path_chunks)
        test_modules = os.listdir(path_to_tests)

        for module in test_modules:
            if module.endswith('.py') and not module.startswith('_'):
                module_name = module[:-3]
                importlib.import_module('.'.join([*path_chunks, module_name]))

    def run_all_tests(self, output_file=None):
        self._import_tests()
        errors = inspected = 0
        start = datetime.utcnow()
        with file_or_stdout(output_file) as fp:
            fp.write('Beginning tests\n{}\n'.format(start))

        for name, test in self._tests.items():
            results = test(output_file)
            errors += results.get('errors_found', 0)
            inspected += results.get('records_inspected', 0)
        finish = datetime.utcnow()

        with file_or_stdout(output_file) as fp:
            fp.write('\nTests completed\n{}\n'.format(finish))

        # Save the results
        IntegrityTest.objects.create(
            errors_found=errors,
            records_inspected=inspected,
            start_time=start,
            finish_time=finish,
        )

    def register(self, func):
        self._tests[func.__name__] = func


integrity_tests = _TestRunner()


def register(func):
    integrity_tests.register(func)
    return func


def output_errors(file, header, records):
    with file_or_stdout(file) as fp:
        fp.write(header)
        for record in records:
            fp.write(', '.join(map(str, record)) + '\n')


@contextlib.contextmanager
def file_or_stdout(file):
    if file is None:
        yield sys.stdout  # pragma: no cover
    else:
        with open(file, 'a') as out_file:
            yield out_file
