# -*- coding: utf-8 -*-
"""
Applications lookup
"""
from __future__ import absolute_import, division, print_function

from pathlib import Path

import yaml
from ansible.plugins.lookup import LookupBase

# pylint: disable=invalid-name
__metaclass__ = type

DOCUMENTATION = """
    lookup: apps
    author: Open FUN (France Universite Numerique) <fun.dev(at)fun-mooc.fr>
    version_added: "0.1"
    short_description: walk through an application tree to discover deployable
        applications
    description: >
        Lookup ready-to-deploy applications following recommended Arnold
        applications' tree, e.g. for the "richie" application and the
        "apps" ``apps_path``::

            apps/richie
            ├── templates
            │   ├── services
            │   │   ├── app
            │   │   │   ├── *.yml.j2
            │   │   ├── elasticsearch
            │   │   │   └── *.yml.j2
            │   │   ├── nginx
            │   │   │   ├── configs
            │   │   │   │   └── richie.conf.j2
            │   │   │   └── *.yml.j2
            │   │   └── postgresql
            │   │       └── *.yml.j2
            │   └── volumes
            │       ├── media.yml.j2
            │       └── static.yml.j2
            ├── tray.yml
            └── vars
                ├── all
                │   └── main.yml
                ├── settings.yml
                └── vault
                    └── main.yml.j2


        Analysing this tree with the ``apps`` lookup should return the
        following data structure:

        .. code-block:: json

            [
                {
                    "name": "richie",
                    "services": [
                        {
                            "configs": [
                                "apps/richie/templates/nginx/_configs/richie.conf.j2"
                            ],
                            "name": "nginx",
                            "templates": [
                                "apps/richie/templates/nginx/dc.yml.j2",
                                "apps/richie/templates/nginx/svc.yml.j2"
                            ],
                            "environment_variables": None
                        },
                        {
                            "configs": [],
                            "name": "postgresql",
                            "templates": [
                                "apps/richie/templates/postgresql/dc.yml.j2",
                                "apps/richie/templates/postgresql/ep.yml.j2",
                                "apps/richie/templates/postgresql/svc.yml.j2"
                            ],
                            "environment_variables": None
                        },
                        {
                            "configs": [],
                            "name": "elasticsearch",
                            "templates": [
                                "apps/richie/templates/elasticsearch/dc.yml.j2",
                                "apps/richie/templates/elasticsearch/svc.yml.j2"
                            ],
                            "environment_variables": None
                        },
                        {
                            "configs": [],
                            "name": "richie",
                            "templates": [
                                "apps/richie/templates/richie/job_regenerate_indexes.yml.j2",
                                "apps/richie/templates/richie/dc.yml.j2",
                                "apps/richie/templates/richie/route.yml.j2",
                                "apps/richie/templates/richie/job_collectstatic.yml.j2",
                                "apps/richie/templates/richie/svc.yml.j2",
                                "apps/richie/templates/richie/job_db_migrate.yml.j2"
                            ],
                            "environment_variables": None
                        }
                    ],
                    "volumes": [
                        "apps/richie/templates/_volumes/static.yml.j2",
                        "apps/richie/templates/_volumes/media.yml.j2"
                    ],
                    vars: [
                        {
                            "type": "all",
                            "name": "main",
                            "path": "apps/richie/vars/all/main.yml",
                        },
                    ],
                    settings: {
                        "databases": [
                            "engine": "postgresql",
                            "release": "9.6"
                        ]
                    }
                }
            ]
    options:
      _terms:
        description: list of application paths to look for
        required: True
"""

EXAMPLES = """
- debug: msg="Available apps: {{ lookup('apps', apps_path) }}"
"""

RETURN = """
  _list:
    description:
      - Available applications
    type: list
"""


# pylint: disable=too-many-instance-attributes
class LookupModule(LookupBase):
    """Apps lookup module"""

    def __init__(self, loader=None, templar=None, **kwargs):
        """Add application related properties."""
        super().__init__(loader=None, templar=None, **kwargs)

        self.configs_dir = "configs"
        self.services_dir = "services"
        self.templates_dir = "templates"
        self.vars_dir = "vars"
        self.volumes_dir = "volumes"
        self.env_file = "_env.yml.j2"
        self.settings_file = "settings.yml"
        self.tray_file = "tray.yml"
        # For now we only accept "all" type vars, but this can evolve soon.
        self.var_types = ("all",)
        self.apps = []

    @staticmethod
    def _yaml_load(file_path):
        """Syntactic sugar to get yaml content with a simpler line of code"""

        return yaml.load(Path(file_path).read_text(), Loader=yaml.FullLoader)

    def _get_app_service(self, service_path):
        """Explore an application service"""

        p = Path(service_path)

        # Expected environment variables for this service
        env_vars = p / self.env_file
        return {
            "name": p.name,
            "templates": sorted(map(str, p.glob("[!_]*.yml.j2"))),
            "configs": sorted(map(str, (p / self.configs_dir).glob("*.j2"))),
            "environment_variables": str(env_vars) if env_vars.exists() else None,
        }

    def _get_app_services(self, app_path):
        """Explore an application services"""

        services = []
        for service_path in (
            Path(app_path) / self.templates_dir / self.services_dir
        ).iterdir():
            # Each directory store templates for a service
            if not service_path.is_dir():
                continue
            services.append(self._get_app_service(service_path))
        return services

    def _get_app_settings(self, app_path):
        """Explore application settings"""

        settings_path = Path(app_path) / self.vars_dir / self.settings_file
        if not settings_path.exists():
            return {}
        return self._yaml_load(settings_path)

    def _get_app_vars(self, app_path):
        """Get application variables"""

        _vars = []
        for var_type in self.var_types:
            for var_file in (Path(app_path) / self.vars_dir / var_type).glob("*.yml"):
                _vars.append(
                    {"type": var_type, "name": var_file.stem, "path": str(var_file)}
                )
        return _vars

    def _get_app_volumes(self, app_path):
        """Get application volumes"""

        return sorted(
            map(
                str,
                (Path(app_path) / self.templates_dir / self.volumes_dir).glob(
                    "*.yml.j2"
                ),
            )
        )

    # pylint: disable=inconsistent-return-statements
    def _get_app(self, app_path):
        """Explore an application path and add it to apps if it's a valid app"""

        tray_file = Path(app_path) / self.tray_file
        # Application is not a valid tray, ignore it
        if not tray_file.exists():
            return
        # Parse the tray file
        tray = self._yaml_load(tray_file)

        return {
            "name": tray.get("metadata").get("name"),
            "services": self._get_app_services(app_path),
            "vars": self._get_app_vars(app_path),
            "volumes": self._get_app_volumes(app_path),
            "settings": self._get_app_settings(app_path),
        }

    def _get_apps(self, apps_path):
        """Explore an application path and return discovered apps list."""

        apps = []
        for app_path in Path(apps_path).iterdir():
            if not app_path.is_dir():
                continue
            apps.append(self._get_app(app_path))
        return apps

    def run(self, terms, variables=None, **kwargs):
        """This is the lookup plugin entry point that will be invoked"""

        for term in terms:
            for apps_path in term:
                self.apps += self._get_apps(apps_path)

        return self.apps
