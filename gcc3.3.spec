%define name			%{cross_prefix}gcc%{package_suffix}
%define branch			3.3
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define version			3.3.6
%define release			 %mkrel 3
%define biarches		x86_64 ppc64

%define hammer_branch		1
%define hammer_date		20050117

# TODO: Provide fastjar, gccint, gcj info pages?
%define _unpackaged_files_terminate_build 0

# Define libraries major versions
%define libgcc_major		1
%define libstdcxx_major		5
%define libstdcxx_minor		7
%define libf2c_major		0
%define libgcj_major		4
%define libobjc_major		1
%define libgnat_major		1
%define libffi_major		2

# Package holding Java tools (gij, jv-convert, etc.)
%define GCJ_TOOLS		%{cross_prefix}gcj%{package_suffix}-tools

#-- JDK version
# "gcj" implements the JDK 1.1 language, "libgcj" is largely compatible with JDK 1.2
%define JDK_VERSION 1.2

#-- Alternatives for Java tools
#       Sun JDK         40
#       Kaffe           30
#       Gcj 3.2         20

%define gcj_alternative_priority 20
%define gcj_alternative_programs jar rmic rmiregistry grepjar java

# Define Mandrakelinux version we are building for
%define mdkversion		%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

# Define if building a cross compiler
# FIXME: assume user does not define both cross and cross_bootstrap variables
%define build_cross		0
%define build_cross_bootstrap	0
%{expand: %{?cross:		%%global build_cross 1}}
%{expand: %{?cross_bootstrap:	%%global build_cross_bootstrap 1}}

%if %{mdkversion} == 1000
%define system_compiler		1
%else
%define system_compiler		0
%endif
%define target_cpu		%{_target_cpu}
%if %{build_cross}
%define system_compiler		0
%define target_cpu		%{cross}
%endif
%if %{build_cross_bootstrap}
%define build_cross		1
%define system_compiler		0
%define target_cpu		%{cross_bootstrap}
%endif
%if %{system_compiler}
%define alternative_priority	30%{branch_tag}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{nil}
%define program_prefix		%{nil}
%define program_suffix		%{nil}
%else
%if %{build_cross}
%define alternative_priority	10%{branch_tag}
%define cross_prefix		cross-%{target_cpu}-
%define cross_program_prefix	%{target_cpu}-linux-
%define package_suffix		%{nil}
%define program_prefix		%{cross_program_prefix}
%define program_suffix		%{nil}
%else
%define alternative_priority	20%{branch_tag}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{branch}
%define program_prefix		%{nil}
%define program_suffix		-%{version}
%endif
%endif
%define _alternativesdir	/etc/alternatives
%if "%{package_suffix}" == "%{nil}"
%define _package_suffix		%{nil}
%else
%define _package_suffix		-%{package_suffix}
%endif

%define RELEASE			1
%if %{RELEASE}
%define source_package		gcc-%{version}
%define source_dir		gcc-%{version}
%else
%define snapshot		20040107
%define source_package		gcc-%{version}-%{snapshot}
%define source_dir		gcc-%{version}
%endif

# Define GCC target platform, and arch we built for
%if %{build_cross}
%define biarches		noarch
%define arch			%{target_cpu}
%define gcc_target_platform	%{target_cpu}-linux
%define target_prefix		%{_prefix}/%{gcc_target_platform}
%define target_libdir		%{target_prefix}/lib
%else
%define arch			%(echo %{_target_cpu}|sed -e "s/i.86/i386/" -e "s/athlon/i386/" -e "s/amd64/x86_64/")
%define gcc_target_platform	%{_target_platform}
%define target_prefix		%{_prefix}
%define target_libdir		%{_libdir}
%endif

# Location of Java headers, don't let them in compiler specific
# directory as they are grabbed first
%define libjava_includedir	%{target_prefix}/include/libgcj-%{version}

# We now have versioned libstdcxx_includedir, that is c++/<VERSION>/
%define libstdcxx_includedir	%{target_prefix}/include/c++/%{version}

%define color_gcc_version	1.3.2
%define build_minimal		0
%define build_doc		1
%define build_pdf_doc		1
%define build_check		1
%define build_ada		0
%define gpc_snapshot		20030507
%define build_pascal		0
%ifarch %{ix86} x86_64
%define build_pascal		1
%endif
%ifarch %{ix86} x86_64
%define build_ada		1
%endif
%define build_cxx		1
%define build_fortran		1
%define build_objc		1
%define build_java		1
%define build_colorgcc		1
%define build_libffi		1
%define build_debug		0
%if !%{system_compiler}
%if %{mdkversion} >= 200600
# some people like to do vintage business
%define build_fortran		1
%else
%define build_fortran		0
%endif
%define build_objc		0
%define build_pascal		0
%define build_ada		0
%define build_colorgcc		0
%define build_java		0
%define build_libffi		0
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_PDF:	%%global build_pdf_doc 0}}
%{expand: %{?_without_DEBUG:	%%global build_debug 0}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_without_MINIMAL:	%%global build_minimal 0}}
%{expand: %{?_with_PDF:		%%global build_pdf_doc 1}}
%{expand: %{?_with_DEBUG:	%%global build_debug 1}}
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_with_MINIMAL:	%%global build_minimal 1}}

# Allow --without <front-end> at rpm command line build
%{expand: %{?_with_CXX:		%%global build_cxx 1}}
%{expand: %{?_with_ADA:		%%global build_ada 1}}
%{expand: %{?_with_F77:		%%global build_fortran 1}}
%{expand: %{?_with_JAVA:	%%global build_java 1}}
%{expand: %{?_with_OBJC:	%%global build_objc 1}}
%{expand: %{?_with_PASCAL:	%%global build_pascal 1}}

# Allow --with <front-end> at rpm command line build
%{expand: %{?_without_CXX:	%%global build_cxx 0}}
%{expand: %{?_without_ADA:	%%global build_ada 0}}
%{expand: %{?_without_F77:	%%global build_fortran 0}}
%{expand: %{?_without_JAVA:	%%global build_java 0}}
%{expand: %{?_without_OBJC:	%%global build_objc 0}}
%{expand: %{?_without_PASCAL:	%%global build_pascal 0}}

# A minimal build overrides all other options
%if %{build_cross_bootstrap}
%define build_minimal		1
%endif
%if %{build_minimal}
%define build_doc		0
%define build_pdf_doc		0
%define build_check		0
%define build_ada		0
%define build_cxx		0
%define build_fortran		0
%define build_objc		0
%define build_java		0
%define build_pascal		0
%define build_colorgcc		0
%define build_debug		0
%endif
%if %{build_cross}
%define build_doc		0
%define build_pdf_doc		0
# Unsupported features when cross-compiling for now
%define build_check		0
%define build_colorgcc		0
%define build_pascal		0
%define build_java		0
%define build_ada		0
%endif

# Define library packages names
%define libgcc_name_orig	%{cross_prefix}libgcc
%define libgcc_name		%{libgcc_name_orig}%{libgcc_major}
%define libstdcxx_name_orig	%{cross_prefix}libstdc++
%define libstdcxx_name		%{libstdcxx_name_orig}%{libstdcxx_major}
%define libf2c_name_orig	%{cross_prefix}libf2c
%define libf2c_name		%{libf2c_name_orig}%{libf2c_major}
%define libgcj_name_orig	%{cross_prefix}libgcj
%define libgcj_name		%{libgcj_name_orig}%{libgcj_major}
%define libobjc_name_orig	%{cross_prefix}libobjc
%define libobjc_name		%{libobjc_name_orig}%{libobjc_major}
%define libgnat_name_orig	%{cross_prefix}libgnat
%define libgnat_name		%{libgnat_name_orig}%{libgnat_major}
%define libffi_name_orig	%{cross_prefix}libffi
%define libffi_name		%{libffi_name_orig}%{libffi_major}

%if %{mdkversion} >= 1010
%{expand:%%define mdk_version %(A=$(awk '{print $3}' /etc/release); if [ -n "$A" ];then echo $A;else echo Cooker;fi)}
%else
%{expand:%%define mdk_version %(A=$(awk '{print $4}' /etc/mandrake-release); if [ -n "$A" ];then echo $A;else echo Cooker;fi)}
%endif

Summary:	GNU Compiler Collection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/C

# Main source:	(CVS)
URL:		http://gcc.gnu.org/
Source0:	%{source_package}.tar.bz2
Source1:	gcc31-java.bz2
Source2:	gcc31-javac.bz2
Source3:	gcc32-jdk-config.bz2
# ColorGCC:	http://home.i1.net/~jamoyers/software/colorgcc/
Source4:	colorgcc-%{color_gcc_version}.tar.bz2
Source5:	gpc-%{gpc_snapshot}.tar.bz2
# FIXME: unless we get proper help2man package
Source6:	gcc33-help2man.pl.bz2
Source7:	build_cross_gcc3.3.sh

