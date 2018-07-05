# coding=utf-8
# pylint: disable=I0011,E0401,C0103,C0111,W0212
# https://github.com/octplane/ansible_stdout_compact_logger


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
from datetime import datetime

try:
    from ansible.utils.color import colorize, hostcolor
    from ansible.plugins.callback import CallbackBase
except ImportError:
    class CallbackBase:
        # pylint: disable=I0011,R0903
        pass

import unittest

# Fields we would like to see before the others, in this order, please...
PREFERED_FIELDS = ['stdout', 'rc', 'stderr', 'start', 'end', 'msg']
# Fields we will delete from the result
DELETABLE_FIELDS = [
    'stdout', 'stdout_lines', 'rc', 'stderr', 'start', 'end', 'msg',
    '_ansible_verbose_always', '_ansible_no_log']

CHANGED = 'yellow'
UNCHANGED = 'green'


def deep_serialize(data, indent=0):
    # pylint: disable=I0011,E0602,R0912,W0631

    padding = " " * indent * 2
    if isinstance(data, list):
        if data == []:
            return "[]"
        output = "[ "
        if len(data) == 1:
            output = output + \
                ("\n" +
                 padding).join(deep_serialize(data[0], 0).splitlines()) + " ]"
        else:
            list_padding = " " * (indent + 1) * 2

            for item in data:
                output = output + "\n" + list_padding + "- " + \
                    deep_serialize(item, indent)
            output = output + "\n" + padding + " ]"
    elif isinstance(data, dict):
        if "_ansible_no_log" in data and data["_ansible_no_log"]:
            data = {"censored":
                    "the output has been hidden due to the fact that"
                    " 'no_log: true' was specified for this result"}
        list_padding = " " * (indent + 1) * 2
        output = "{\n"

        for key in PREFERED_FIELDS:
            if key in data.keys():
                value = data[key]
                prefix = list_padding + "- %s: " % key
                output = output + prefix + "%s\n" % \
                    "\n".join([" " * len(prefix) + line
                               for line in deep_serialize(value, indent)
                               .splitlines()]).strip()

        for key in DELETABLE_FIELDS:
            if key in data.keys():
                del data[key]

        for key, value in data.items():
            output = output + list_padding + \
                "- %s: %s\n" % (key, deep_serialize(value, indent + 1))

        output = output + padding + "}"
    else:
        string_form = "%s" % data
        if len(string_form) == 0:
            return "\"\""
        else:
            return string_form
    return output


class TestStringMethods(unittest.TestCase):

    test_structure = {
        u'cmd': [u'false'], u'end': u'2016-12-29 16:46:04.151591',
        '_ansible_no_log': False, u'stdout': u'', u'changed': True, 'failed': True,
        u'delta': u'0:00:00.005046', u'stderr': u'', u'rc': 1, 'invocation':
            {'module_name': u'command',
             u'module_args': {
                 u'creates': None, u'executable': None, u'chdir': None,
                 u'_raw_params': u'false', u'removes': None,
                 u'warn': True, u'_uses_shell': False}},
        'stdout_lines': [], u'start': u'2016-12-29 16:46:04.146545', u'warnings': []}

    def test_single_item_array(self):
        self.assertEqual(
            deep_serialize(self.test_structure['cmd']),
            "[ false ]")

    def test_single_empty_item_array(self):
        self.assertEqual(
            deep_serialize([""]),
            "[ \"\" ]")

    def test_issue_4(self):
        self.assertEqual(
            deep_serialize(["ÉLÉGANT"]),
            "[ ÉLÉGANT ]")

    def test_empty_array(self):
        self.assertEqual(
            deep_serialize(self.test_structure['stdout_lines']),
            "[]")

    def test_simple_hash(self):
        hs = {"cmd": "toto", "ret": 12}
        expected_result = "{\n  - cmd: toto\n  - ret: 12\n}"
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_hash_array(self):
        hs = {u'cmd': [u'false']}
        expected_result = "{\n  - cmd: [ false ]\n}"
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_hash_array2(self):
        hs = {u'cmd': ['one', 'two']}
        expected_result = """{
  - cmd: [
    - one
    - two
   ]
}"""
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_favorite_hash(self):
        hs = {"cmd": "toto", "rc": 12}
        expected_result = "{\n  - rc: 12\n  - cmd: toto\n}"
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_nested(self):
        hs = {u'cmd': {'bar': ['one', 'two']}}
        expected_result = """{
  - cmd: {
    - bar: [
      - one
      - two
     ]
  }
}"""
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_multiline_single(self):
        # pylint: disable=I0011,C0303
        hs = [["foo", "bar"]]
        expected_result = """[ [
  - foo
  - bar
 ] ]"""
        # print(deep_serialize(hs))
        # print(expected_result)
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_empty_array_no_padding(self):
        hs = [[{"foo": []}]]
        expected_result = """[ [ {
  - foo: []
} ] ]"""
        # print(deep_serialize(hs))
        # print(expected_result)
        self.assertEqual(deep_serialize(hs), expected_result)

    def test_hidden_fields(self):
        hs = {"_ansible_verbose_always": True}
        expected_result = """{
}"""
        # print(deep_serialize(hs))
        # print(expected_result)
        self.assertEqual(deep_serialize(hs), expected_result)


