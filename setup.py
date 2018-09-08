from setuptools import setup
from vue import __version__


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='vuepy',
    version=__version__,
    description='Pythonic Vue',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windws',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='web reactive gui framework',
    url='https://stefanhoelzl.github.io/vue.py/',
    author='Stefan Hoelzl',
    author_email='stefan.hoelzl@posteo.de',
    license='MIT',
    packages=[
        'vuecli',
        'vue',
        'vue.bridge',
        'vue.decorators'
    ],
    install_requires=[
        'Flask==1.0.2',
        'Jinja2==2.10',
        'pyyaml==3.13',
        'docopt==0.6.2',
    ],
    package_data={
        'vuecli': ['js/*.js', 'js/LICENSE_*', "index.html"]
    },
    entry_points={
        'console_scripts': ['vue-cli=vuecli.cli:main'],
    },
    zip_safe=False
)