# CVS patches
Patch1: gcc33-hammer-%{hammer_date}.patch.bz2
Patch2: gcc33-mdkoptions.patch.bz2
Patch3: gcc33-pr11536-testcase.patch.bz2
Patch4: gcc33-pr9929-testcase.patch.bz2
Patch5: gcc33-gcse-volatile.patch.bz2

# MDK patches
Patch100: colorgcc-1.3.2-mdkconf.patch.bz2
Patch101: gcc33-pass-slibdir.patch.bz2
Patch102: gcc31-c++-diagnostic-no-line-wrapping.patch.bz2
Patch103: gcc32-pr7434-testcase.patch.bz2
Patch104: gcc33-pr8213-testcase.patch.bz2
Patch106: gcc33-x86_64-biarch-testsuite.patch.bz2
Patch107: gcc33-i386-mtune.patch.bz2
Patch108: gcc33-ada-addr2line.patch.bz2
Patch109: gcc33-ada-link.patch.bz2
Patch110: gcc33-ada-makefile.patch.bz2
Patch111: gcc33-multi-do-libdir.patch.bz2
Patch112: gcc33-cross-gxx_include_dir.patch.bz2
Patch113: gcc33-cross-inhibit_libc.patch.bz2
Patch114: gcc32-mklibgcc-serialize-crtfiles.patch.bz2
Patch115: gcc33-c++-classfn-member-template.patch.bz2
Patch116: gcc33-gpc.patch.bz2
Patch117: gcc33-gpc-serialize-build.patch.bz2
Patch119: gcc33-pr11631.patch.bz2
Patch120: gcc33-pr13179.patch.bz2
Patch121: gcc33-no-store-motion.patch.bz2
Patch122: gcc33-linux32.patch.bz2
Patch123: gcc33-ppc64-_LP64.patch.bz2
Patch124: gcc33-ppc-no-nof.patch.bz2
Patch125: gcc33-cross-bootstrap-no-gcov-in-libgcc.patch.bz2
Patch126: gcc33-ppc64-unwind-fixes.patch.bz2

# Red Hat patches
Patch200: gcc33-2.96-RH-compat.patch.bz2
Patch201: gcc33-fde-merge-compat.patch.bz2
Patch202: gcc33-debug-pr7241.patch.bz2
Patch205: gcc33-dwarf2-dtprel.patch.bz2
Patch206: gcc33-trunc_int_for_mode.patch.bz2
Patch209: gcc33-inline-label.patch.bz2
Patch210: gcc33-ia64-symbol_ref_flags.patch.bz2
Patch211: gcc33-cse-tweak.patch.bz2
Patch212: gcc33-tls-direct-segment-addressing.patch.bz2
Patch213: gcc33-pie.patch.bz2
Patch216: gcc33-pr6794.patch.bz2
Patch218: gcc33-ia64-libjava-locks.patch.bz2
Patch219: gcc33-rhl-testsuite.patch.bz2
Patch220: gcc33-libgcc34.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# Want updated alternatives priorities
%if %{build_cross}
Conflicts:	gcc-cpp < 3.2.2-4mdk
%endif
# We want -pie support
Requires:	%{cross_prefix}binutils >= 2.14.90.0.5-1mdk
BuildRequires:	%{cross_prefix}binutils >= 2.14.90.0.5-1mdk
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1
BuildRequires:	zlib-devel
%if %{build_ada}
# Ada requires Ada to build
BuildRequires:	%{name}-gnat >= 3.1, %{libgnat_name} >= 3.1
%endif
Requires:	%{name}-cpp = %{version}-%{release}
Requires:	%{libgcc_name_orig} >= %{version}-%{release}
Requires(post,preun):		info-install
Requires(post,preun):		update-alternatives
BuildRequires:	gettext, flex, bison
BuildRequires:	texinfo >= 4.1
# Make sure pthread.h doesn't contain __thread keyword
%if !%{build_cross_bootstrap}
Requires:	%{cross_prefix}glibc-devel >= 2.2.5-14mdk
BuildRequires:	%{cross_prefix}glibc-devel >= 2.2.5-14mdk
%endif
%if %{build_check}
%if %{mdkversion} >= 900
BuildRequires:	%{cross_prefix}glibc-static-devel >= 2.2.5-14mdk
%endif
%endif
%if %{system_compiler}
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}
%endif
%if %{build_pdf_doc}
BuildRequires:	tetex, tetex-dvips, tetex-latex
%endif
%if %{build_check}
BuildRequires:	dejagnu
# libstdc++ regression testsuite needs those, just make sure they are
# installed instead of relying on good build environments
BuildRequires:	locales-de, locales-en, locales-es, locales-fr, locales-it
%endif

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.
This package is required for all other GCC compilers, namely C++,
Fortran 77, Objective C and Java.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C compiler version %{version}.

%package -n %{libgcc_name}
Summary:	GNU C library
Group:		System/Libraries
Provides:	%{libgcc_name_orig} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}%{branch}
Provides:	%{libgcc_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}3.0
Provides:	%{libgcc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libgcc_name_orig}3.2 = %{version}-%{release}

%description -n %{libgcc_name}
The %{libgcc_name} package contains GCC shared libraries for gcc %{branch}

####################################################################
# C++ Compiler

%package c++
Summary:	C++ support for gcc
Group:		Development/C++
%if %{system_compiler}
Obsoletes:	gcc%{branch}-c++
Provides:	gcc%{branch}-c++ = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{libstdcxx_name} = %{version}
Requires:	%{libstdcxx_name}-devel = %{version}
Requires(post,preun):		update-alternatives

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files; the library for dynamically linking
programs is available separately.

If you have multiple versions of GCC installed on your system, it is
preferred to type "g++-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C++ compiler version %{version}.

####################################################################
# C++ Libraries

%package -n %{libstdcxx_name}
Summary:	GNU C++ library
Group:		System/Libraries
Obsoletes:	%{libstdcxx_name_orig}%{branch}
Provides:	%{libstdcxx_name_orig}%{branch} = %{version}-%{release}
Provides:	%{libstdcxx_name_orig} = %{version}-%{release}
%if "%{branch}" == "3.3"
# By default, the libstdc++ from gcc3.3 is ABI compatible with the one
# from gcc3.2. Just tell other packages about it if they relied on that.
Provides:	%{libstdcxx_name_orig}3.2 = %{version}-%{release}
%endif

%description -n %{libstdcxx_name}
This package contains the GCC Standard C++ Library v3, an ongoing
project to implement the ISO/IEC 14882:1998 Standard C++ library.

%package -n %{libstdcxx_name}-devel
Summary:	Header files and libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name} = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-devel
Provides:	%{libstdcxx_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}-devel = %{version}-%{release}

%description -n %{libstdcxx_name}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development.

%package -n %{libstdcxx_name}-static-devel
Summary:	Static libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name}-devel = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-static-devel
Provides:	%{libstdcxx_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}-static-devel = %{version}-%{release}

%description -n %{libstdcxx_name}-static-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the static libraries needed for C++ development.

####################################################################
# Objective C Compiler

%package objc
Summary:	Objective C support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-objc
Provides:	gcc%{branch}-objc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}

%description objc
This package adds Objective C support to the GNU C compiler. Objective
C is an object oriented derivative of the C language, mainly used on
systems running NeXTSTEP. This package does not include the standard
Objective C object library.

####################################################################
# Objective C Libraries

%package -n %{libobjc_name}
Summary:	Objective C runtime libraries
Group:		System/Libraries
Obsoletes:	%{libobjc_name_orig}3.0, %{libobjc_name_orig}3.1
Provides:	%{libobjc_name_orig} = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.1 = %{version}-%{release}
%if !%{system_compiler}
Conflicts:	%{name}-objc < %{branch}
%endif

%description -n %{libobjc_name}
Runtime libraries for the GNU Objective C Compiler.

####################################################################
# Pascal Compiler

%package gpc
Summary:	Pascal support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gpc
Provides:	gcc%{branch}-gpc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}

%description gpc
The GNU Pascal Compiler (GPC) is, as the name says, the Pascal
compiler of the GNU family.  The compiler supports the following
language standards and quasi-standards:

  * ISO 7185 Pascal (see Resources),
  * most of ISO 10206 Extended Pascal,
  * Borland Pascal 7.0,
  * parts of Borland Delphi, Mac Pascal and Pascal-SC (PXSC). 

