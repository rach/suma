import os
import sys
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class ToxCommand(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

here = os.path.abspath(os.path.dirname(__file__))

short_desc = (
    "Application to generate short URL's, manage external links and extract "
    "link info (eg: title, screenshot, content) "
)


install_requires = [
    'alembic==0.8.4',
    'pyramid==1.5.7',
    'pyramid-tm==0.12',
    'pyramid-services==0.3',
    'pyramid-exclog==0.7',
    'zope.sqlalchemy==0.7.6',
    'Sqlalchemy==1.0.10',
    'pyramid_storage==0.0.8',
    'schematics==1.1.0',
    'structlog==15.1.0',
    'hashids==1.1.0',
    'psycopg2==2.6.1',
    'filedepot==0.2.1',
    'goose-extractor==1.0.25',
    'celery[redis]==3.1.18',
    'requests==2.8.1',
    'selenium==2.47.1'
]

s3_require = [
    'boto',
]

tests_require = [
    'tox',
    'pytest-cov'
    'pytest',
]


develop_requires = [
    'waitress',
    'pyramid_debugtoolbar',
    'tox',
    'pytest-cov', # before pytest, more info why. See bug #196 in setuptools 
    'pytest',
    'Paste==2.0.2',
    'bumpversion',
    'alembic==0.7.7',
]


dependency_links = [
]


setup(
    name='suma',
    version='0.1.0',
    description=short_desc,
    long_description=open('description.rst').read() + '\n\n' + open('CHANGES.txt').read(),
    cmdclass={'test': ToxCommand, },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Rachid Belaid',
    author_email='rachid.belaid@gmail.com',
    url='https://github.com/rach/suma',
    keywords='shorturl screenshot',
    packages=find_packages(),
    dependency_links=dependency_links,
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'dev': develop_requires,
        'test': tests_require,
        's3': s3_require
    },
    entry_points="""\
    [console_scripts]
        initialize_suma_db = suma.core.scripts.initializedb:main
    [paste.app_factory]
        api = suma.api:main
        web = suma.web:main
    """
)
