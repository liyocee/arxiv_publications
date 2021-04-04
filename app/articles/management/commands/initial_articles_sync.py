import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings



class Command(BaseCommand):
    help = 'Start an initial sync of articles metadata from arxiv'
    requires_migrations_checks = True
    MONTHS_OFFSET_ARG = "months_offset"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
                f'--{self.MONTHS_OFFSET_ARG}',
                help='Number of months in the past from which we should fetch articles metadata',
            )


    def handle(self, *args, **options) -> None:
        months_offset = options.get(self.MONTHS_OFFSET_ARG, None)
        if not months_offset:
            months_offset = settings.INITIAL_SYNC_OFFSET_MONTHS
        self.stdout.write(self.style.NOTICE(f'Starting initial articles sync with an offset of {months_offset} months'))
