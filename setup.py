from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='python-vlc-http',
    version='0.0.1',
    description='Python module that enables communication with the VLC http server ',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Matej Plavevski',
    author_email='matej.plavevski+github@gmail.com',
    keywords=['VLC', 'HttpServer'],
    url='https://github.com/matejmecka/python-vlc-http',
    download_url='https://pypi.org/project/python-vlc-http/'
)

install_requires = [
    'requets',
    'xmltodict'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
