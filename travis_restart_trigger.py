# -*- coding: utf-8 -*-
"""
Simple script to trigger restart of travis build
"""
import logging
import time
import click
from travispy import TravisPy

DEV_LOGGER = logging.getLogger(__name__)


def get_last_build(github_token, repository_slug):
    '''
    Get last build
    '''
    t = TravisPy.github_auth(github_token)
    DEV_LOGGER.info('Logged in')
    r = t.repo(repository_slug)
    DEV_LOGGER.info('Got repo %r', r)
    return r.last_build


def get_build(github_token, build_id):
    '''
    Get build by id
    '''
    t = TravisPy.github_auth(github_token)
    DEV_LOGGER.info('Logged in')
    build = t.build(build_id)
    DEV_LOGGER.info('Got build %r', build)
    return build


@click.command()
@click.argument('repository_slug')
@click.option('--github-token', envvar='GITHUB_TOKEN')
def run(repository_slug, github_token):
    '''
    Start a travis build and wait for it to finish
    '''
    logging.basicConfig()
    DEV_LOGGER.setLevel(logging.INFO)
    last_build = get_last_build(github_token, repository_slug)
    DEV_LOGGER.info('Last build was %r', last_build)
    last_build_at = last_build.finished_at
    last_build_id = last_build.id

    assert last_build.restart()
    DEV_LOGGER.info('Restarted last build')

    while True:
        build_status = get_build(github_token, last_build_id)
        DEV_LOGGER.info(
            'Build status of %r state=%r finished_at=%r',
            last_build_id,
            build_status.state,
            build_status.finished_at)
        if build_status.finished_at != last_build_at and build_status.finished:
            break
        time.sleep(5)
