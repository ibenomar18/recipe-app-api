"""
Test custom Django management commands.
"""

from unittest.mock import patch  # to mock the behavior of the database

from psycopg2 import OperationalError as Psycopg2Error  # Errors we expect

from django.core.management import call_command
from django.db.utils import OperationalError  # Errors we expect
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready. """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        """Explanation of what's going in these lines:
        The first 2 times that we call the mocked method, we want it to
        raise a Psycopg2Error. Then we raise 3 OperationalError. 2 & 3
        are arbitrary values, can be modified to be more/less exceptions
        to mock receive from the database then it'll return a true value."""

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        # 6 = 2 Psycopg2Error, 3 OperationalError, 1 True
        patched_check.assert_called_with(databases=['default'])