class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'anstomlog'

    def _get_duration(self):
        end = datetime.now()
        total_duration = (end - self.tark_started)
        duration = total_duration.microseconds / \
            1000 + total_duration.total_seconds() * 1000
        return duration

    def _command_generic_msg(self, hostname, result, caption):
        duration = self._get_duration()

        stdout = result.get('stdout', '')
        if self._display.verbosity > 0:
            if 'stderr' in result and result['stderr']:
                stderr = result.get('stderr', '')
                return "%s | %s | %sms | rc=%s | stdout: \n%s\n\n\t\t\t\tstderr: %s" % \
                    (hostname, caption, duration,
                     result.get('rc', 0), stdout, stderr)
            else:
                if len(stdout) > 0:
                    return "%s | %s | %sms | rc=%s | stdout: \n%s\n" % \
                        (hostname, caption, duration, result.get('rc', 0), stdout)
                else:
                    return "%s | %s | %sms | rc=%s | no stdout" % \
                        (hostname, caption, duration, result.get('rc', 0))
        else:
            return "%s | %s | %sms | rc=%s" % (hostname, caption, duration, result.get('rc', 0))

    def v2_playbook_on_task_start(self, task, is_conditional):
        # pylint: disable=I0011,W0613
        self._open_section(task.get_name())
        self._task_level += 1

    def _open_section(self, section_name):
        # pylint: disable=I0011,W0201
        self.tark_started = datetime.now()

        prefix = ''
        if self._task_level > 0:
            prefix = '  ➥'

        self.task_start_preamble = "[{}]{} {} ...".format(
            self.tark_started.strftime(
                "%H:%M:%S"), prefix.encode('utf-8'), section_name).encode("utf8")
        sys.stdout.write(self.task_start_preamble)

    def v2_playbook_on_handler_task_start(self, task):
        self._emit_line("triggering handler | %s " % task.get_name().strip())

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # pylint: disable=I0011,W0613,W0201
        duration = self._get_duration()
        host_string = self._host_string(result)
        self._task_level = 0

        if 'exception' in result._result:
            exception_message = "An exception occurred during task execution."
            if self._display.verbosity < 3:
                # extract just the actual error message from the exception text
                error = result._result['exception'].strip().split('\n')[-1]
                msg = exception_message + \
                    "To see the full traceback, use -vvv. The error was: %s" % error
            else:
                msg = exception_message + \
                    "The full traceback is:\n" + \
                    result._result['exception'].replace('\n', '')

                self._emit_line(msg, color='red')

        self._emit_line("%s | FAILED | %dms" %
                        (host_string,
                         duration), color='red')
        self._emit_line(deep_serialize(result._result), color='cyan')

    def v2_on_file_diff(self, result):

        if result._task.loop and 'results' in result._result:
            for res in result._result['results']:
                if 'diff' in res and res['diff'] and res.get('changed', False):
                    diff = self._get_diff(res['diff'])
                    if diff:
                        self._emit_line(diff)

        elif 'diff' in result._result and \
                result._result['diff'] and \
                result._result.get('changed', False):
            diff = self._get_diff(result._result['diff'])
            if diff:
                self._emit_line(diff)

    def _host_string(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)

        if delegated_vars:
            host_string = "%s -> %s" % (
                result._host.get_name(), delegated_vars['ansible_host'])
        else:
            host_string = result._host.get_name()

        return host_string

    def v2_runner_on_ok(self, result):
        # pylint: disable=I0011,W0201,
        duration = self._get_duration()

        self._clean_results(result._result, result._task.action)

        host_string = self._host_string(result)

        self._clean_results(result._result, result._task.action)

        if result._task.action in ('include', 'include_role'):
            sys.stdout.write("\b\b\b\b    \n")
            return

        self._task_level = 0
        msg, color = self._changed_or_not(result._result, host_string)

        if result._task.loop and self._display.verbosity > 0 and 'results' in result._result:
            for item in result._result['results']:
                msg, color = self._changed_or_not(item, host_string)
                item_msg = "%s - item=%s" % (msg, self._get_item(item))
                self._emit_line("%s | %dms" %
                                (item_msg, duration), color=color)
        else:
            self._emit_line("%s | %dms" %
                            (msg, duration), color=color)
        self._handle_warnings(result._result)

        if (
            self._display.verbosity > 0 or
            '_ansible_verbose_always' in result._result
        ) and not '_ansible_verbose_override' in result._result:
            self._emit_line(deep_serialize(result._result), color=color)

        result._preamble = self.task_start_preamble

    def _changed_or_not(self, result, host_string):
        if result.get('changed', False):
            msg = "%s | CHANGED" % host_string
            color = CHANGED
        else:
            msg = "%s | SUCCESS" % host_string
            color = UNCHANGED

        return [msg, color]

    def _emit_line(self, lines, color='normal'):

        if self.task_start_preamble is None:
            self._open_section("system")

        if self.task_start_preamble.endswith(" ..."):
            sys.stdout.write("\b\b\b\b | ")
            self.task_start_preamble = " "

        for line in lines.splitlines():
            self._display.display(line, color=color)

    def v2_runner_on_unreachable(self, result):
        self._task_level = 0
        self._emit_line("%s | UNREACHABLE!: %s" %
                        (self._host_string(result), result._result.get('msg', '')), color=CHANGED)

    def v2_runner_on_skipped(self, result):
        duration = self._get_duration()
        self._task_level = 0

        self._emit_line("%s | SKIPPED | %dms" %
                        (self._host_string(result), duration), color='cyan')

    def v2_playbook_on_include(self, included_file):
        self._open_section("system")

        msg = 'included: %s for %s' % \
            (included_file._filename, ", ".join(
                [h.name for h in included_file._hosts]))
        self._emit_line(msg, color='cyan')

    def v2_playbook_on_stats(self, stats):
        self._open_section("system")
        self._emit_line("-- Play recap --")

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)

            self._emit_line(u"%s : %s %s %s %s" % (
                hostcolor(h, t),
                colorize(u'ok', t['ok'], UNCHANGED),
                colorize(u'changed', t['changed'], CHANGED),
                colorize(u'unreachable', t['unreachable'], CHANGED),
                colorize(u'failed', t['failures'], 'red')))

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self._task_level = 0
        reload(sys).setdefaultencoding('utf8')


if __name__ == '__main__':
    unittest.main()
