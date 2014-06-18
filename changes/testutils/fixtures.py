from __future__ import absolute_import

__all__ = ('Fixtures', 'SAMPLE_COVERAGE', 'SAMPLE_DIFF', 'SAMPLE_XUNIT')

from uuid import uuid4

from changes.config import db
from changes.models import (
    Repository, Job, JobPlan, Project, Revision, Change, Author,
    Patch, Plan, Step, Build, Source, Node, JobPhase, JobStep, Task,
    Artifact, TestCase, LogChunk, LogSource, Cluster, ClusterNode
)
from changes.utils.slugs import slugify


SAMPLE_COVERAGE = """<?xml version="1.0" ?>
<!DOCTYPE coverage
  SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-03.dtd'>
<coverage branch-rate="0" line-rate="0.4483" timestamp="1375818307337" version="3.6">
    <!-- Generated by coverage.py: http://nedbatchelder.com/code/coverage -->
    <packages>
        <package branch-rate="0" complexity="0" line-rate="0.4483" name="">
            <classes>
                <class branch-rate="0" complexity="0" filename="setup.py" line-rate="0" name="setup">
                    <methods/>
                    <lines>
                        <line hits="0" number="2"/>
                        <line hits="0" number="12"/>
                        <line hits="1" number="13"/>
                        <line hits="1" number="14"/>
                        <line hits="0" number="16"/>
                    </lines>
                </class>
                <class branch-rate="0" complexity="0" filename="src/pytest_phabricator/plugin.py" line-rate="0.1875" name="src/pytest_phabricator/plugin">
                    <methods/>
                    <lines>
                        <line hits="1" number="1"/>
                        <line hits="1" number="2"/>
                        <line hits="1" number="3"/>
                        <line hits="0" number="7"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>"""

with open('sample.diff', 'r') as f:
    SAMPLE_DIFF = f.read()

SAMPLE_XUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="1" failures="0" name="" skips="0" tests="0" time="0.077">
    <testcase classname="" name="tests.test_report" time="0">
        <failure message="collection failure">tests/test_report.py:1: in &lt;module&gt;
&gt;   import mock
E   ImportError: No module named mock</failure>
    </testcase>
    <testcase classname="tests.test_report.ParseTestResultsTest" name="test_simple" time="0.00165796279907" rerun="1"/>
</testsuite>"""

LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed facilisis ligula ut ante ultrices, quis posuere eros tristique. Phasellus auctor imperdiet ligula quis gravida. Duis id gravida libero. Praesent non justo quis felis elementum volutpat at in neque. Sed eget consectetur lorem. Donec condimentum condimentum volutpat. Vestibulum lobortis enim augue, quis egestas libero dictum eu.

Vivamus a erat eu nibh pharetra rhoncus sit amet at lacus. Proin ullamcorper quis enim at feugiat. Suspendisse sit amet luctus elit. Nunc quis aliquet massa, sed imperdiet est. In urna orci, consectetur a auctor eget, dapibus at turpis. Aliquam facilisis mi id nunc auctor, id convallis odio fermentum. Nunc mollis felis nec orci mattis, ut mollis elit imperdiet.

Mauris eget elit aliquet, mattis augue dignissim, fermentum orci. Ut vestibulum viverra cursus. Duis libero justo, dapibus vel tincidunt in, laoreet et nulla. Maecenas cursus diam id gravida sollicitudin. Nullam varius nunc purus, nec bibendum sem mattis ac. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla et ullamcorper nibh. Duis convallis erat erat, a egestas leo consectetur vel. Vivamus fermentum placerat ipsum, a vulputate risus lacinia eu. Donec iaculis orci non neque mattis lacinia.

Duis id volutpat leo. Quisque turpis erat, scelerisque nec nibh eu, elementum interdum ipsum. Proin viverra leo eget nisl scelerisque, a euismod urna eleifend. Sed vel luctus arcu. Phasellus eros ligula, rutrum cursus egestas ut, consequat id ante. In hac habitasse platea dictumst. Nullam venenatis ut risus a elementum. Donec hendrerit massa risus, a ultricies orci mollis ut. Fusce eget orci magna. Pellentesque pharetra faucibus dolor, ac porttitor nulla elementum in. Ut posuere, nibh ut consectetur tincidunt, libero turpis rutrum enim, sit amet volutpat mauris dui sit amet mi. In consequat dictum vehicula.

Morbi dictum justo nec auctor lacinia. Vestibulum scelerisque vitae nisi quis faucibus. Nunc facilisis nibh sit amet porttitor varius. Nulla rhoncus, orci at venenatis faucibus, mauris nisl mattis odio, ut vulputate arcu magna et orci. Duis in sodales tellus. Nam feugiat quis enim ac dictum. Sed in tortor enim. Curabitur nibh leo, pulvinar ac vestibulum at, lobortis vel dui. Aenean a ante in dolor lacinia tristique facilisis eget massa. Duis in erat vitae tortor lacinia auctor. Quisque sit amet sem nec justo sagittis viverra.
"""

