"""
Tests for the "deploy" plugin filter
"""

from ansible.compat.tests import unittest
from ansible.errors import AnsibleFilterError

from plugins.filter.deploy import blue_green_host, blue_green_hosts


class TestBlueGreenHostFilter(unittest.TestCase):
    """Tests for the ``blue_green_host`` filter"""

    def test_with_empty_prefix(self):
        """When the prefix is empty, the host should be left unmodified"""

        host = "foo.com"

        self.assertEqual(blue_green_host(host), host)
        self.assertEqual(blue_green_host(host, prefix=""), host)

    def test_with_not_allowed_prefix(self):
        """If prefix is not allowed, we should raise an error"""

        host = "foo.com"

        with self.assertRaises(AnsibleFilterError) as context_manager:
            blue_green_host(host, prefix="spam")
        self.assertEqual(
            context_manager.exception.message,
            "prefix 'spam' is not allowed (must be in ['previous', 'current', 'next'])",
        )

    def test_with_current_prefix(self):
        """When the prefix is "current", the host should be left unmodified"""

        host = "foo.com"

        self.assertEqual(blue_green_host(host, "current"), host)

    def test_with_next_previous_prefix(self):
        """When next or previous prefixes are used, the host should be modified"""

        host = "foo.com"

        self.assertEqual(blue_green_host(host, "previous"), "previous.{}".format(host))
        self.assertEqual(blue_green_host(host, "next"), "next.{}".format(host))


class TestBlueGreenHostsFilter(unittest.TestCase):
    """Tests for the ``blue_green_hosts`` filter"""

    def test_with_empty_host(self):
        """When the host is empty, the filter should raise an error"""

        with self.assertRaises(AnsibleFilterError) as context_manager:
            blue_green_hosts(None)
        self.assertEqual(context_manager.exception.message, "host cannot be empty")

        with self.assertRaises(AnsibleFilterError) as context_manager:
            blue_green_hosts("")
        self.assertEqual(context_manager.exception.message, "host cannot be empty")

    def test_with_valid_base_host(self):
        """Test the filter with a valid host"""

        host = "foo.com"

        self.assertEqual(
            blue_green_hosts(host), "previous.foo.com,foo.com,next.foo.com"
        )
