"""
Merge Jinja filters
"""

from copy import deepcopy

from ansible.errors import AnsibleFilterError


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

    if not len(base["name"]):
        raise AnsibleFilterError("input apps name cannot be empty")

    result = deepcopy(base)

    # Add or override services metadata
    for base_service in result["services"]:
        new_app_selected_services = [
            s for s in new["services"] if s.get("name") == base_service.get("name")
        ]

        if len(new_app_selected_services) != 1:
            continue
        new_service = new_app_selected_services[0]
        for k in ("configs", "templates"):
            if not new_service.get(k):
                continue
            # Use the list(set()) trick to remove duplicated items
            base_service[k] = sorted(list(set(new_service[k] + base_service[k])))

    # Merge volumes (if any)
    if result.get("volumes") and new.get("volumes"):
        # Use the list(set()) trick to remove duplicated items
        result["volumes"] = sorted(list(set(new["volumes"] + result["volumes"])))

    return result


class FilterModule(object):
    """Filters used to deep merge python objects"""

    def filters(self):
        return {"merge_with_app": merge_with_app}
