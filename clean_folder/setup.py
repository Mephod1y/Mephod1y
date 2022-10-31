from setuptools import setup, find_packages

setup(
      name='clean_folder',
      version='1.0',
      description='Code for sort folder',
      author='Mephodiy',
      license='MIT',
      packages=find_packages(),
      entry_points={
            'console_scripts': ['clean_folder = clean_folder.clean:clean'],
},
)
