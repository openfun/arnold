"""
Deploy Jinja filters
"""
from ansible.errors import AnsibleFilterError

BLUE_GREEN_PREFIXES = ["previous", "current", "next"]


def blue_green_host(host, prefix=None):
    """
        Add next/previous prefix to the base host, if prefix is empty or equals
        to 'current', the host is left unchanged.

        Example usage:

            {{ "foo.bar.com" | blue_green_host("previous") }}
            # Should return: previous.foo.bar.com

            {{ "foo.bar.com" | blue_green_host() }}
            # Should return: foo.bar.com

            {{ "foo.bar.com" | blue_green_host("current") }}
            # Should return: foo.bar.com
    """

    if prefix is None or not prefix:
        return host

    if prefix not in BLUE_GREEN_PREFIXES:
        raise AnsibleFilterError(
            "prefix '{}' is not allowed (must be in {})".format(
                prefix, BLUE_GREEN_PREFIXES
            )
        )

    return "{}.{}".format(prefix, host) if prefix != "current" else host


def blue_green_hosts(host):
    """
        Add next/current/previous prefix to the base host, and return that list
        of possible hosts.

        Example usage:

            {{ "foo.bar.com" | blue_green_hosts }}
            # Should return: previous.foo.bar.com, foo.bar.com, next.foo.bar.com
    """

    if not host:
        raise AnsibleFilterError("host cannot be empty")

    return ",".join(
        [
            "{}.{}".format(prefix, host) if prefix != "current" else host
            for prefix in BLUE_GREEN_PREFIXES
        ]
    )


# pylint: disable=no-self-use,too-few-public-methods
class FilterModule():
    """Filters used for deployments"""

    def filters(self):
        """List plugin filters"""

        return {
            "blue_green_host": blue_green_host,
            "blue_green_hosts": blue_green_hosts,
        }
