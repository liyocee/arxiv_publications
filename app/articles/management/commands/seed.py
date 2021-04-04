from seeders.seeder import DatabaseSeeder
from django.core.management.base import BaseCommand
import inspect
from seeders import base


class Command(BaseCommand):
    help = 'Seed initial database data'
    requires_migrations_checks = True

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.NOTICE(self.help))
        self.seed_db()

    def seed_db(self) -> None:
        """
        Discover seeder classes using reflection and invoke the seed method
        """
        seeders = inspect.getmembers(base, inspect.isclass)
        for seeder_entry in seeders:
            seeder_cls_name = seeder_entry[0]
            seeder_cls = seeder_entry[1]

            if not issubclass(seeder_cls, DatabaseSeeder):
                continue
            try:
                seeder: DatabaseSeeder = seeder_cls()
                seeder.seed()
            except Exception as ex:
                self.stdout.write(self.style.ERROR(
                    f'Error seeding data for seeder: {seeder_cls_name} . Message: {ex}'
                ))
