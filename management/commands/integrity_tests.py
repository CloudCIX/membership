# libs
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    can_import_settings = True
    help = (
        'Run tests on the DataBase to ensure it is in a valid state'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--logfile',
            action='store',
        )

    def handle(self, *args, **options):
        from membership.management.integrity.runner import integrity_tests
        file = options.get('logfile')
        integrity_tests.run_all_tests(file)
