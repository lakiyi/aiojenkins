import contextlib
import pytest

from aiojenkins.exceptions import (
    JenkinsError,
    JenkinsNotFoundError,
)

from tests import jenkins


TEST_CONFIG_XML = """<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>arg</name>
          <description></description>
          <defaultValue></defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command></command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
"""

TEST_JOB_NAME = 'test'


@pytest.mark.asyncio
async def test_delete_job():
    try:
        await jenkins.jobs.delete(TEST_JOB_NAME)
    except JenkinsNotFoundError:
        ...


@pytest.mark.asyncio
async def test_create_job():
    await jenkins.jobs.create(TEST_JOB_NAME, TEST_CONFIG_XML)


@pytest.mark.asyncio
async def test_get_job_config():
    await jenkins.jobs.get_config(TEST_JOB_NAME)


@pytest.mark.asyncio
async def test_disable_job():
    await jenkins.jobs.disable(TEST_JOB_NAME)


@pytest.mark.asyncio
async def test_disable_unavailable_job():
    with pytest.raises(JenkinsNotFoundError):
        await jenkins.jobs.disable('unavailable')


@pytest.mark.asyncio
async def test_enable_job():
    await jenkins.jobs.enable(TEST_JOB_NAME)


@pytest.mark.asyncio
async def test_get_job_info():
    info = await jenkins.jobs.get_info(TEST_JOB_NAME)
    assert isinstance(info, dict)


@pytest.mark.asyncio
async def test_copy_job():
    job_name_old = test_copy_job.__name__
    job_name_new = job_name_old + '_new'

    with contextlib.suppress(JenkinsError):
        await jenkins.jobs.delete(job_name_old)
        await jenkins.jobs.delete(job_name_new)

    await jenkins.jobs.create(job_name_old, TEST_CONFIG_XML)
    available_jobs = await jenkins.jobs.get_all()
    assert job_name_old in available_jobs

    await jenkins.jobs.copy(job_name_old, job_name_new)
    available_jobs = await jenkins.jobs.get_all()

    assert job_name_new in available_jobs
    assert job_name_old in available_jobs

    await jenkins.jobs.delete(job_name_old)
    await jenkins.jobs.delete(job_name_new)


@pytest.mark.asyncio
async def test_rename_job():
    job_name_old = test_rename_job.__name__
    job_name_new = job_name_old + '_new'

    with contextlib.suppress(JenkinsError):
        await jenkins.jobs.delete(job_name_old)
        await jenkins.jobs.delete(job_name_new)

    await jenkins.jobs.create(job_name_old, TEST_CONFIG_XML)
    available_jobs = await jenkins.jobs.get_all()
    assert job_name_old in available_jobs

    await jenkins.jobs.rename(job_name_old, job_name_new)
    available_jobs = await jenkins.jobs.get_all()

    assert job_name_new in available_jobs
    assert job_name_old not in available_jobs

    await jenkins.jobs.delete(job_name_new)