"""
Tests for the "apps" plugin lookup
"""

import unittest

from pyfakefs.fake_filesystem_unittest import \
    TestCaseMixin as fakefsTestCaseMixin

from lookup_plugins.apps import LookupModule as AppsLookupModule


# pylint: disable=protected-access
class TestAppsLookup(unittest.TestCase, fakefsTestCaseMixin):
    """Tests for the ``apps`` lookup"""

    def create_fake_app_tree(self):
        """Create a fake application tree"""

        app_files = (
            # Learning locker
            ("apps/learninglocker/templates/services/app/dc_api.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/_dc_base.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/dc_ui.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/dc_worker.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/_env.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/job_storage.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/secret.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/svc_api.yml.j2", ""),
            ("apps/learninglocker/templates/services/app/svc_ui.yml.j2", ""),
            ("apps/learninglocker/templates/services/mongodb/dc.yml.j2", ""),
            ("apps/learninglocker/templates/services/mongodb/ep.yml.j2", ""),
            ("apps/learninglocker/templates/services/mongodb/secret.yml.j2", ""),
            ("apps/learninglocker/templates/services/mongodb/svc.yml.j2", ""),
            (
                "apps/learninglocker/templates/services/nginx/configs/default.conf.j2",
                "",
            ),
            ("apps/learninglocker/templates/services/nginx/dc.yml.j2", ""),
            ("apps/learninglocker/templates/services/nginx/route.yml.j2", ""),
            ("apps/learninglocker/templates/services/nginx/svc.yml.j2", ""),
            ("apps/learninglocker/templates/services/xapi/dc.yml.j2", ""),
            ("apps/learninglocker/templates/services/xapi/_env.yml.j2", ""),
            ("apps/learninglocker/templates/services/xapi/secret.yml.j2", ""),
            ("apps/learninglocker/templates/services/xapi/svc.yml.j2", ""),
            ("apps/learninglocker/templates/volumes/storage.yml.j2", ""),
            (
                "apps/learninglocker/tray.yml",
                "metadata:\n  name: learninglocker\n  version: v2.6.2\n",
            ),
            ("apps/learninglocker/vars/all/main.yml", ""),
            (
                "apps/learninglocker/vars/settings.yml",
                (
                    "is_blue_green_compatible: False\n"
                    "databases:\n"
                    '  - engine: "mongodb"\n'
                    '    release: "3.2"\n'
                ),
            ),
            ("apps/learninglocker/vars/vault/main.yml.j2", ""),
        )
        for file_path, file_content in app_files:
            self.fs.create_file(file_path, contents=file_content)

    def setUp(self):
        """Setup PyfakefS"""

        self.setUpPyfakefs()
        self.create_fake_app_tree()

    def test_yaml_load(self):
        """Test the _yaml.load method"""

        file_path = "foo.yml"
        contents = "foo:\n  bar: baz\n"
        self.fs.create_file(file_path, contents=contents)

        expected = {"foo": {"bar": "baz"}}
        self.assertEqual(AppsLookupModule._yaml_load(file_path), expected)

    def test_get_app_service_without_envs_and_configs(self):
        """Test the _get_app_service method for a service without specific
        environment or configuration.
        """

        lkp = AppsLookupModule()
        service_path = "apps/learninglocker/templates/services/mongodb"

        expected = {
            "name": "mongodb",
            "templates": [
                "apps/learninglocker/templates/services/mongodb/dc.yml.j2",
                "apps/learninglocker/templates/services/mongodb/ep.yml.j2",
                "apps/learninglocker/templates/services/mongodb/secret.yml.j2",
                "apps/learninglocker/templates/services/mongodb/svc.yml.j2",
            ],
            "configs": [],
            "environment_variables": None,
        }
        self.assertEqual(lkp._get_app_service(service_path), expected)

    def test_get_app_service_with_envs_and_no_configs(self):
        """Test the _get_app_service method for a service with a specific
        environment but no configuration.
        """

        lkp = AppsLookupModule()
        service_path = "apps/learninglocker/templates/services/xapi"

        expected = {
            "name": "xapi",
            "templates": [
                "apps/learninglocker/templates/services/xapi/dc.yml.j2",
                "apps/learninglocker/templates/services/xapi/secret.yml.j2",
                "apps/learninglocker/templates/services/xapi/svc.yml.j2",
            ],
            "configs": [],
            "environment_variables": "apps/learninglocker/templates/services/xapi/_env.yml.j2",
        }
        self.assertEqual(lkp._get_app_service(service_path), expected)

    def test_get_app_service_without_envs_but_configs(self):
        """Test the _get_app_service method for a service with no specific
        environment but a configuration.
        """

        lkp = AppsLookupModule()
        service_path = "apps/learninglocker/templates/services/nginx"

        expected = {
            "name": "nginx",
            "templates": [
                "apps/learninglocker/templates/services/nginx/dc.yml.j2",
                "apps/learninglocker/templates/services/nginx/route.yml.j2",
                "apps/learninglocker/templates/services/nginx/svc.yml.j2",
            ],
            "configs": [
                "apps/learninglocker/templates/services/nginx/configs/default.conf.j2"
            ],
            "environment_variables": None,
        }
        self.assertEqual(lkp._get_app_service(service_path), expected)

    def test_get_app_service_ignore_hidden_templates(self):
        """Test the _get_app_service method ignore templates files who's
        name starts with and underscore.
        """

        lkp = AppsLookupModule()
        service_path = "apps/learninglocker/templates/services/app"

        expected = {
            "name": "app",
            "templates": [
                "apps/learninglocker/templates/services/app/dc_api.yml.j2",
                "apps/learninglocker/templates/services/app/dc_ui.yml.j2",
                "apps/learninglocker/templates/services/app/dc_worker.yml.j2",
                "apps/learninglocker/templates/services/app/job_storage.yml.j2",
                "apps/learninglocker/templates/services/app/secret.yml.j2",
                "apps/learninglocker/templates/services/app/svc_api.yml.j2",
                "apps/learninglocker/templates/services/app/svc_ui.yml.j2",
            ],
            "configs": [],
            "environment_variables": "apps/learninglocker/templates/services/app/_env.yml.j2",
        }
        self.assertEqual(lkp._get_app_service(service_path), expected)

    def test_get_app_services(self):
        """Test the _get_app_services"""

        lkp = AppsLookupModule()
        app_path = "apps/learninglocker"

        expected = [
            {
                "name": "app",
                "templates": [
                    "apps/learninglocker/templates/services/app/dc_api.yml.j2",
                    "apps/learninglocker/templates/services/app/dc_ui.yml.j2",
                    "apps/learninglocker/templates/services/app/dc_worker.yml.j2",
                    "apps/learninglocker/templates/services/app/job_storage.yml.j2",
                    "apps/learninglocker/templates/services/app/secret.yml.j2",
                    "apps/learninglocker/templates/services/app/svc_api.yml.j2",
                    "apps/learninglocker/templates/services/app/svc_ui.yml.j2",
                ],
                "configs": [],
                "environment_variables": "apps/learninglocker/templates/services/app/_env.yml.j2",
            },
            {
                "name": "mongodb",
                "templates": [
                    "apps/learninglocker/templates/services/mongodb/dc.yml.j2",
                    "apps/learninglocker/templates/services/mongodb/ep.yml.j2",
                    "apps/learninglocker/templates/services/mongodb/secret.yml.j2",
                    "apps/learninglocker/templates/services/mongodb/svc.yml.j2",
                ],
                "configs": [],
                "environment_variables": None,
            },
            {
                "name": "nginx",
                "templates": [
                    "apps/learninglocker/templates/services/nginx/dc.yml.j2",
                    "apps/learninglocker/templates/services/nginx/route.yml.j2",
                    "apps/learninglocker/templates/services/nginx/svc.yml.j2",
                ],
                "configs": [
                    "apps/learninglocker/templates/services/nginx/configs/default.conf.j2"
                ],
                "environment_variables": None,
            },
            {
                "name": "xapi",
                "templates": [
                    "apps/learninglocker/templates/services/xapi/dc.yml.j2",
                    "apps/learninglocker/templates/services/xapi/secret.yml.j2",
                    "apps/learninglocker/templates/services/xapi/svc.yml.j2",
                ],
                "configs": [],
                "environment_variables": "apps/learninglocker/templates/services/xapi/_env.yml.j2",
            },
        ]
        self.assertEqual(lkp._get_app_services(app_path), expected)

    def test_get_app_services_ignore_non_directories(self):
        """Test that the _get_app_services method only consider directories
        in service_dir as services.
        """

        self.fs.create_file("apps/foo/templates/services/foo")

        lkp = AppsLookupModule()
        app_path = "apps/foo"

        self.assertEqual(lkp._get_app_services(app_path), [])

    def test_get_app_settings(self):
        """Test the _get_app_settings method"""

        lkp = AppsLookupModule()
        app_path = "apps/learninglocker"

        expected = {
            "databases": [{"engine": "mongodb", "release": "3.2"}],
            "is_blue_green_compatible": False,
        }
        self.assertEqual(lkp._get_app_settings(app_path), expected)

    def test_get_app_settings_detects_missing_settings(self):
        """Test that the _get_app_settings method ignore missing app settings file"""

        lkp = AppsLookupModule()
        app_path = "apps/foo"

        expected = {}
        self.assertEqual(lkp._get_app_settings(app_path), expected)

    def test_get_app_vars(self):
        """Test the _get_app_vars method"""

        lkp = AppsLookupModule()
        app_path = "apps/learninglocker"

        expected = [
            {
                "type": "all",
                "name": "main",
                "path": "apps/learninglocker/vars/all/main.yml",
            }
        ]
        self.assertEqual(lkp._get_app_vars(app_path), expected)

    def test_get_app_volumes(self):
        """Test the _get_app_volumes method"""

        lkp = AppsLookupModule()
        app_path = "apps/learninglocker"

        expected = ["apps/learninglocker/templates/volumes/storage.yml.j2"]
        self.assertEqual(lkp._get_app_volumes(app_path), expected)

    def test_get_app(self):
        """Test the _get_app method"""

        lkp = AppsLookupModule()
        app_path = "apps/learninglocker"

        app = lkp._get_app(app_path)
        self.assertEqual(app.get("name"), "learninglocker")
        self.assertEqual(len(app.get("services")), 4)
        self.assertEqual(len(app.get("vars")), 1)
        self.assertEqual(len(app.get("volumes")), 1)
        self.assertEqual(len(app.get("settings")), 2)

    def test_get_app_without_tray_file(self):
        """Test the _get_app method for an app with no tray.yml file"""

        # Create a hello app with no tray.yml file
        app_files = (
            ("apps/hello/templates/services/app/dc.yml.j2", ""),
            ("apps/hello/templates/services/app/route.yml.j2", ""),
            ("apps/hello/templates/services/app/svc.yml.j2", ""),
            ("apps/hello/vars/all/main.yml", ""),
        )
        for file_path, file_content in app_files:
            self.fs.create_file(file_path, contents=file_content)

        lkp = AppsLookupModule()
        app_path = "apps/hello"

        app = lkp._get_app(app_path)
        self.assertEqual(app, None)

    def test_get_apps(self):
        """Test the _get_apps method"""

        # Create a supplementary hello app
        app_files = (
            ("apps/hello/templates/services/app/dc.yml.j2", ""),
            ("apps/hello/templates/services/app/route.yml.j2", ""),
            ("apps/hello/templates/services/app/svc.yml.j2", ""),
            ("apps/hello/tray.yml", "metadata:\n  name: hello\n  version: 1.0.0\n"),
            ("apps/hello/vars/all/main.yml", ""),
        )
        for file_path, file_content in app_files:
            self.fs.create_file(file_path, contents=file_content)

        lkp = AppsLookupModule()
        apps_path = "apps"

        apps = lkp._get_apps(apps_path)
        self.assertEqual(len(apps), 2)

    def test_get_apps_ignores_files_in_apps_directory(self):
        """Test the _get_apps method ignore standard files in the apps_directory"""

        # Create file to ignore
        self.fs.create_file("apps/foo")

        lkp = AppsLookupModule()
        apps_path = "apps"

        apps = lkp._get_apps(apps_path)
        self.assertEqual(len(apps), 1)

    def test_run(self):
        """Dummy test the run method"""

        lkp = AppsLookupModule()
        apps_path = "apps"

        apps = lkp.run([[apps_path]])
        self.assertEqual(len(apps), 1)