If you have multiple versions of GCC installed on your system, it is
preferred to type "gpc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Fortran 77 compiler version %{version}.

####################################################################
# Fortran 77 Compiler

%package g77
Summary:	Fortran 77 support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-g77
Provides:	gcc%{branch}-g77 = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{libf2c_name_orig} = %{version}-%{release}

%description g77
This package adds support for compiling Fortran 77 programs with the GNU
compiler.

If you have multiple versions of GCC installed on your system, it is
preferred to type "g77-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Fortran 77 compiler version %{version}.

####################################################################
# Fortran 77 Libraries

%package -n %{libf2c_name}
Summary:	Fortran 77 runtime libraries
Group:		System/Libraries
Provides:	%{libf2c_name_orig} = %{version}
Obsoletes:	%{libf2c_name_orig}%{branch}
Provides:	%{libf2c_name_orig}%{branch} = %{version}-%{release}

%description -n %{libf2c_name}
This package contains Fortran 77 shared library which is needed to run
Fortran 77 dynamically linked programs.

####################################################################
# Ada 95 Compiler

%package gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{libgnat_name} = %{version}-%{release}
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gnat
Provides:	gcc%{branch}-gnat = %{version}-%{release}
%endif
Obsoletes:	%{cross_prefix}gnat
Provides:	%{cross_prefix}gnat = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description gnat
This package contains an Ada95 compiler and associated development
tools based on the GNU gcc technology. Ada95 is the object oriented
successor of the Ada83 language. To build this package from sources
you must have installed a binary version to bootstrap the compiler.

####################################################################
# Ada 95 Libraries

%package -n %{libgnat_name}
Summary:	Ada 95 runtime libraries
Group:		System/Libraries
Provides:	%{libgnat_name_orig} = %{version}-%{release}
Obsoletes:	%{cross_prefix}gnat-runtime
Provides:	%{cross_prefix}gnat-runtime = %{version}-%{release}

%description -n %{libgnat_name}
This package contains the shared libraries required to run programs
compiled with the GNU Ada compiler (GNAT) if they are compiled to use
shared libraries.  It also contains the shared libraries for the
Implementation of the Ada Semantic Interface Specification (ASIS), the
implementation of Distributed Systems Programming (GLADE) and the
Posix 1003.5 Binding (Florist).

####################################################################
# Java Compiler

%package java
Summary:	Java support for gcc
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	gcc%{branch}-java
Provides:	gcc%{branch}-java = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{GCJ_TOOLS} = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_name}-devel >= %{version}
Requires(post,preun):		update-alternatives

%description java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcj-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Java compiler version %{version}.

####################################################################
# Java Runtime Tools

%package -n %{GCJ_TOOLS}
Summary:	Java related tools from gcc %{version}
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	%{cross_prefix}gcj%{branch}-tools
Provides:	%{cross_prefix}gcj%{branch}-tools = %{version}-%{release}
%endif
Provides:	%{cross_prefix}gcj-tools = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_name}-devel >= %{version}
Conflicts:	kaffe < 1.0.7-3mdk
Requires(post,preun):		update-alternatives

%description -n %{GCJ_TOOLS}
This package includes Java related tools built from gcc %{version}:

   * gij: a Java ByteCode Interpreter
   * gcj-jar: a fast .jar archiver
   * gcjh: generating C++ header files corresponding to ``.class'' files
   * jcf-dump: printing out useful information from a ``.class'' file
   * jv-scan: printing some useful information from a ``.java'' file

If you have multiple versions of GCC installed on your system, the
above-mentioned tools are called as follows: "<gcj_tool>-$(gcc%{branch}-version)"
(without double quotes).

####################################################################
# Java Libraries

%package -n %{libgcj_name}
Summary:	GNU Java runtime libraries
Group:		System/Libraries
Requires:	zip >= 2.1
Obsoletes:	%{cross_prefix}gcc-libgcj
Provides:	%{cross_prefix}gcc-libgcj = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}
Provides:	%{libgcj_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	libgcj3

%description -n %{libgcj_name}
Runtime libraries for the GNU Java Compiler. The libgcj includes parts
of the Java Class Libraries, plus glue to connect the libraries to the
compiler and the underlying OS.

%package -n %{libgcj_name}-devel
Summary:	Header files and libraries for Java development
Group:		Development/Java
Requires:	zip >= 2.1
Requires:	zlib-devel
Requires:	%{libgcj_name} = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}-devel
Provides:	%{libgcj_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-devel = %{version}-%{release}
Obsoletes:	libgcj3-devel

%description -n %{libgcj_name}-devel
Development headers and libraries for the GNU Java Compiler. The
libgcj includes parts of the Java Class Libraries, plus glue to
connect the libraries to the compiler and the underlying OS.

%package -n %{libgcj_name}-static-devel
Summary:	Static libraries for Java development
Group:		Development/Java
Requires:	%{libgcj_name}-devel = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}-static-devel
Provides:	%{libgcj_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-static-devel = %{version}-%{release}
Obsoletes:	libgcj3-static-devel

%description -n %{libgcj_name}-static-devel
Static libraries for the GNU Java Compiler.

####################################################################
# FFI headers and libraries

%package -n %{libffi_name}-devel
Summary:	Development headers and static library for FFI
Group:		Development/C
Obsoletes:	%{libffi_name_orig}%{branch}-devel
Provides:	%{libffi_name_orig}%{branch}-devel = %{version}-%{release}
Obsoletes:	%{libffi_name_orig}-devel
Provides:	%{libffi_name_orig}-devel = %{version}-%{release}
Provides:	ffi-devel = %{version}-%{release}

%description -n %{libffi_name}-devel
This package contains the development headers and the static library
for libffi. The libffi library provides a portable, high level
programming interface to various calling conventions. This allows a
programmer to call any function specified by a call interface
description at run time.

####################################################################
# Preprocessor

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
%if %{system_compiler}
Obsoletes:	gcc%{branch}-cpp
Provides:	gcc%{branch}-cpp = %{version}-%{release}
%endif
Requires(post,preun):		info-install
Requires(post,preun):		update-alternatives

%description cpp
The C preprocessor is a 'macro processor' which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define 'macros,' which are abbreviations for longer
constructs.

The C preprocessor provides four separate facilities that you can use as
you see fit:

* Inclusion of header files. These are files of declarations that can be
  substituted into your program.
* Macro expansion. You can define 'macros,' which are abbreviations for 
  arbitrary fragments of C code, and then the C preprocessor will replace
  the macros with their definitions throughout the program.
* Conditional compilation. Using special preprocessing directives,
  you can include or exclude parts of the program according to various
  conditions.
* Line control. If you use a program to combine or rearrange source files
  into an intermediate file which is then compiled, you can use line
  control to inform the compiler about where each source line originated.

You should install this package if you are a programmer who is searching for
such a macro processor.

If you have multiple versions of GCC installed on your system, you
will have to type "cpp -V%{version}" or "cpp-%{version}" (without double quotes)
in order to use the GNU C Preprocessor version %{version}.

####################################################################
# ColorGCC

%package colorgcc
Summary:	GCC output colorizer
Group:		Development/Other
Obsoletes:	gcc2.96-colorgcc
%if %{system_compiler}
Obsoletes:	gcc%{branch}-colorgcc
Provides:	gcc%{branch}-colorgcc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}
Requires(post,preun):		update-alternatives
Requires:	perl

%description colorgcc
ColorGCC is a Perl wrapper to colorize the output of compilers with
warning and error messages matching the GCC output format.

This package is configured to run with the associated system compiler,
that is GCC version %{version}. If you want to use it for another
compiler (e.g. gcc 2.96), you may have to define gccVersion: 2.96 and
uncomment the respective compiler paths in %{_sysconfdir}/colorgccrc
for a system-wide effect, or in ~/.colorgccrc for your user only.

####################################################################
# Documentation

%package doc
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
%endif

%description doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.

%package doc-pdf
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc-pdf
Provides:	gcc%{branch}-doc-pdf = %{version}-%{release}
%endif

%description doc-pdf
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler printable
documentation in PDF.

%prep
%setup -q -n %{source_dir} -a 4 -a 5
%if %{hammer_branch}
%patch1 -p1 -E
%patch2 -p1 -b .mdkoptions
%endif
%patch3 -p1 -b .pr11536-testcase
%patch4 -p1 -b .pr9929-testcase
%patch5 -p1 -b .gcse-volatile

