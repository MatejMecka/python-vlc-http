from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='python-vlc-http',
    version='0.0.2',
    description='Python module that enables communication with the VLC http server ',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Matej Plavevski',
    author_email='matej.plavevski+github@gmail.com',
    keywords=['VLC', 'HttpServer'],
    url='https://github.com/matejmecka/python-vlc-http',
    download_url='https://pypi.org/project/python-vlc-http/',
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
  ],
)

install_requires = [
    'requests',
    'xmltodict'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
