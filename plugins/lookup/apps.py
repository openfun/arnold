# -*- coding: utf-8 -*-
"""
Applications lookup
"""
# pylint: disable=bad-continuation
from __future__ import absolute_import, division, print_function

import os
import re

from ansible.plugins.lookup import LookupBase

# pylint: disable=invalid-name
__metaclass__ = type

DOCUMENTATION = """
    lookup: apps
    author: Open FUN (France Universite Numerique) <fun.dev(at)fun-mooc.fr>
    version_added: "0.1"
    short_description: walk through an application tree to discover deployable
        applications
    description:
        Lookup ready-to-deploy applications following recommended Arnold
        applications' tree, e.g. for the "richie" application and the
        "apps" ``apps_path``:

            apps/richie
                └── templates
                    ├── elasticsearch
                    │   ├── dc.yml.j2
                    │   └── svc.yml.j2
                    ├── nginx
                    │   ├── _configs
                    │   │   └── richie.conf.j2
                    │   ├── dc.yml.j2
                    │   └── svc.yml.j2
                    ├── postgresql
                    │   ├── dc.yml.j2
                    │   ├── ep.yml.j2
                    │   └── svc.yml.j2
                    ├── richie
                    │   ├── dc.yml.j2
                    │   ├── job_collectstatic.yml.j2
                    │   ├── job_db_migrate.yml.j2
                    │   ├── job_regenerate_indexes.yml.j2
                    │   └── svc.yml.j2
                    └── _volumes
                        ├── media.yml.j2
                        └── static.yml.j2

        Analysing this tree with ``lookup_apps`` should return the
        following data structure:

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
                            ]
                        },
                        {
                            "name": "postgresql",
                            "templates": [
                                "apps/richie/templates/postgresql/dc.yml.j2",
                                "apps/richie/templates/postgresql/ep.yml.j2",
                                "apps/richie/templates/postgresql/svc.yml.j2"
                            ]
                        },
                        {
                            "name": "elasticsearch",
                            "templates": [
                                "apps/richie/templates/elasticsearch/dc.yml.j2",
                                "apps/richie/templates/elasticsearch/svc.yml.j2"
                            ]
                        },
                        {
                            "name": "richie",
                            "templates": [
                                "apps/richie/templates/richie/job_regenerate_indexes.yml.j2",
                                "apps/richie/templates/richie/dc.yml.j2",
                                "apps/richie/templates/richie/route.yml.j2",
                                "apps/richie/templates/richie/job_collectstatic.yml.j2",
                                "apps/richie/templates/richie/svc.yml.j2",
                                "apps/richie/templates/richie/job_db_migrate.yml.j2"
                            ]
                        }
                    ],
                    "volumes": [
                        "apps/richie/templates/_volumes/static.yml.j2",
                        "apps/richie/templates/_volumes/media.yml.j2"
                    ]
                }
            ]
    options:
      _apps_paths:
        description: Paths to look for applications
        required: True
"""

EXAMPLES = """
- debug: msg="Available apps: {{ lookup('apps','apps') }}"
"""

RETURN = """
  _list:
    description:
      - Available applications
    type: list
"""


class LookupModule(LookupBase):
    """Apps lookup module"""

    # pylint: disable=arguments-differ, too-many-locals
    def run(self, apps_paths, variables, **kwargs):

        app_volumes_dir = "_volumes"
        service_config_dir = "_configs"
        apps = []
        app = None

        for apps_path in apps_paths:

            ignore_dirs_regex = r"^{}/_.*(/.*)*$".format(apps_path.strip("/"))

            for root, _, files in os.walk(apps_path):

                (head, tail) = os.path.split(root)

                # ./apps/
                if not tail:
                    continue

                # Ignore directories matching ignore_dirs_regex
                if re.match(ignore_dirs_regex, root):
                    continue

                # ./apps/foo app directory
                if root == os.path.join(apps_path, tail):
                    if app is not None:
                        apps.append(app)
                    app = {"name": tail, "services": []}
                    continue

                # ./apps/foo/_volumes directory
                if tail == app_volumes_dir:
                    volumes = [os.path.join(root, f) for f in files]
                    app["volumes"] = volumes
                    continue

                # ./apps/foo/templates/bar service templates
                if app is not None and root == os.path.join(
                    apps_path, app["name"], "templates", tail
                ):
                    templates = [os.path.join(root, f) for f in files]
                    app["services"].append({"name": tail, "templates": templates})
                    continue

                # ./apps/foo/templates/bar/_configs directory
                if tail == service_config_dir:
                    service = os.path.basename(head)
                    idx = [s.get("name") for s in app["services"]].index(service)
                    configs = [os.path.join(root, f) for f in files]
                    app["services"][idx].update({"configs": configs})
                    continue

            apps.append(app)

        return apps
