"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import models


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class QueryTest(TestCase):
    def test_invite_requsts(self):
        return models.InvitationManager.objects.all()
        
    def runTest(self):
        print(self.test_invite_requests())
