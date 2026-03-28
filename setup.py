from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function return list of requirements
    """
    
    requirement_list:List[str]=[]
    
    try:
        with open('requirements.txt','r') as file:
            #read lines from the files
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
            
    except FileNotFoundError:
        pass
    return requirement_list
print(get_requirements())
setup(
    name="AI travel planner",
    version="0.0.1",
    author="Jatin",
    author_email="jatindev1022@gmail.com",
    install_requires=get_requirements()
)