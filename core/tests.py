"""Basic tests for the core app."""

from django.test import TestCase


class SmokeTest(TestCase):
    """Very simple smoke test to ensure the test framework runs."""

    def test_true_is_true(self):
        """Assert that True is indeed True."""
        self.assertTrue(True)
