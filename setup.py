from setuptools import setup

setup(
    name='Grades',
    version='0.1.0',
    py_modules=['grades', 'grades'],
    install_requires=[
        'click',
        'mechanicalsoup'
    ],
    entry_points='''
        [console_scripts]
        grades=src.main:main
    '''
)
