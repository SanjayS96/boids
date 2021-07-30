from setuptools import setup, find_packages

setup(name="boidspkg", 
packages=find_packages(where='src'),
# packages=['resources'],
package_dir={"": "src"},
# package_dir={"resources": "src/resources"},
# package_data={"resources": ["data_pk/*.dat"]},
include_package_data=True,
install_requires=['numpy', 'scipy'],
)



