from setuptools import setup, find_packages

setup(name="PACKAGENAME", 
package_dir={"": "src"},
packages=find_packages(where="src")
)

# setuptools.setup(
#     package_dir={"": "src"},
#     packages=setuptools.find_packages(where="src"),
#     python_requires=">=3.6",
# )

