"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class QueryTest(TestCase):
    def test_email_query(self):
        """
        Tests to see if an email address is already in the db
        """
        return models.InvitationManager.objects.filter(email=invited_email_address)
