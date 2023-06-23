from setuptools import find_packages, setup
from typing import List

k = '-e .'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        # if k in requirements:
        #     requirements.remove(k)
        return requirements

setup(
    name='DiamondPricePrediction',
    version='0.0.1',
    author='ChandniJha',
    author_email='chandnijha630@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)
