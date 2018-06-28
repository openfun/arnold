"""
Merge Jinja filters
"""

from copy import deepcopy

from ansible.errors import AnsibleFilterError
from deepmerge import always_merger


def merge_with_app(base, new):
    """Merge data from the "new" application to the "base" application"""

    if not isinstance(base, dict) or not isinstance(new, dict):
        raise AnsibleFilterError("input apps definitions should be 'dict' types")

    if base.get("name") is None or new.get("name") is None:
        raise AnsibleFilterError("input apps should have a name key")

    if base["name"] != new["name"]:
        raise AnsibleFilterError("input apps should have the same name")

    result = deepcopy(base)

    # Add or override services metadata
    for service in result["services"]:
        new_app_selected_services = filter(
            lambda s: s.get("name") == service.get("name"), new["services"]
        )
        if len(new_app_selected_services) != 1:
            continue
        service = always_merger.merge(service, new_app_selected_services[0])

    # Merge volumes (if any)
    if result.get("volumes") and new.get("volumes"):
        result["volumes"] = always_merger.merge(result["volumes"], new["volumes"])

    return result


class FilterModule(object):
    """Filters used to deep merge python objects"""

    def filters(self):
        return {"merge_with_app": merge_with_app}
