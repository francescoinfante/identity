from setuptools import setup, find_packages

setup(
    name='identity',
    url='https://github.com/francescoinfante/identity',
    author='Francesco Infante',
    author_email='francesco.infante@icloud.com',
    version='0.1.2',
    packages=find_packages(),
    long_description=open('README.md').read(),
    license='GNU Lesser General Public License v3 (LGPLv3)',
    install_requires=['dpath', 'ujson', 'unidecode'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    ])
