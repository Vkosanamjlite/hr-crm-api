"""
Test Custom Django management commands using
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class TestCommands(SimpleTestCase):
    """
    Test Custom Django management commands using
    """

    @patch('core.management.commands.wait_for_db.Command.check')
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database to be available
        :return:
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_check):
        """
        Test waiting for database to be getting Operational error
        :param patched_check:
        :return:
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 10)
        patched_check.assert_called_with(databases=['default'])
