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
        'Operating System :: Microsoft :: Windows',
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
        'vuecli.provider',
        'vue',
        'vue.bridge',
        'vue.decorators'
    ],
    install_requires=[
        'brython==3.8.9',
        'Jinja2~=2.10',
        'pyyaml~=5.1',
    ],
    extra_requires={
        "flask": 'Flask~=1.0',
    },
    package_data={
        'vuecli': ['js/*.js', 'js/LICENSE_*', "index.html", "loading.gif"]
    },
    entry_points={
        'console_scripts': ['vue-cli=vuecli.cli:main'],
        'vuecli.provider': [
            "static=vuecli.provider.static:Static",
            "flask=vuecli.provider.flask:Flask",
        ]
    },
    zip_safe=False
)
