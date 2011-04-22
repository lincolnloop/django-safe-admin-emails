import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-safe-admin-emails",
    version = "0.1",
    author = "Brian Luft",
    author_email = "brian@lincolnloop.com",
    description = "Provides support for making sure sensitive information "
                    "does not appear in admin emails.",
    license = "MIT",
    keywords = "Django admin emails mail_admins logging security",
    packages=['admin_emails'],
    url='http://github.com/lincolnloop/django-safe-admin-emails',
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
