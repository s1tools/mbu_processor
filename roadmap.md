This version of MBU processor is considering the master tables version 27.
This version 27 does not support the full set of tables required, and is then using local tables defined as version 4.

ecc.codes_set(self.bufr, 'masterTablesVersionNumber', 27)
ecc.codes_set(self.bufr, 'localTablesVersionNumber', 4)

An update of master tables to include the required tables was submitted to WMO and approved.
Once the corresponding master tables will be available, MBU processor will be updated accordingly to use master tables version 40 (to be confirmed) and no local tables (then version 0).
