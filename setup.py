from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in snrg_cartons/__init__.py
from snrg_cartons import __version__ as version

setup(
	name="snrg_cartons",
	version=version,
	description="Carton Management System",
	author="SNRG Electricals",
	author_email="admin@snrgelectricals.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