# MDK patches
%patch101 -p1 -b .pass-slibdir
%patch102 -p1 -b .c++-diagnostic-no-line-wrapping
%patch103 -p1 -b .pr7434-testcase
%patch104 -p1 -b .pr8213-testcase
%patch106 -p1 -b .x86_64-biarch-testsuite
%patch107 -p1 -b .i386-mtune
%patch108 -p1 -b .ada-addr2line
%patch109 -p1 -b .ada-link
%patch110 -p1 -b .ada-makefile
%patch111 -p1 -b .multi-do-libdir
%patch112 -p1 -b .cross-gxx_include_dir
%patch113 -p1 -b .cross-inhibit_libc
%patch114 -p1 -b .mklibgcc-serialize-crtfiles
%patch115 -p1 -b .c++-classfn-member-template
%patch119 -p1 -b .pr11631-testcase
%patch120 -p1 -b .pr13179
%patch121 -p1 -b .no-store-motion
%patch122 -p1 -b .linux32
%patch123 -p1 -b .ppc64-_LP64
%patch124 -p1 -b .ppc-no-nof
%patch125 -p1 -b .cross-bootstrap-no-gcov-in-libgcc
%patch126 -p1 -b .ppc64-unwind-fixes

# Red Hat patches
%patch200 -p0 -b .2.96-RH-compat
%patch201 -p0 -b .fde-merge-compat
%patch202 -p0 -b .debug-pr7241
%patch205 -p1 -b .dwarf2-dtprel
%patch206 -p1 -b .trunc_int_for_mode
%patch209 -p0 -b .inline-label
%patch210 -p1 -b .ia64-symbol_ref_flags
%patch211 -p1 -b .cse-tweak
#%patch212 -p1 -b .tls-direct-segment-addressing
%patch213 -p1 -b .pie
%patch216 -p1 -b .pr6794
%patch218 -p1 -b .ia64-libjava-locks
%patch219 -p1 -b .rhl-testsuite
%patch220 -p0 -b .libgcc34

# Integrate GNU Pascal compiler
mv gpc-%{gpc_snapshot}/p gcc/p
rmdir gpc-%{gpc_snapshot}
patch -p0 < gcc/p/diffs/gcc-3.3.diff
%patch116 -p1 -b .gpc
%patch117 -p1 -b .gpc-serialize-build

# MDKzification for bug reports
perl -pi -e 's/3\.3\.3/3.3.2/' gcc/version.c
perl -pi -e "/bug_report_url/ and s/\"[^\"]+\"/\"<URL:https:\/\/qa.mandrakesoft.com\/>\"/;" \
         -e '/version_string/ and s/([0-9]*(\.[0-9]*){1,3}).*(\";)$/\1 \(Mandrakelinux %{mdk_version} %{version}-%{release}\)\3/;' \
         gcc/version.c

# ColorGCC patch
cd colorgcc-%{color_gcc_version};
%patch100 -p1 -b .mdkconf
perl -pi -e 's|GCC_VERSION|%{version}|' colorgcc*
cd ..

%build
# Force a seperate object dir
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

# FIXME: extra tools needed
mkdir -p bin
bzcat %{SOURCE6} >bin/help2man
export PATH=$PATH:$PWD/bin

# Make bootstrap-lean
CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g'`
%if %{build_debug}
OPT_FLAGS=`echo "$OPT_FLAGS -g" | sed -e "s/-fomit-frame-pointer//g"`
%endif
%if %{build_cross}
OPT_FLAGS="-O2 -pipe"
%endif
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fomit-frame-pointer//g'`
LANGUAGES="c"
%if %{build_cxx}
LANGUAGES="$LANGUAGES,c++"
%endif
%if %{build_ada}
LANGUAGES="$LANGUAGES,ada"
%endif
%if %{build_fortran}
LANGUAGES="$LANGUAGES,f77"
%endif
%if %{build_objc}
LANGUAGES="$LANGUAGES,objc"
%endif
%if %{build_java}
LANGUAGES="$LANGUAGES,java"
%endif
%if %{build_pascal}
LANGUAGES="$LANGUAGES,pascal"
%endif
PROGRAM_SUFFIX=""
%if !%{system_compiler}
PROGRAM_SUFFIX="--program-suffix=%{program_suffix}"
%endif
%if %{build_cxx}
LIBSTDCXX_V3_FLAGS="--enable-long-long --enable-__cxa_atexit --enable-clocale=gnu"
%endif
%if %{build_cross}
CROSS_FLAGS="--with-sysroot=%{_prefix}/%{target_cpu}-linux --disable-multilib"
%endif
%if %{build_cross_bootstrap}
CROSS_FLAGS="--disable-multilib --disable-shared --disable-threads"
%endif
[[ -n "$CROSS_FLAGS" ]] && CROSS_FLAGS="$CROSS_FLAGS --target=%{gcc_target_platform}"
# update config.{sub,guess} scripts
%{?__cputoolize: %{__cputoolize} -c ..}
%{?__cputoolize: %{__cputoolize} -c ../boehm-gc}
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --libdir=%{_libdir} --with-slibdir=/%{_lib} \
	--mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-shared --enable-threads=posix --disable-checking $LIBSTDCXX_V3_FLAGS \
	--enable-languages="$LANGUAGES" $PROGRAM_SUFFIX \
	--host=%{_target_platform} $CROSS_FLAGS \
%ifarch ppc64
	--enable-biarch \
%endif
	--with-system-zlib
touch ../gcc/c-gperf.h
%if %{build_cross}
%make
%else
%ifarch alpha
%make bootstrap-lean BOOT_CFLAGS="$OPT_FLAGS"
%else
%make bootstrap-lean
%endif
%endif

%if %{build_ada}
# This doesn't work with -j$RPM_BUILD_NCPUS
make -C gcc gnatlib-shared
make -C gcc gnattools
make -C gcc ada.info
%endif

%if !%{build_cross}
# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto
%endif
cd ..

# Copy various doc files here and there
mkdir -p rpm.doc/g77
mkdir -p rpm.doc/objc
mkdir -p rpm.doc/libjava
mkdir -p rpm.doc/libobjc
mkdir -p rpm.doc/boehm-gc
mkdir -p rpm.doc/fastjar
mkdir -p rpm.doc/gpc

