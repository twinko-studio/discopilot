from setuptools import setup, find_packages

setup(
    name='discopilot',
    version='0.1.0',
    description='Using discord bots to automate RSS feed processing, translation, summarization and publishing to other services such as twitter, weibo etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tengfei Yin',
    author_email='tengfei@twinko.studio',
    url='https://github.com/twinko-studio/discopilot',
    packages=find_packages(exclude=['tests*', 'docs']),
    python_requires='>=3.8',  # Your supported Python versions
)