# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '3.1.0'

setup(name='Sentinel1_MBU_Processor',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3.9",
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Nuno Miranda (ESA), Manuel Goacolou (MPC-Team/CLS)',
      author_email='mgoacolou@groupcls.fr',
      url='http://www.cls.fr',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      package_data={'cls': ['maps'+'/*'*20, ]},
      include_package_data=True,
      zip_safe=False,
      # dependency_links = ["."],
      install_requires=['netCDF4',
                        'numpy',
                        ],
      entry_points={
          'console_scripts': [
              'MBUprocessor = mbu.converter_ocn_to_bufr:cmdline',
              'bufr_encode_sentinel1 = mbu.bufr_encode_sentinel1:cmdline',
          ]
      },
      )
