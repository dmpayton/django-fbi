#!/usr/bin/env python

import os
from django_fbi import __version__, __description__
from setuptools import setup, find_packages

## Package detection from django-registration

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('django_fbi'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[11:] # Strip "django_fbi/" or "django_fbi\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='django-fbi',
    version=__version__,
    description=__description__,
    long_description=__description__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django facebook',
    maintainer = 'Derek Payton',
    maintainer_email = 'derek@cukerinteractive.com',
    url='http://github.com/dmpayton/django-fbi',
    license='MIT License',
    packages=packages,
    package_data={'django_fbi': data_files},
    package_dir={'django_fbi': 'django_fbi'},
    zip_safe=False,
    )
