from __future__ import absolute_import

import mock

from flask import current_app

from changes.models.jobplan import JobPlan
from changes.testutils import TestCase


class AutogeneratedJobTest(TestCase):
    @mock.patch('changes.models.project.Project.get_config')
    def test_autogenerated_commands(self, get_config):
        get_config.return_value = {
            'bazel.targets': [
                '//aa/bb/cc/...',
                '//aa/abc/...',
            ],
        }

        current_app.config['APT_SPEC'] = 'deb http://example.com/debian distribution component1'

        project = self.create_project()
        build = self.create_build(project)
        job = self.create_job(build, autogenerated=True)

        _, implementation = JobPlan.get_build_step_for_job(job.id)

        expected = """#!/bin/bash -eu
echo "deb http://example.com/debian distribution component1" | sudo tee /etc/apt/sources.list.d/bazel-changes-autogen.list > /dev/null 2>&1
(sudo apt-get update || true) > /dev/null 2>&1
sudo apt-get install -y --force-yes bazel drte-v1 gcc unzip zip python > /dev/null 2>&1
(bazel query 'tests(//aa/bb/cc/... + //aa/abc/...)' | python -c "import sys
import json


targets = sys.stdin.read().splitlines()
out = {
    'cmd': 'bazel test {test_names}',
    'tests': targets,
}
json.dump(out, sys.stdout)
") 2> /dev/null
""".strip()

        assert len(implementation.commands) == 2
        assert implementation.commands[1].script == expected
