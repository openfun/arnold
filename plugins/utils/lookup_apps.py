# -*- coding: utf-8 -*-
"""
Lookup the "apps" directory to generate apps configuration
"""
import os
import re

from ansible.plugins.filter.core import to_nice_yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
APPS_DIRECTORY = os.path.join(PROJECT_ROOT, "apps")
IGNORE_DIRS_REGEX = "^{}/_.*(/.*)*$".format(APPS_DIRECTORY)
APP_VOLUMES_DIR = "_volumes"
SERVICE_CONFIG_DIR = "_configs"


def lookup_apps(apps_path):
    """
    Lookup ready-to-deploy applications following recommended Arnold applications'
    tree, e.g. for the "richie" application and the "apps" ``apps_path``:

        apps/richie
        ├── templates
        │   ├── elasticsearch
        │   │   ├── dc.yml.j2
        │   │   └── svc.yml.j2
        │   ├── nginx
        │   │   ├── _configs
        │   │   │   └── richie.conf.j2
        │   │   ├── dc.yml.j2
        │   │   └── svc.yml.j2
        │   ├── postgresql
        │   │   ├── dc.yml.j2
        │   │   ├── ep.yml.j2
        │   │   └── svc.yml.j2
        │   ├── richie
        │   │   ├── dc.yml.j2
        │   │   ├── job_collectstatic.yml.j2
        │   │   ├── job_db_migrate.yml.j2
        │   │   ├── job_regenerate_indexes.yml.j2
        │   │   ├── route.yml.j2
        │   │   └── svc.yml.j2
        │   └── _volumes
        │       ├── media.yml.j2
        │       └── static.yml.j2
        └── vars
            └── main.yml

    Analysing this tree with ``lookup_apps`` should return the following data structure:

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
    """
    apps = []
    app = None

    for root, _, files in os.walk(apps_path):

        (head, tail) = os.path.split(root)

        # Ignore directories matching IGNORE_DIRS_REGEX
        if re.match(IGNORE_DIRS_REGEX, root):
            continue

        # ./apps/foo app directory
        if root == os.path.join(apps_path, tail):
            if app is not None:
                apps.append(app)
            app = {"name": tail, "services": []}
            continue

        # ./apps/foo/_volumes directory
        if tail == APP_VOLUMES_DIR:
            volumes = [
                os.path.relpath(os.path.join(root, f), PROJECT_ROOT) for f in files
            ]
            app["volumes"] = volumes
            continue

        # ./apps/foo/templates/bar service templates
        if (
            app is not None
            and root == os.path.join(apps_path, app["name"], "templates", tail)
        ):
            templates = [
                os.path.relpath(os.path.join(root, f), PROJECT_ROOT) for f in files
            ]
            app["services"].append({"name": tail, "templates": templates})
            continue

        # ./apps/foo/templates/bar/_configs directory
        if tail == SERVICE_CONFIG_DIR:
            service = os.path.basename(head)
            idx = map(lambda s: s.get("name"), app["services"]).index(service)
            configs = [
                os.path.relpath(os.path.join(root, f), PROJECT_ROOT) for f in files
            ]
            app["services"][idx].update({"configs": configs})
            continue

    apps.append(app)

    return apps


def main():
    """
    Once we looked up applications and services, pretty print collected data in
    YAML format.
    """
    apps = lookup_apps(APPS_DIRECTORY)
    print(to_nice_yaml(apps, indent=2))


if __name__ == "__main__":
    main()
