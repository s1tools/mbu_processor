/*
 * (C) Copyright 1996-2017 ECMWF.
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 * In applying this licence, ECMWF does not waive the privileges and immunities
 * granted to it by virtue of its status as an intergovernmental organisation nor
 * does it submit to any jurisdiction.
 */

#ifndef eccodes_ecbuild_config_h
#define eccodes_ecbuild_config_h

/* ecbuild info */

#ifndef ECBUILD_VERSION_STR
#define ECBUILD_VERSION_STR "2.6.0"
#endif
#ifndef ECBUILD_MACROS_DIR
#define ECBUILD_MACROS_DIR  "/usr/local/components/MBU-1.0/lib/eccodes/eccodes-2.1.0-Source/cmake"
#endif

/* cpu arch info */

/* #undef EC_BIG_ENDIAN */
#define EC_LITTLE_ENDIAN    1

/* compiler support */

/* #undef EC_HAVE_FUNCTION_DEF */

/* os capability checks */

/* --- symbols --- */

#define EC_HAVE_FSEEK
#define EC_HAVE_FSEEKO
#define EC_HAVE_FTELLO
/* #undef EC_HAVE_LSEEK */
/* #undef EC_HAVE_FTRUNCATE */
/* #undef EC_HAVE_OPEN */
#define EC_HAVE_FOPEN
#define EC_HAVE_FMEMOPEN
/* #undef EC_HAVE_FUNOPEN */
#define EC_HAVE_FLOCK
#define EC_HAVE_MMAP

#define EC_HAVE_POSIX_MEMALIGN

#define EC_HAVE_F_GETLK
#define EC_HAVE_F_SETLKW
#define EC_HAVE_F_SETLK

#define EC_HAVE_F_GETLK64
#define EC_HAVE_F_SETLKW64
#define EC_HAVE_F_SETLK64

#define EC_HAVE_MAP_ANONYMOUS
#define EC_HAVE_MAP_ANON

/* --- include files --- */

#define EC_HAVE_ASSERT_H
#define EC_HAVE_STDLIB_H
#define EC_HAVE_UNISTD_H
#define EC_HAVE_STRING_H
#define EC_HAVE_STRINGS_H
#define EC_HAVE_SYS_STAT_H
#define EC_HAVE_SYS_TIME_H
#define EC_HAVE_SYS_TYPES_H

#define EC_HAVE_MALLOC_H
/* #undef EC_HAVE_SYS_MALLOC_H */

#define EC_HAVE_SYS_PARAM_H
#define EC_HAVE_SYS_MOUNT_H
#define EC_HAVE_SYS_VFS_H

/* --- capabilities --- */

#define EC_HAVE_OFFT
#define EC_HAVE_OFF64T

#define EC_HAVE_STRUCT_STAT
#define EC_HAVE_STRUCT_STAT64
#define EC_HAVE_STAT
#define EC_HAVE_STAT64
#define EC_HAVE_FSTAT
#define EC_HAVE_FSTAT64

#define EC_HAVE_FSEEKO64
#define EC_HAVE_FTELLO64
#define EC_HAVE_LSEEK64
#define EC_HAVE_OPEN64
#define EC_HAVE_FOPEN64
#define EC_HAVE_FTRUNCATE64
#define EC_HAVE_FLOCK64
#define EC_HAVE_MMAP64

#define EC_HAVE_STRUCT_STATVFS
#define EC_HAVE_STRUCT_STATVFS64
/* #undef EC_HAVE_STATVFS */
/* #undef EC_HAVE_STATVFS64 */

#define EC_HAVE_FSYNC
#define EC_HAVE_FDATASYNC
#define EC_HAVE_DIRFD
/* #undef EC_HAVE_SYSPROC */
#define EC_HAVE_SYSPROCFS

#define EC_HAVE_EXECINFO_BACKTRACE

/* --- asynchronous IO support --- */

/* #undef EC_HAVE_AIOCB */
/* #undef EC_HAVE_AIO64CB */

/* --- reentrant funtions support --- */

#define EC_HAVE_GMTIME_R
#define EC_HAVE_GETPWUID_R
#define EC_HAVE_GETPWNAM_R
#define EC_HAVE_READDIR_R
#define EC_HAVE_GETHOSTBYNAME_R

/* --- compiler __attribute__ support --- */

#define EC_HAVE_ATTRIBUTE_CONSTRUCTOR
#define EC_ATTRIBUTE_CONSTRUCTOR_INITS_ARGV
#define EC_HAVE_PROCFS


/* --- dl library support --- */

#define EC_HAVE_DLFCN_H
#define EC_HAVE_DLADDR

/* --- c compiler support --- */

#define EC_HAVE_C_INLINE

/* --- c++ compiler support --- */

/* #undef EC_HAVE_FUNCTION_DEF */

/* #undef EC_HAVE_CXXABI_H */
/* #undef EC_HAVE_CXX_BOOL */

/* #undef EC_HAVE_CXX_SSTREAM */

/* config info */

#define ECCODES_OS_NAME          "Linux-2.6.32-642.el6.x86_64"
#define ECCODES_OS_BITS          64
#define ECCODES_OS_BITS_STR      "64"
#define ECCODES_OS_STR           "linux.64"
#define ECCODES_OS_VERSION       "2.6.32-642.el6.x86_64"
#define ECCODES_SYS_PROCESSOR    "x86_64"

#define ECCODES_BUILD_TIMESTAMP  "20180104164741"
#define ECCODES_BUILD_TYPE       "RelWithDebInfo"

#define ECCODES_C_COMPILER_ID      "GNU"
#define ECCODES_C_COMPILER_VERSION "4.4.7"

#define ECCODES_CXX_COMPILER_ID      ""
#define ECCODES_CXX_COMPILER_VERSION ""

#define ECCODES_C_COMPILER       "/usr/bin/cc"
#define ECCODES_C_FLAGS          " -pipe -O2 -g"

#define ECCODES_CXX_COMPILER     ""
#define ECCODES_CXX_FLAGS        ""

/* Needed for finding per package config files */

#define ECCODES_INSTALL_DIR       "/usr/local/components/MBU-1.0/lib/eccodes"
#define ECCODES_INSTALL_BIN_DIR   "/usr/local/components/MBU-1.0/lib/eccodes/bin"
#define ECCODES_INSTALL_LIB_DIR   "/usr/local/components/MBU-1.0/lib/eccodes/lib"
#define ECCODES_INSTALL_DATA_DIR  "/usr/local/components/MBU-1.0/lib/eccodes/share/eccodes"

#define ECCODES_DEVELOPER_SRC_DIR "/usr/local/components/MBU-1.0/lib/eccodes/eccodes-2.1.0-Source"
#define ECCODES_DEVELOPER_BIN_DIR "/usr/local/components/MBU-1.0/lib/eccodes/eccodes-2.1.0-Source/build"

#define EC_HAVE_FORTRAN

#ifdef EC_HAVE_FORTRAN

#define ECCODES_Fortran_COMPILER_ID      "GNU"
#define ECCODES_Fortran_COMPILER_VERSION ""

#define ECCODES_Fortran_COMPILER "/usr/bin/gfortran"
#define ECCODES_Fortran_FLAGS    " -O2 -g"

#endif

/* #undef BOOST_UNIT_TEST_FRAMEWORK_HEADER_ONLY */
/* #undef BOOST_UNIT_TEST_FRAMEWORK_LINKED */

#endif /* eccodes_ecbuild_config_h */
