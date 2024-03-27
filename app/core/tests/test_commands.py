from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class TestCommands(SimpleTestCase):
    """
    Test custom Django management commands
    """

    @patch('core.management.commands.wait_for_db.Command.check')
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for the database to be available
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_with(databases=['default'])

    @patch('core.management.commands.wait_for_db.Command.check')
    @patch('time.sleep', return_value=None)
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for the database while getting Operational errors
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
