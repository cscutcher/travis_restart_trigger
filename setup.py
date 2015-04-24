# -*- coding: utf-8 -*-
"""
Travis restart triggering script
"""
import logging
from setuptools import setup

DEV_LOGGER = logging.getLogger(__name__)


setup(
    name='travis_restart_trigger',
    version='0.1',
    py_modules='travis_restart_trigger',
    install_requires=('click', 'travispy'),
    entry_points={
        'console_scripts': [
            'travis_restart_trigger = travis_restart_trigger:run',
        ]
    }

)
