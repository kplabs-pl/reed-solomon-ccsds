import os
import setuptools

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='reed_solomon_ccsds',
    url='https://github.com/kplabs-pl/reed-solomon-ccsds',
    author='OBC Team',
    author_email='obc@kplabs.pl',
    license='LGPL 2.1',
    keywords='Reed Solomon CCSDS',
    description='Reed Solomon CCSDS (255, 223)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    use_scm_version={
        'root': '.',
        'relative_to': __file__
    },
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3'
    ],
    packages=['reed_solomon_ccsds'],
    include_package_data=True,
    setup_requires=['setuptools-scm'],
    install_requires=['numpy>=1.17.4'],
    extras_require={
        'dev': ['yapf'],
        'tests': ['flake8', 'mypy', 'pytest']
    }
)
