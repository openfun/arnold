"""
Merge Jinja filters
"""

from copy import deepcopy

from ansible.errors import AnsibleFilterError
from ansible.utils.encrypt import random_password


# pylint: disable=invalid-name,too-many-branches
def merge_with_app(base, new):
    """
        Merge data from the "new" application to the "base" application.
        Services listed in "new" that do not exist in "base" will be ignored.
    """

    if base is None:
        raise AnsibleFilterError("input base app is empty")

    if new is None:
        raise AnsibleFilterError("input new app is empty")

    if not isinstance(base, dict) or not isinstance(new, dict):
        raise AnsibleFilterError("input apps definitions should be 'dict' types")

    if base.get("name") is None or new.get("name") is None:
        raise AnsibleFilterError("input apps should have a 'name' key")

    if base["name"] != new["name"]:
        raise AnsibleFilterError("input apps should have the same name")

    if not base["name"]:
        raise AnsibleFilterError("input apps name cannot be empty")

    result = deepcopy(base)

    if "services" not in new:
        return result

    # Add or override services metadata
    for base_service in result["services"]:
        new_app_selected_services = [
            s for s in new["services"] if s.get("name") == base_service.get("name")
        ]

        if len(new_app_selected_services) != 1:
            continue
        new_service = new_app_selected_services[0]
        for k in ("configs", "templates"):
            if new_service.get(k) is None:
                continue
            # Use the list(set()) trick to remove duplicated items
            base_service[k] = sorted(list(set(new_service[k] + base_service[k])))

        # Add service missing keys (could be meta, such as host, etc.)
        for k, v in new_service.iteritems():
            if base_service.get(k) is None:
                base_service[k] = v

    # Merge volumes (if any)
    if result.get("volumes") and new.get("volumes"):
        # Use the list(set()) trick to remove duplicated items
        result["volumes"] = sorted(list(set(new["volumes"] + result["volumes"])))

    # Add new keys for this app
    for k, v in new.iteritems():
        if k not in result:
            result[k] = v

    return result


def merge_with_database(base, database, app_name, customer, environment):
    """
        Merge a database information with a database structure already existent.
        If database already exist the new one is ignored.
    """

    if not isinstance(base, dict) or not isinstance(database, dict):
        raise AnsibleFilterError("input database is empty")

    if "engine" not in database:
        raise AnsibleFilterError("input database should define an 'engine' key")

    if "release" not in database:
        raise AnsibleFilterError("input database should define a 'release' key")

    result = deepcopy(base)

    database_name = "_".join([environment[0], customer, app_name])
    new_database = {
        "application": app_name,
        "password": random_password(),
        "name": database_name,
        "user": database_name,
    }

    engine = database.get("engine")

    if engine not in result:
        # Create a new entry for this database engine
        result[database.get("engine")] = [
            {"release": database.get("release"), "databases": [new_database]}
        ]

        return result

    # Loop over defined engines and look for existing releases
    for defined_engine in result[engine]:
        if defined_engine.get("release", None) == database.get("release"):
            # Target release already exists
            for defined_database in defined_engine.get("databases"):
                if defined_database.get("application") == app_name:
                    # Target database already exist: abort
                    break
            else:
                # Add a new entry for targeted database engine and release
                defined_engine.get("databases").append(new_database)
        else:
            # Add a new release and database for targeted database engine
            result[engine].append(
                {"release": database.get("release"), "databases": [new_database]}
            )

    return result


# pylint: disable=no-self-use,too-few-public-methods
class FilterModule(object):
    """Filters used to deep merge python objects"""

    def filters(self):
        """List plugin filters"""

        return {
            "merge_with_app": merge_with_app,
            "merge_with_database": merge_with_database,
        }