_lorem_paragraphs = tuple(filter(bool, LOREM_IPSUM.splitlines()))
_lorem_sentences = [s.strip() for s in LOREM_IPSUM.split('. ') if s.strip()]


def get_paragraphs(number):
    return _lorem_paragraphs[:number]


def get_sentences(number):
    return _lorem_sentences[:number]


class Fixtures(object):
    def create_repo(self, **kwargs):
        kwargs.setdefault('url', 'http://example.com/{0}'.format(uuid4().hex))

        repo = Repository(**kwargs)
        db.session.add(repo)
        db.session.commit()

        return repo

    def create_node(self, cluster=None, **kwargs):
        kwargs.setdefault('label', uuid4().hex)

        node = Node(**kwargs)
        db.session.add(node)

        if cluster:
            db.session.add(ClusterNode(cluster=cluster, node=node))

        db.session.commit()

        return node

    def create_cluster(self, **kwargs):
        kwargs.setdefault('label', uuid4().hex)

        cluster = Cluster(**kwargs)
        db.session.add(cluster)
        db.session.commit()

        return cluster

    def create_project(self, **kwargs):
        if not kwargs.get('repository'):
            kwargs['repository'] = self.create_repo()
        kwargs['repository_id'] = kwargs['repository'].id
        kwargs.setdefault('name', uuid4().hex)
        kwargs.setdefault('slug', kwargs['name'])

        project = Project(**kwargs)
        db.session.add(project)
        db.session.commit()

        return project

    def create_change(self, project, **kwargs):
        kwargs.setdefault('label', 'Sample')

        change = Change(
            hash=uuid4().hex,
            repository=project.repository,
            project=project,
            **kwargs
        )
        db.session.add(change)
        db.session.commit()

        return change

    def create_test(self, job, **kwargs):
        kwargs.setdefault('name', uuid4().hex)

        case = TestCase(
            job=job,
            project=job.project,
            project_id=job.project_id,
            job_id=job.id,
            **kwargs
        )
        db.session.add(case)
        db.session.commit()

        return case

    def create_job(self, build, **kwargs):
        project = build.project

        kwargs.setdefault('label', build.label)
        kwargs.setdefault('status', build.status)
        kwargs.setdefault('result', build.result)
        kwargs.setdefault('duration', build.duration)
        kwargs.setdefault('date_started', build.date_started)
        kwargs.setdefault('date_finished', build.date_finished)
        kwargs.setdefault('source', build.source)

        if kwargs.get('change', False) is False:
            kwargs['change'] = self.create_change(project)

        job = Job(
            build=build,
            build_id=build.id,
            project=project,
            project_id=project.id,
            **kwargs
        )
        db.session.add(job)
        db.session.commit()

        return job

    def create_job_plan(self, job, plan):
        job_plan = JobPlan(
            project_id=job.project_id,
            build_id=job.build_id,
            plan_id=plan.id,
            job_id=job.id,
        )
        db.session.add(job_plan)
        db.session.commit()

        return job_plan

    def create_source(self, project, **kwargs):
        if 'revision_sha' not in kwargs:
            revision = self.create_revision(repository=project.repository)
            kwargs['revision_sha'] = revision.sha

        source = Source(
            repository_id=project.repository_id,
            **kwargs
        )
        db.session.add(source)
        db.session.commit()

        return source

    def create_build(self, project, **kwargs):
        if 'source' not in kwargs:
            kwargs['source'] = self.create_source(project)

        kwargs['source_id'] = kwargs['source'].id

        kwargs.setdefault('label', 'Sample')

        build = Build(
            project_id=project.id,
            project=project,
            **kwargs
        )
        db.session.add(build)
        db.session.commit()

        return build

    def create_patch(self, project, **kwargs):
        kwargs.setdefault('diff', SAMPLE_DIFF)
        kwargs.setdefault('parent_revision_sha', uuid4().hex)
        if not kwargs.get('repository'):
            kwargs['repository'] = self.create_repo()
        kwargs['repository_id'] = kwargs['repository'].id

        patch = Patch(
            **kwargs
        )
        db.session.add(patch)
        db.session.commit()

        return patch

    def create_revision(self, **kwargs):
        kwargs.setdefault('sha', uuid4().hex)
        if not kwargs.get('repository'):
            kwargs['repository'] = self.create_repo()
        kwargs['repository_id'] = kwargs['repository'].id

        if not kwargs.get('author'):
            kwargs['author'] = self.create_author()
        kwargs['author_id'] = kwargs['author'].id

        if not kwargs.get('message'):
            message = get_sentences(1)[0][:128] + '\n'
            message += '\n\n'.join(get_paragraphs(2))
            kwargs['message'] = message

        revision = Revision(**kwargs)
        db.session.add(revision)
        db.session.commit()

        return revision

    def create_author(self, email=None, **kwargs):
        if not kwargs.get('name'):
            kwargs['name'] = ' '.join(get_sentences(1)[0].split(' ')[0:2])

        if not email:
            email = '{0}-{1}@example.com'.format(
                slugify(kwargs['name']), uuid4().hex)

        kwargs.setdefault('name', 'Test Case')

        author = Author(email=email, **kwargs)
        db.session.add(author)
        db.session.commit()

        return author

    def create_plan(self, **kwargs):
        kwargs.setdefault('label', 'test')

        plan = Plan(**kwargs)
        db.session.add(plan)
        db.session.commit()

        return plan

    def create_step(self, plan, **kwargs):
        kwargs.setdefault('implementation', 'changes.backends.buildstep.BuildStep')
        kwargs.setdefault('order', 0)

        step = Step(plan=plan, **kwargs)
        db.session.add(step)
        db.session.commit()

        return step

    def create_jobphase(self, job, **kwargs):
        kwargs.setdefault('label', 'test')
        kwargs.setdefault('result', job.result)
        kwargs.setdefault('status', job.status)

        phase = JobPhase(
            job=job,
            project=job.project,
            **kwargs
        )
        db.session.add(phase)
        db.session.commit()

        return phase

    def create_jobstep(self, phase, **kwargs):
        kwargs.setdefault('label', phase.label)
        kwargs.setdefault('result', phase.result)
        kwargs.setdefault('status', phase.status)

        step = JobStep(
            job=phase.job,
            project=phase.project,
            phase=phase,
            **kwargs
        )
        db.session.add(step)
        db.session.commit()

        return step

    def create_task(self, **kwargs):
        kwargs.setdefault('task_id', uuid4())

        task = Task(**kwargs)
        db.session.add(task)
        db.session.commit()

        return task

    def create_artifact(self, step, **kwargs):
        artifact = Artifact(
            step=step,
            project=step.project,
            job=step.job,
            **kwargs
        )
        db.session.add(artifact)
        db.session.commit()

        return artifact

    def create_logsource(self, step=None, **kwargs):
        if step:
            kwargs['job'] = step.job
        kwargs['project'] = kwargs['job'].project

        logsource = LogSource(
            step=step,
            **kwargs
        )
        db.session.add(logsource)
        db.session.commit()

        return logsource

    def create_logchunk(self, source, text=None, **kwargs):
        # TODO(dcramer): we should default offset to previosu entry in LogSource
        kwargs.setdefault('offset', 0)
        kwargs['job'] = source.job
        kwargs['project'] = source.project

        if text is None:
            text = '\n'.join(get_sentences(4))

        logchunk = LogChunk(
            source=source,
            text=text,
            size=len(text),
            **kwargs
        )
        db.session.add(logchunk)
        db.session.commit()

        return logchunk