%if %{build_pascal}
(cd gcc/p; for i in ChangeLog* README NEWS FAQ; do
	cp -p $i ../../rpm.doc/gpc/$i
done)
%endif
%if %{build_fortran}
(cd gcc/f; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/g77/$i.f
done)
(cd libf2c; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/g77/$i.libf2c
done)
%endif
%if %{build_objc}
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/libobjc/$i.libobjc
done)
%endif
%if %{build_java}
(cd boehm-gc; for i in ChangeLog*; do
        cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar; for i in ChangeLog* README*; do
        cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libjava; for i in README THANKS COPYING ChangeLog; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
(cd libjava; cp -p LIBGCJ_LICENSE ../rpm.doc/libjava/LICENSE.libjava)
%endif

# [ghibo] - build printable documentation
%if %{build_pdf_doc}
(cd gcc/doc; for file in gcc.texi cpp.texi cppinternals.texi; do
  texi2dvi -p -t @afourpaper -t @finalout -I ./include $file
done)
(cd gcc/ada; for file in gnat_rm.texi gnat_ug_unx.texi; do
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include $file
done
mv gnat_ug_unx.pdf gnat_ug.pdf
)
(cd gcc/f;
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include g77.texi
)
%endif

# Run tests
%ifarch %{biarches}
RUNTESTFLAGS="--target_board 'unix{-m32,}'"
%endif
echo ====================TESTING=========================
%if %{build_check}
cd obj-%{gcc_target_platform}
%make -k RUNTESTFLAGS="$RUNTESTFLAGS" check || true
logfile="$PWD/../%{name}-%{version}-%{release}.log"
../contrib/test_summary > $logfile
cd ..
%endif
echo ====================TESTING END=====================
 
%install
rm -rf $RPM_BUILD_ROOT

# Fix HTML docs for libstdc++-v3
perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html
find libstdc++-v3/docs/html -name CVS | xargs rm -rf

# Create some directories, just to make sure (e.g. ColorGCC)
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_infodir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

# ColorGCC stuff
%if %{build_colorgcc}
pushd colorgcc-%{color_gcc_version};
  install -m 755 colorgcc $RPM_BUILD_ROOT%{_bindir}/colorgcc-%{version}
  ln -s colorgcc-%{version} $RPM_BUILD_ROOT%{_bindir}/colorgcc
  install -m 644 colorgccrc $RPM_BUILD_ROOT%{_sysconfdir}/
  for i in COPYING CREDITS ChangeLog; do
    [ ! -f ../$i.colorgcc ] && mv -f $i ../$i.colorgcc
  done
popd
%endif

pushd obj-%{gcc_target_platform};
  %makeinstall slibdir=$RPM_BUILD_ROOT/%{_lib}
  %if %{build_ada}
  make -C gcc ada.install-info DESTDIR=$RPM_BUILD_ROOT
  for f in $RPM_BUILD_ROOT%{_infodir}/gnat_ug_unx.info*; do
    sed -e "s/gnat_ug_unx/gnat_ug/g" $f > ${f/gnat_ug_unx/gnat_ug}
  done
  chmod 644 $RPM_BUILD_ROOT%{_infodir}/gnat*
  %endif
popd

FULLVER=`$RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix} --version | head -n 1 | cut -d' ' -f3`
FULLPATH=$(dirname $RPM_BUILD_ROOT%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1)

#if [ "%{gcc_target_platform}" != "%{_target_platform}" ]; then
#   mv -f $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc $RPM_BUILD_ROOT%{_bindir}/%{_target_platform}-gcc
#fi

file $RPM_BUILD_ROOT/%{_bindir}/* | grep ELF | cut -d':' -f1 | xargs strip || :
strip $FULLPATH/cc1
%if %{build_cxx}
strip $FULLPATH/cc1plus
%endif
%if %{build_pascal}
strip $FULLPATH/gpc1
%endif
%if %{build_fortran}
strip $FULLPATH/f771
%endif
%if %{build_java}
strip $FULLPATH/{jc1,jvgenmain}
%endif

# Create /usr/bin/%{program_prefix}gcc%{branch}-version that contains the full version of gcc
cat >$RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version <<EOF
#!/bin/sh
echo "$FULLVER"
EOF
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version

# Fix program names
# (gb) For each primary program in every package, I want it to be
# named <program>-<version>
pushd $RPM_BUILD_ROOT%{_bindir}
for file in cpp gcc g++ gcj g77 gpc gpidump; do
  file_version="${file}-%{version}"
  if [ -x "$file" -a "(" ! -x "$file_version" -o -L "$file_version" ")" ]; then
    cp -f $file $file_version
    rm -f $file
    ln -s $file_version $file
  fi
  file="%{program_prefix}$file" file_version="%{program_prefix}$file_version"
  if [ -x "$file" -a ! -x "$file_version" ]; then
    cp -f $file $file_version
    rm -f $file
    ln -s $file_version $file
  fi
done
popd

# Fix some links
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/cc
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# First, move 32-bit libraries to the right directories
%ifarch %{biarches}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
mv $RPM_BUILD_ROOT%{_libdir}/32/* $RPM_BUILD_ROOT%{_prefix}/lib
rm -rf $RPM_BUILD_ROOT%{_libdir}/32
ln -sf ../lib $RPM_BUILD_ROOT%{_libdir}/32

mkdir -p $RPM_BUILD_ROOT/lib
rm -rf $RPM_BUILD_ROOT/%{_lib}/32
ln -sf ../lib $RPM_BUILD_ROOT/%{_lib}/32
%endif

# Dispatch Ada 95 libraries (special case)
%if %{build_ada}
pushd $FULLPATH/adalib
  rm -f libgnarl.so* libgnat.so*
  mv -f libgnarl-*.so.* $RPM_BUILD_ROOT%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnarl-*.so.* libgnarl.so
  mv -f libgnat-*.so.* $RPM_BUILD_ROOT%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnat-*.so.* libgnat.so
popd
%endif

# Strip debug info from libraries
STRIP_DEBUG=
%if !%{build_debug}
STRIP_DEBUG="strip -g"
if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
  STRIP_DEBUG="%{target_cpu}-linux-$STRIP_DEBUG"

fi
%endif

# Dispatch libraries to the right directories
DispatchLibs() {
	libname=$1 libversion=$2
	rm -f $libname.so $libname.a
	$STRIP_DEBUG ../../../$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../$crosslibdir/$libname.a
	ln -s ../../../$crosslibdir/$libname.so.$libversion $libname.so
	rm -f ../../../$crosslibdir/$libname.so
	cp -f ../../../$crosslibdir/$libname.a $libname.a
	rm -f ../../../$crosslibdir/$libname.a
	%ifarch %{biarches}
	[ -d 32 ] || mkdir 32
	pushd 32
	mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
	$STRIP_DEBUG ../../../../32/$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../../32/$crosslibdir/$libname.a
	ln -s ../../../../32/$libname.so.$libversion $libname.so
	rm -f ../../../../32/$libname.so
	[ -r "../../../../32/$libname.a" ] && {
	cp -f ../../../../32/$libname.a $libname.a
	rm -f ../../../../32/$libname.a
	}
	popd
	%endif
	%ifarch ppc
	[ -d nof ] || mkdir nof
	pushd nof
	$STRIP_DEBUG ../../../../nof/$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../../nof/$crosslibdir/$libname.a
	ln -s ../../../../nof/$libname.so.$libversion $libname.so
	rm -f ../../../../nof/$libname.so
	[ -r "../../../../nof/$libname.a" ] && {
	cp -f ../../../../nof/$libname.a $libname.a
	rm -f ../../../../nof/$libname.a
	}
	popd
	%endif
}
pushd $FULLPATH
	if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
	crosslibdir="../%{gcc_target_platform}/lib"
	fi
	%if %{build_cxx}
	DispatchLibs libstdc++	%{libstdcxx_major}.0.%{libstdcxx_minor}
	mv ../../../$crosslibdir/libsupc++.a libsupc++.a
	%ifarch %{biarches}
	mv -f ../../../32/libsupc++.a 32/libsupc++.a
	%endif
	%endif
	%if %{build_java}
	DispatchLibs libgcj	%{libgcj_major}.0.0
	DispatchLibs lib-org-xml-sax 0.0.0
	DispatchLibs lib-org-w3c-dom 0.0.0
	%endif
	%if %{build_objc}
	DispatchLibs libobjc	%{libobjc_major}.0.0
	%endif
	%if %{build_fortran}
	DispatchLibs libg2c	%{libf2c_major}.0.0
	mv -f ../../../$crosslibdir/libfrtbegin.a libfrtbegin.a
	[ -r "../../../32/libfrtbegin.a" ] &&
	mv -f ../../../32/libfrtbegin.a 32/libfrtbegin.a
	[ -r "../../../nof/libfrtbegin.a" ] &&
	mv -f ../../../nof/libfrtbegin.a nof/libfrtbegin.a
	%endif
popd

# Move Java headers to /usr/include/libgcj-<version>
%if %{build_java}
if [ "%{libjava_includedir}" != "%{_includedir}" ]; then
  mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}
  mv $RPM_BUILD_ROOT%{_includedir}/j*.h $RPM_BUILD_ROOT%{libjava_includedir}/
  for dir in gcj gnu java javax; do
    mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}/$dir
    mv $RPM_BUILD_ROOT%{_includedir}/$dir/* $RPM_BUILD_ROOT%{libjava_includedir}/$dir/
    rmdir $RPM_BUILD_ROOT%{_includedir}/$dir
  done

  # move <gcj/libgcj-config.h> too
  mv $FULLPATH/include/gcj/libgcj-config.h $RPM_BUILD_ROOT%{libjava_includedir}/gcj/
  rmdir $FULLPATH/include/gcj

  # include <libgcj/XXX.h> should lead to <libgcj-VERSION/XXX.h>
  ln -s %{libjava_includedir} $RPM_BUILD_ROOT%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/libgcj
  ln -s %{libjava_includedir} $RPM_BUILD_ROOT%{_includedir}/libgcj
fi
%endif

# Move libgcj.spec to compiler-specific directories
%if %{build_java}
mv $RPM_BUILD_ROOT%{_libdir}/libgcj.spec $FULLPATH/libgcj.spec
%endif

# Rename jar because it could clash with Kaffe's if this gcc
# is primary compiler (aka don't have the -<version> extension)
%if %{build_java}
pushd $RPM_BUILD_ROOT%{_bindir}/
  mv jar%{program_suffix} gcj-jar-%{version}
  for app in grepjar rmic rmiregistry; do
    mv $app%{program_suffix} gcj-$app-%{version}
  done
popd
%endif

# Add java and javac wrappers
%if %{build_java}
pushd $RPM_BUILD_ROOT%{_bindir}/
  SED_PATTERN="s|@GCJ_VERSION@|%{version}|;s|@JDK_VERSION@|%{JDK_VERSION}|;s|@JDK_INCLUDES@|-I%{libjava_includedir}|;"
  bzcat %{SOURCE1} | sed -e "$SED_PATTERN" > gcj-java-%{version}
  chmod 0755 gcj-java-%{version}
  bzcat %{SOURCE2} | sed -e "$SED_PATTERN" > gcj-javac-%{version}
  chmod 0755 gcj-javac-%{version}
  bzcat %{SOURCE3} | sed -e "$SED_PATTERN" > gcj-jdk-config-%{version}
  chmod 0755 gcj-jdk-config-%{version}
popd
%endif

# Move <cxxabi.h> to compiler-specific directories
%if %{build_cxx}
mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/
%endif

# Fix links to binaries
pushd $RPM_BUILD_ROOT%{_bindir};
	progs="cpp gcc"
	%if %{build_cxx}
	progs="$progs g++ c++"
	%endif
	for file in $progs; do
		[[ -L $file ]] && rm -f $file
		[[ -x $file ]] && mv $file "$file"-%{version}
		[[ -n "%{program_prefix}" ]] && {
			[[ -x "$file"-%{version} ]] && mv "$file"-%{version} "%{program_prefix}$file"-%{version}
			[[ -L "%{program_prefix}$file" ]] || {
				rm -f "%{program_prefix}$file"
				ln -s "%{program_prefix}$file"-%{version} "%{program_prefix}$file"
			}
		}
		[[ -x "%{program_prefix}$file"-%{version} ]] || { echo "ERROR: no versioned binary for $file"; exit 1; }
	done
	%if %{build_java}
	for file in gcjh jcf-dump jv-scan; do [ -x $file -a -n "%{program_suffix}" ] && mv $file "$file"-%{version}; done
	%endif
popd

# Link gnatgcc to gcc
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/gnatgcc

# Create an empty file with perms 0755
FakeAlternatives() {
  for file in ${1+"$@"}; do
    rm -f $file
    touch $file
    chmod 0755 $file
  done
}

# Alternatives provide /lib/cpp and %{_bindir}/cpp
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives cpp)
(mkdir -p $RPM_BUILD_ROOT/lib; cd $RPM_BUILD_ROOT/lib; ln -sf %{_bindir}/cpp cpp)

# Alternatives provide /usr/bin/{g77,f77}
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives g77 f77)

# Alternatives provide /usr/bin/c++
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives c++)

# Alternatives provide java programs
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives %{gcj_alternative_programs} javac)

# Alternatives provide jdk-config script
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives jdk-config)

if [[ -z "%{?cross_bootstrap:1}" ]]; then
# Move libgcc_s.so* to /%{_lib}
pushd $RPM_BUILD_ROOT/%{_lib}
  chmod 0755 libgcc_s.so.%{libgcc_major}
%if %{build_cross}
  mkdir -p $RPM_BUILD_ROOT%{target_libdir}
  mv -f libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s.so.%{libgcc_major}
  ln -sf libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s.so
%else
  mv -f libgcc_s.so.%{libgcc_major} libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} libgcc_s.so.%{libgcc_major}
  rm -f libgcc_s.so
  ln -sf ../../../../../%{_lib}/libgcc_s.so.%{libgcc_major} $FULLPATH/libgcc_s.so
%endif
popd
# Handle 32-bit libgcc
%ifarch %{biarches}
pushd $RPM_BUILD_ROOT/lib
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mv -f libgcc_s.so.%{libgcc_major} libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} libgcc_s.so.%{libgcc_major}
  rm -f libgcc_s.so libgcc_s_32.so
  ln -sf ../../../../../../lib/libgcc_s.so.%{libgcc_major} $FULLPATH/32/libgcc_s.so
  ln -sf ../../../../../../lib/libgcc_s.so.%{libgcc_major} $FULLPATH/32/libgcc_s_32.so
popd
%endif
fi

# Create c89 and c99 wrappers
%if %{system_compiler}
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/c?9
%endif

# FIXME: cpp, gcov manpages names
pushd $RPM_BUILD_ROOT%{_mandir}/man1;
  if [[ -n "%{program_prefix}%{program_suffix}" ]]; then
    for f in gcov cpp gcc g++ g77 gpc; do
      [[ -f "$f.1" ]] && mv $f.1 %{program_prefix}$f%{program_suffix}.1
    done
  fi
popd

# Fix info pages
if [[ "%{name}" = "gcc%{branch}" ]]; then
  cd $RPM_BUILD_ROOT%{_infodir}/
  for f in cpp cppinternals gcc gpc g77 gpcs gfortran gnat-style gnat_rm gnat_ug gcj; do
    if [[ -f "$f.info" ]]; then
      perl -pe "/^START-INFO-DIR-ENTRY/ .. /^END-INFO-DIR-ENTRY/ and s/($f)/\${1}-%{branch}/ig" $f.info > ${f}-%{branch}.info
      rm -f $f.info
    fi
  done
  cd ..
fi

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

# In case we are cross-compiling, don't bother to remake symlinks and
# don't let spec-helper when stripping files either
%if "%{name}" != "gcc"
export DONT_SYMLINK_LIBS=1
export DONT_STRIP=1
%endif

%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif

%clean
#rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_bindir}/%{cross_program_prefix}gcc %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/%{cross_program_prefix}gcc ] || update-alternatives --auto %{cross_program_prefix}gcc

%postun
if [ ! -f %{_bindir}/%{cross_program_prefix}gcc-%{version} ]; then
  update-alternatives --remove %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version}
fi

%post colorgcc
update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/%{program_prefix}colorgcc %(expr %{alternative_priority} + 50000)

%postun colorgcc
if [ ! -f %{_bindir}/colorgcc-%{version} ]; then
  update-alternatives --remove gcc %{_bindir}/colorgcc
  # update-alternatives silently ignores paths that don't exist
  update-alternatives --remove g++ %{_bindir}/colorgcc
  update-alternatives --remove g77 %{_bindir}/colorgcc
  update-alternatives --remove gcj %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-c++
update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000) --slave %{_bindir}/c++ c++ %{_bindir}/colorgcc

%triggerpostun colorgcc -- %{name}-c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
  update-alternatives --remove g++ %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-g77
update-alternatives --install %{_bindir}/g77 g77 %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000) --slave %{_bindir}/f77 f77 %{_bindir}/colorgcc

%triggerpostun colorgcc -- %{name}-g77
if [ ! -f %{_bindir}/g77-%{version} ]; then
  update-alternatives --remove g77 %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-java
update-alternatives --install %{_bindir}/gcj gcj %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000)

%triggerpostun colorgcc -- %{name}-java
if [ ! -f %{_bindir}/gcj-%{version} ]; then
  update-alternatives --remove gcj %{_bindir}/colorgcc
fi

%if %{build_cxx}
%post c++
update-alternatives --install %{_bindir}/%{cross_program_prefix}g++ %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version} %{alternative_priority} --slave %{_bindir}/%{cross_program_prefix}c++ %{cross_program_prefix}c++ %{_bindir}/%{program_prefix}g++-%{version}
[ -e %{_bindir}/%{cross_program_prefix}g++ ] || update-alternatives --auto %{cross_program_prefix}g++

%postun c++
if [ ! -f %{_bindir}/%{cross_program_prefix}g++-%{version} ]; then
  update-alternatives --remove %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version}
fi
%endif

%if %{build_cxx}
%post -n %{libstdcxx_name} -p /sbin/ldconfig
%postun -n %{libstdcxx_name} -p /sbin/ldconfig
%endif

%post -n %{libgcc_name} -p /sbin/ldconfig
%postun -n %{libgcc_name} -p /sbin/ldconfig

%post cpp
update-alternatives --install %{_bindir}/%{cross_program_prefix}cpp %{cross_program_prefix}cpp %{_bindir}/%{program_prefix}cpp-%{version} %{alternative_priority} --slave /lib/%{cross_program_prefix}cpp %{cross_program_prefix}lib_cpp %{_bindir}/%{program_prefix}cpp-%{version}
[ -e %{_bindir}/%{cross_program_prefix}cpp ] || update-alternatives --auto %{cross_program_prefix}cpp

%postun cpp
if [ ! -f %{_bindir}/cpp-%{version} ]; then
  update-alternatives --remove cpp %{_bindir}/%{program_prefix}cpp-%{version}
fi

%if %{build_pascal}
%post gpc
update-alternatives --install %{_bindir}/gpc gpc %{_bindir}/%{program_prefix}gpc-%{version} %{alternative_priority} --slave %{_bindir}/gpidump gpidump %{_bindir}/%{program_prefix}gpidump-%{version}
[ -e %{_bindir}/gpc ] || update-alternatives --auto gpc

%postun gpc
if [ ! -f %{_bindir}/gpc-%{version} ]; then
  update-alternatives --remove gpc %{_bindir}/%{program_prefix}gpc-%{version}
fi
%endif

%if %{build_fortran}
%post g77
update-alternatives --install %{_bindir}/%{cross_program_prefix}g77 %{cross_program_prefix}g77 %{_bindir}/%{program_prefix}g77-%{version} %{alternative_priority} --slave %{_bindir}/%{cross_program_prefix}f77 %{cross_program_prefix}f77 %{_bindir}/%{program_prefix}g77-%{version}
[ -e %{_bindir}/%{cross_program_prefix}g77 ] || update-alternatives --auto %{cross_program_prefix}g77

%postun g77
if [ ! -f %{_bindir}/%{cross_program_prefix}g77-%{version} ]; then
  update-alternatives --remove %{cross_program_prefix}g77 %{_bindir}/%{program_prefix}g77-%{version}
fi
%endif

%if %{build_java}
%post java
update-alternatives --install %{_bindir}/gcj gcj %{_bindir}/gcj-%{version} %{alternative_priority}
[ -e %{_bindir}/gcj ] || update-alternatives --auto gcj
# Remove binaries if not alternativeszificated yet
[ ! -L %{_bindir}/javac ] && /bin/rm -f %{_bindir}/javac
update-alternatives --install %{_bindir}/javac javac %{_bindir}/gcj-javac-%{version} %{gcj_alternative_priority}
update-alternatives --install %{_bindir}/jdk-config jdk-config %{_bindir}/gcj-jdk-config-%{version} %{gcj_alternative_priority}

%postun java
if [ ! -f %{_bindir}/gcj-%{version} ]; then
  update-alternatives --remove gcj %{_bindir}/gcj-%{version}
fi
if [ ! -f %{_bindir}/gcj-javac-%{version} ]; then
  update-alternatives --remove javac %{_bindir}/gcj-javac-%{version}
fi
if [ ! -f %{_bindir}/gcj-jdk-config-%{version} ]; then
  update-alternatives --remove jdk-config %{_bindir}/gcj-jdk-config-%{version}
fi
%endif

%if %{build_java}
%post -n %{GCJ_TOOLS}
for app in %{gcj_alternative_programs}; do
  # Remove binaries if not alternativeszificated yet
  [ ! -L %{_bindir}/$app ] && /bin/rm -f %{_bindir}/$app
  # Build slaves list
  [[ "$app" != java ]] && slaves="$slaves --slave %{_bindir}/$app $app %{_bindir}/gcj-$app-%{version}"
done
update-alternatives --install %{_bindir}/java java %{_bindir}/gcj-java-%{version} %{gcj_alternative_priority} $slaves
%endif

%if %{build_java}
%postun -n %{GCJ_TOOLS}
if [ ! -f "%{_bindir}/gcj-java-%{version}" ]; then
  update-alternatives --remove java %{_bindir}/gcj-java-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_name}-devel
update-alternatives --install %{_includedir}/libgcj libgcj %{_includedir}/libgcj-%{version} %{gcj_alternative_priority}
%endif

%if %{build_java}
%postun -n %{libgcj_name}-devel
if [ ! -d %{_includedir}/libgcj-%{version} ]; then
  update-alternatives --remove gcj %{_includedir}/libgcj-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_name} -p /sbin/ldconfig
%postun -n %{libgcj_name} -p /sbin/ldconfig
%endif

%if %{build_objc}
%post -n %{libobjc_name} -p /sbin/ldconfig
%postun -n %{libobjc_name} -p /sbin/ldconfig
%endif

%if %{build_fortran}
%post -n %{libf2c_name} -p /sbin/ldconfig
%postun -n %{libf2c_name} -p /sbin/ldconfig
%endif

%if %{build_ada}
%post -n %{libgnat_name} -p /sbin/ldconfig
%postun -n %{libgnat_name} -p /sbin/ldconfig
%endif

%post doc
%_install_info gcc%{_package_suffix}.info
%_install_info cpp%{_package_suffix}.info
%if %{build_pascal}
%_install_info gpc%{_package_suffix}.info
%_install_info gpcs%{_package_suffix}.info
%endif
%if %{build_fortran}
%_install_info g77%{_package_suffix}.info
%endif
%if %{build_ada}
%_install_info gnat_rm%{_package_suffix}.info
%_install_info gnat_ug%{_package_suffix}.info
%endif

%preun doc
if [ "$1" = "0" ];then /sbin/install-info %{_infodir}/gcc%{_package_suffix}.info.bz2 --dir=%{_infodir}/dir --remove;fi;
%_remove_install_info cpp%{_package_suffix}.info
%if %{build_pascal}
%_remove_install_info gpc%{_package_suffix}.info
%_remove_install_info gpcs%{_package_suffix}.info
%endif
%if %{build_fortran}
%_remove_install_info g77%{_package_suffix}.info
%endif
%if %{build_ada}
%_remove_install_info gnat_rm%{_package_suffix}.info
%_remove_install_info gnat_ug%{_package_suffix}.info
%endif

%files
%defattr(-,root,root)
#
%doc gcc/README* gcc/*ChangeLog*
%{_mandir}/man1/%{program_prefix}gcc%{program_suffix}.1*
%if "%{name}" == "gcc"
%{_mandir}/man1/gcov%{program_suffix}.1*
%endif
#
%{_bindir}/%{program_prefix}gcc%{branch}-version
%{_bindir}/%{program_prefix}gcc-%{version}
%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix}
%if "%{name}" == "gcc"
%{_bindir}/protoize%{program_suffix}
%{_bindir}/unprotoize%{program_suffix}
%{_bindir}/gcov%{program_suffix}
%endif
%if %{system_compiler}
%{_bindir}/cc
%{_bindir}/c89
%{_bindir}/c99
%endif
#
%if "%{build_cross}:%{build_cross_bootstrap}" == "1:0"
%{target_libdir}/libgcc_s.so
%endif
%if "%{name}" == "gcc%{package_suffix}"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcc_s.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc_s.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc_s_32.so
%endif
%endif
#
%ifarch %{biarches}
/%{_lib}/32
%{_libdir}/32
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/collect2
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/*crt*.o
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcc.a
%if !%{build_cross_bootstrap}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcc_eh.a
%endif
%if "%{name}" == "gcc"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/SYSCALLS.c.X
%endif
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/specs
%ifarch %{biarches}
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/*crt*.o
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc_eh.a
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/float.h
%if %{build_fortran}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/g2c.h
%endif
%if "%{arch}" == "i386"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/pmmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/emmintrin.h
%endif
%if "%{arch}" == "x86_64"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/pmmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/emmintrin.h
%endif
%if "%{arch}" == "ppc64"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/altivec.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/ppc-asm.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/spe.h
%endif
%if "%{arch}" == "ppc"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/altivec.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/ppc-asm.h
%endif
%if "%{arch}" == "ia64"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/ia64intrin.h
%endif
%if "%{arch}" == "m68k"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/math-68881.h
%endif
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/iso646.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/limits.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stdarg.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stdbool.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stddef.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/syslimits.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/unwind.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/varargs.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/README

%if "%{name}" == "%{cross_prefix}gcc"
%files -n %{libgcc_name}
%defattr(-,root,root)
%if "%{name}" == "gcc"
/%{_lib}/libgcc_s-%{version}.so.%{libgcc_major}
/%{_lib}/libgcc_s.so.%{libgcc_major}
%endif
%if %{?build_cross:0}%{!?build_cross:1}
%{target_libdir}/libgcc_s-%{version}.so.%{libgcc_major}
%{target_libdir}/libgcc_s.so.%{libgcc_major}
%endif
%ifarch %{biarches}
/lib/libgcc_s-%{version}.so.%{libgcc_major}
/lib/libgcc_s.so.%{libgcc_major}
%endif
%endif

%files cpp
%defattr(-,root,root)
#
%{_mandir}/man1/%{program_prefix}cpp%{program_suffix}.1*
#
/lib/cpp
%ghost %{_bindir}/%{cross_program_prefix}cpp
%{_bindir}/%{program_prefix}cpp-%{version}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1

%if %{build_cxx}
%files c++
%defattr(-,root,root)
#
%doc gcc/cp/ChangeLog*
%{_mandir}/man1/%{program_prefix}g++%{program_suffix}.1*
#
%ghost %{_bindir}/%{cross_program_prefix}c++
%{_bindir}/%{program_prefix}g++-%{version}
%{_bindir}/%{gcc_target_platform}-g++%{program_suffix}
%{_bindir}/%{gcc_target_platform}-c++%{program_suffix}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1plus
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}
%defattr(-,root,root)
%{target_libdir}/libstdc++.so.%{libstdcxx_major}
%{target_libdir}/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%ifarch %{biarches}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}-devel
%defattr(-,root,root)
#
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/docs/html/
#
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/cxxabi.h
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libstdc++.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libsupc++.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libstdc++.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libsupc++.a
%endif
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}-static-devel
%defattr(-,root,root)
%doc libstdc++-v3/README
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libstdc++.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libstdc++.a
%endif
%endif

%if %{build_objc}
%files objc
%defattr(-,root,root)
#
%doc rpm.doc/objc/*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1obj
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libobjc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libobjc.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libobjc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libobjc.so
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/objc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/objc/*.h
%endif

%if %{build_objc}
%files -n %{libobjc_name}
%defattr(-,root,root)
#
%doc rpm.doc/libobjc/*
%doc libobjc/THREADS* libobjc/ChangeLog
#
%{target_libdir}/libobjc.so.%{libobjc_major}
%{target_libdir}/libobjc.so.%{libobjc_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libobjc.so.%{libobjc_major}
%{_prefix}/lib/libobjc.so.%{libobjc_major}.0.0
%endif
%endif

%if %{build_pascal}
%files gpc
%defattr(-,root,root)
#
%doc rpm.doc/gpc/*
%{_mandir}/man1/%{program_prefix}gpc%{program_suffix}.1*
%{_mandir}/man1/%{program_prefix}/gpc-run%{program_suffix}.1*
#
%{_bindir}/gpc-run
%{_bindir}/binobj
%ghost %{_bindir}/gpc
%ghost %{_bindir}/gpidump
%{_bindir}/%{program_prefix}gpc-%{version}
%{_bindir}/%{program_prefix}gpidump-%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gpc1
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gpcpp
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgpc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/gpc-in-c.h
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.c
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.s
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.inc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.pas
%endif

%if %{build_fortran}
%files g77
%defattr(-,root,root)
#
%doc gcc/f/BUGS gcc/f/NEWS rpm.doc/g77/*
%{_mandir}/man1/%{program_prefix}g77%{program_suffix}.1*
#
%ghost %{_bindir}/g77
%ghost %{_bindir}/f77
%{_bindir}/%{program_prefix}g77-%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/f771
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libfrtbegin.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libg2c.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libg2c.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libfrtbegin.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libg2c.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libg2c.so
%endif
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/g2c.h
%endif

%if %{build_fortran}
%files -n %{libf2c_name}
%defattr(-,root,root)
#
%{target_libdir}/libg2c.so.%{libf2c_major}
%{target_libdir}/libg2c.so.%{libf2c_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libg2c.so.%{libf2c_major}
%{_prefix}/lib/libg2c.so.%{libf2c_major}.0.0
%endif
%endif

%if %{build_java}
%files java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_bindir}/gcj-%{version}
%{_bindir}/gcj-javac-%{version}
%{_bindir}/gcj-jdk-config-%{version}
%ghost %{_bindir}/javac
%ghost %{_bindir}/jdk-config
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/jc1
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/jvgenmain
%{_mandir}/man1/gcj.1*
%endif

%if %{build_java}
%files -n %{GCJ_TOOLS}
%defattr(-,root,root)
%doc rpm.doc/fastjar/*
%{_bindir}/gcj-java-%{version}
%{_bindir}/gcj-jar-%{version}
%{_bindir}/gcj-grepjar-%{version}
%{_bindir}/gcj-rmic-%{version}
%{_bindir}/gcj-rmiregistry-%{version}
%ghost %{_bindir}/java
%ghost %{_bindir}/jar
%ghost %{_bindir}/grepjar
%ghost %{_bindir}/rmic
%ghost %{_bindir}/rmiregistry
%{_bindir}/gij%{program_suffix}
%{_bindir}/gcjh%{program_suffix}
%{_bindir}/jcf-dump%{program_suffix}
%{_bindir}/jv-scan%{program_suffix}
#
%{_mandir}/man1/gij*.1*
%{_mandir}/man1/gcjh*.1*
%{_mandir}/man1/jv-scan*.1*
%{_mandir}/man1/jcf-dump*.1*
%endif

%if %{build_java}
%files -n %{libgcj_name}
%defattr(-,root,root)
#
%{target_libdir}/libgcj.so.%{libgcj_major}
%{target_libdir}/libgcj.so.%{libgcj_major}.0.0
%{target_libdir}/lib-org-xml-sax.so.0
%{target_libdir}/lib-org-xml-sax.so.0.0.0
%{target_libdir}/lib-org-w3c-dom.so.0
%{target_libdir}/lib-org-w3c-dom.so.0.0.0
%ifarch %{biarches}
%{_prefix}/lib/libgcj.so.%{libgcj_major}
%{_prefix}/lib/libgcj.so.%{libgcj_major}.0.0
%{_prefix}/lib/lib-org-xml-sax.so.0
%{_prefix}/lib/lib-org-xml-sax.so.0.0.0
%{_prefix}/lib/lib-org-w3c-dom.so.0
%{_prefix}/lib/lib-org-w3c-dom.so.0.0.0
%endif
#
%dir %{_datadir}/java
%{_datadir}/java/libgcj-%{version}.jar
%endif

%if %{build_java}
%files -n %{libgcj_name}-devel
%defattr(-,root,root)
#
%doc rpm.doc/boehm-gc/*
%doc rpm.doc/libjava/*
#
%{_bindir}/jv-convert%{program_suffix}
#
%ghost %{_includedir}/libgcj
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/libgcj
#
%dir %{libjava_includedir}
%{libjava_includedir}/jni.h
%{libjava_includedir}/jvmpi.h
%dir %{libjava_includedir}/gcj
%{libjava_includedir}/gcj/*.h
%dir %{libjava_includedir}/gnu
%{libjava_includedir}/gnu/*
%dir %{libjava_includedir}/java
%{libjava_includedir}/java/*
%dir %{libjava_includedir}/javax
%{libjava_includedir}/javax/*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.spec
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-w3c-dom.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-xml-sax.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcj.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-w3c-dom.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-xml-sax.so
%endif
%endif

%if %{build_java}
%files -n %{libgcj_name}-static-devel
%defattr(-,root,root)
%doc libjava/README libjava/LIBGCJ_LICENSE
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-w3c-dom.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-xml-sax.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcj.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-w3c-dom.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-xml-sax.a
%endif
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root)
#
%{_bindir}/gnat*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gnat1
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude/*.adb
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude/*.ads
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/*.ali
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/Makefile.adalib
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgmem.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnat.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnat.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnarl.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnarl.so
%endif

%if %{build_libffi}
%files -n %{libffi_name}-devel
%defattr(-,root,root)
%doc libffi/README libffi/LICENSE libffi/ChangeLog*
%{_includedir}/ffi*.h
%{_libdir}/libffi.a
%ifarch %{biarches}
%{_prefix}/lib/libffi.a
%endif
%endif

%if %{build_ada}
%files -n %{libgnat_name}
%defattr(-,root,root)
#
%{target_libdir}/libgnat-*.so.*
%{target_libdir}/libgnarl-*.so.*
%ifarch %{biarches}
# FIXME: not biarch ada yet
#%{_prefix}/lib/libgnat-*.so.*
#%{_prefix}/lib/libgnarl-*.so.*
%endif
%endif

%if %{build_colorgcc}
%files colorgcc
%defattr (-,root,root)
%doc COPYING.colorgcc CREDITS.colorgcc ChangeLog.colorgcc
%config(noreplace) %{_sysconfdir}/colorgccrc
%{_bindir}/colorgcc
%{_bindir}/colorgcc-%{version}
%endif

%if %{build_doc}
%files doc
%defattr(-,root,root)
%{_infodir}/cppinternals%{_package_suffix}.info*
%{_infodir}/cpp%{_package_suffix}.info*
%{_infodir}/gcc%{_package_suffix}.info*
%if %{build_ada}
%{_infodir}/gnat-style%{_package_suffix}.info*
%{_infodir}/gnat_rm%{_package_suffix}.info*
%{_infodir}/gnat_ug%{_package_suffix}.info*
%endif
%if %{build_java}
%{_infodir}/gcj%{_package_suffix}.info*
%endif
%if %{build_pascal}
%{_infodir}/gpc%{_package_suffix}.info*
%{_infodir}/gpcs%{_package_suffix}.info*
%endif
%if %{build_fortran}
%{_infodir}/g77%{_package_suffix}.info*
%endif
%endif

%if %{build_pdf_doc}
%files doc-pdf
%defattr(-,root,root)
%doc gcc/doc/cppinternals.pdf
%doc gcc/doc/gcc.pdf
%doc gcc/doc/cpp.pdf
%if %{build_ada}
%doc gcc/ada/gnat_rm.pdf
%doc gcc/ada/gnat_ug.pdf
%endif
%if %{build_fortran}
%doc gcc/f/g77.pdf
%endif
%endif

