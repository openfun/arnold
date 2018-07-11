"""
Tests for the "merge" plugin filter
"""
from copy import deepcopy

from ansible.compat.tests import unittest
from ansible.errors import AnsibleFilterError

from plugins.filter.merge import merge_with_app


# pylint: disable=invalid-name
def deep_sort_dict(d):
    """
        Recursively alphabetically sort lists as dictionary values (input dict
        is not modified)
    """
    res = {}
    for k, v in d.iteritems():
        if isinstance(v, (list, tuple)):
            l = []  # noqa: E741
            for i in v:
                if isinstance(i, dict):
                    l.append(deep_sort_dict(i))
                else:
                    l.append(deepcopy(i))
            res[k] = sorted(l)
        elif isinstance(v, dict):
            res[k] = deep_sort_dict(v)
        else:
            res[k] = deepcopy(v)
    return res


# pylint: disable=no-self-use
class TestDeepSortDict(unittest.TestCase):
    """Test the ``deep_sort_dict`` utility"""

    def test_immutability(self):
        """Test that our implementation does not modify submitted dict in place"""

        d = {"foo": 1, "bar": ["c", "b", "d", "a"]}
        s = deep_sort_dict(d)

        assert d != s
        assert d == {"foo": 1, "bar": ["c", "b", "d", "a"]}

    def test_flat_dict(self):
        """Test (non nested) dictionary sorting"""

        d = {"foo": 1, "bar": ["c", "b", "d", "a"]}
        expected = {"foo": 1, "bar": ["a", "b", "c", "d"]}

        assert deep_sort_dict(d) == expected

    def test_nested_dict(self):
        """Test nested dictionnary sorting"""

        d = {"foo": {"baz": [4, 5, 6, 1]}, "bar": ["c", "b", "d", "a"]}
        expected = {"foo": {"baz": [1, 4, 5, 6]}, "bar": ["a", "b", "c", "d"]}

        assert deep_sort_dict(d) == expected

    def test_deeply_nested_dict(self):
        """Test deeply nested dictionnary sorting"""

        d = {
            "foo": {"baz": [4, 1, 6, {"lol": ["x", "z", "y"]}]},
            "bar": ["c", "b", "d", "a"],
        }
        expected = {
            "foo": {"baz": [1, 4, 6, {"lol": ["x", "y", "z"]}]},
            "bar": ["a", "b", "c", "d"],
        }

        assert deep_sort_dict(d) == expected


class TestMergeWithAppFilter(unittest.TestCase):
    """Tests for the ``merge_with_app`` filter"""

    # View the full diff upon test failure
    maxDiff = None

    def assertDictDeepEqual(self, a, b):
        """
            Compare deeply sorted dictionaries (aka apps) to avoid false
            positive (list ordering differences is not relevant when comparing
            apps-related data)
        """

        assert deep_sort_dict(a) == deep_sort_dict(b)

    def test_submitted_types_to_merge(self):
        """``base`` and ``new`` arguments should both be dictionaries"""

        for args in (({}, []), ([], {}), ([], [])):
            with self.assertRaises(AnsibleFilterError) as cm:
                merge_with_app(*args)
            self.assertEqual(
                cm.exception.message, "input apps definitions should be 'dict' types"
            )

    def test_submitted_apps_have_name_key(self):
        """Submitted apps should have a ``name`` key"""

        for args in (({"name": "foo"}, {}), ({}, {"name": "foo"})):
            with self.assertRaises(AnsibleFilterError) as cm:
                merge_with_app(*args)
            self.assertEqual(
                cm.exception.message, "input apps should have a 'name' key"
            )

    def test_submitted_apps_same_name_key(self):
        """Submitted apps should have the same ``name`` key"""

        # pylint: disable=bad-continuation
        for args in (
            ({"name": "foo"}, {"name": "bar"}),
            ({"name": "foo"}, {"name": ""}),
            ({"name": ""}, {"name": "bar"}),
        ):
            with self.assertRaises(AnsibleFilterError) as cm:
                merge_with_app(*args)
            self.assertEqual(
                cm.exception.message, "input apps should have the same name"
            )

    def test_submitted_apps_name_is_not_empty(self):
        """Submitted apps should have a non-empty ``name`` key"""

        with self.assertRaises(AnsibleFilterError) as cm:
            merge_with_app({"name": ""}, {"name": ""})
        self.assertEqual(cm.exception.message, "input apps name cannot be empty")

    def test_services_merge_with_empty_new_services(self):
        """
            Test app services merge with no services or volumes for the new
            app
        """

        base = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml"],
                },
                {
                    "name": "baz",
                    "configs": ["baz.conf"],
                    "templates": ["baz/dc.yml", "baz/svc.yml", "baz/ep.yml"],
                },
            ],
            "volumes": ["volumes/foo_bar.yml", "volumes/foo_baz.yml"],
        }

        new = {"name": "foo", "services": []}

        self.assertDictDeepEqual(merge_with_app(base, new), base)

    def test_services_merge_without_duplicates(self):
        """
            Test app services merge does not create duplicates if same items
            appear in base and new apps
        """

        base = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml"],
                },
                {
                    "name": "baz",
                    "configs": ["baz.conf"],
                    "templates": ["baz/dc.yml", "baz/svc.yml", "baz/ep.yml"],
                },
            ],
            "volumes": ["volumes/foo_bar.yml", "volumes/foo_baz.yml"],
        }

        self.assertDictDeepEqual(merge_with_app(base, base), base)

    def test_services_merge(self):
        """Test app services merge"""

        base = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml"],
                },
                {
                    "name": "baz",
                    "configs": ["baz.conf"],
                    "templates": ["baz/dc.yml", "baz/svc.yml", "baz/ep.yml"],
                },
            ],
            "volumes": ["volumes/foo_bar.yml", "volumes/foo_baz.yml"],
        }

        # As the "fun" service does not exist in the "base" app services, we
        # expect that it won't be copied, but simply ignored.
        new = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar2.conf"],
                    "templates": ["bar/dc.yml", "bar/ep.yml"],
                },
                {
                    "name": "fun",
                    "configs": ["fun.conf"],
                    "templates": ["fun/dc.yml", "fun/svc.yml"],
                },
            ],
            "volumes": ["volumes/foo_fun.yml"],
        }

        expected = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf", "bar2.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml", "bar/ep.yml"],
                },
                {
                    "name": "baz",
                    "configs": ["baz.conf"],
                    "templates": ["baz/dc.yml", "baz/svc.yml", "baz/ep.yml"],
                },
            ],
            "volumes": [
                "volumes/foo_bar.yml",
                "volumes/foo_baz.yml",
                "volumes/foo_fun.yml",
            ],
        }

        self.assertDictDeepEqual(merge_with_app(base, new), expected)

    def test_services_merge_with_no_config(self):
        """Test app services merge"""

        base = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml"],
                }
            ],
            "volumes": ["volumes/foo_bar.yml", "volumes/foo_baz.yml"],
        }

        new = {
            "name": "foo",
            "services": [{"name": "bar", "templates": ["bar/dc.yml", "bar/ep.yml"]}],
        }

        expected = {
            "name": "foo",
            "services": [
                {
                    "name": "bar",
                    "configs": ["bar.conf"],
                    "templates": ["bar/dc.yml", "bar/svc.yml", "bar/ep.yml"],
                }
            ],
            "volumes": ["volumes/foo_bar.yml", "volumes/foo_baz.yml"],
        }

        self.assertDictDeepEqual(merge_with_app(base, new), expected)
