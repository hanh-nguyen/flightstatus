from setuptools import setup, find_packages
setup(name='flightstatus',
      version='0.0.1',
      description='Predict flight delay and cancellation',
      author='Hanh Nguyen',
      author_email='myhanh.nguyen1211@gmail.com',
      packages=find_packages("dev"),
      package_dir={"": "dev"},
      install_requires=['pandas'])
