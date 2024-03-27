"""
Django command to wait for database to available connection
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for database to available connection

    """

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database to....")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database Unavailable, waiting 1 seconds...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available"))
