import setuptools

setuptools.setup(
    name="tracker-database",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary'
    ]
)
