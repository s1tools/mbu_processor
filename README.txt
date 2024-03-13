About MBU
---------

MBU is a tool used to convert Sentinel-1 Level 2 products (OCN) of wave mode acquisitions (WV) into BUFR format.

Sentinel-1 WV OCN products are composed of series of NetCDF files (one NetCDF file for each Wave Mode imagette).

The tool convert every NetCDF file into one BUFR file.


Usage
-----

MBU is designed to be operated as an "ESA processor" and thus complies with the ESA Generic IPF ICD.

MBU provides Task Tables defining expected inputs and outputs types.

Those Tasks Tables have to be considered by a Management Layer (not provided here) so as to generate Job Orders.

The Job Orders are the real inputs of MBU.

Roadmap
-------

Some elements of planned evolutions of the tool are presented in [roadmap.md](roadmap.md).

Documentation
-------------

Extended documentation of the MBU processor are provided in the doc directory.


License
-------

Distributed under the MIT License. See LICENSE.txt for more information.

Contributing
------------

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!


- Fork the Project
- Create your Feature Branch (git checkout -b feature/AmazingFeature)
- Commit your Changes (git commit -m 'Add some AmazingFeature')
- Push to the Branch (git push origin feature/AmazingFeature)
- Open a Pull Request
