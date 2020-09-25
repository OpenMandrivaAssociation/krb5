# wine uses krb5
%ifarch %{x86_64}
%bcond_without compat32
%endif

%bcond_with crosscompile
%bcond_with docs
%if %{with crosscompile}
%define bootstrap 1
%else
# FIXME disable
%define bootstrap 1
%endif
%define oname mit-krb5

%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define major 3
%define libname %mklibname %{name}_ %{major}
%define libk5crypto %mklibname k5crypto %{major}
%define lib32name %mklib32name %{name}_ %{major}
%define lib32k5crypto %mklib32name k5crypto %{major}

%define support_major 0
%define libnamesupport %mklibname %{name}support %{support_major}
%define lib32namesupport %mklib32name %{name}support %{support_major}

%define rad_major 0
%define libnamerad %mklibname krad %{rad_major}
%define lib32namerad %mklib32name krad %{rad_major}

%define mit_major 12
%define libkadm5clnt_mit %mklibname kadm5clnt_mit %{mit_major}
%define libkadm5srv_mit %mklibname kadm5srv_mit %{mit_major}
%define lib32kadm5clnt_mit %mklib32name kadm5clnt_mit %{mit_major}
%define lib32kadm5srv_mit %mklib32name kadm5srv_mit %{mit_major}

%define gssapi_major 2
%define libgssapi_krb5 %mklibname gssapi_%{name}_ %{gssapi_major}
%define lib32gssapi_krb5 %mklib32name gssapi_%{name}_ %{gssapi_major}

%define gssrpc_major 4
%define libgssrpc %mklibname gssrpc %{gssrpc_major}
%define lib32gssrpc %mklib32name gssrpc %{gssrpc_major}

%define kdb5_major 10
%define libkdb5 %mklibname kdb5_ %{kdb5_major}
%define lib32kdb5 %mklib32name kdb5_ %{kdb5_major}

%define ldap_major 1
%define libkdb_ldap %mklibname kdb_ldap %{ldap_major}
%define lib32kdb_ldap %mklib32name kdb_ldap %{ldap_major}

%define develname %mklibname -d %{name}
%define devel32name %mklib32name -d %{name}
# enable checking after compile
%define enable_check 0
%{?_with_check: %global %enable_check 1}
%global optflags %{optflags} -Oz

Summary:	The Kerberos network authentication system
Name:		krb5
Version:	1.18.2
Release:	2
License:	MIT
Url:		http://web.mit.edu/kerberos/www/
Group:		System/Libraries
# from http://web.mit.edu/kerberos/dist/krb5/1.9/krb5-1.9.2-signed.tar
Source0:	http://web.mit.edu/kerberos/dist/krb5/%(echo %{version} |cut -d. -f1-2)/krb5-%{version}.tar.gz
Source1:	http://web.mit.edu/kerberos/dist/krb5/%(echo %{version} |cut -d. -f1-2)/krb5-%{version}.tar.gz.asc
Source2:	kprop.service
Source4:	kadmin.service
Source5:	krb5kdc.service
Source6:	krb5.conf
Source10:	kdc.conf
Source11:	kadm5.acl
Source19:	krb5kdc.sysconfig
Source20:	kadmin.sysconfig
# The same source files we "check", generated with "krb5-tex-pdf.sh create"
# and tarred up.
Source23:	krb5-1.10.3-pdf.tar.xz
Source24:	krb5-tex-pdf.sh
Source25:	krb5-1.10-manpaths.txt
Source29:	ksu.pamd
Source30:	kerberos-iv.portreserve
Source31:	kerberos-adm.portreserve
Source32:	krb5_prop.portreserve
Source33:	krb5kdc.logrotate
Source34:	kadmind.logrotate
Source35:	kdb_check_weak.c
Source40:	%{name}.rpmlintrc

Patch5:		krb5-1.10-ksu-access.patch
Patch7:		krb5-1.16-clang.patch
Patch16:	krb5-1.12-buildconf.patch
Patch23:	krb5-1.3.1-dns.patch
Patch39:	krb5-1.12-api.patch
Patch60:	krb5-1.12.1-pam.patch
Patch75:	krb5-pkinit-debug.patch
Patch86:	krb5-1.9-debuginfo.patch
Patch107:	krb5-aarch64.patch
Patch109:	Address-some-optimized-out-memset-calls.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	diffutils
BuildRequires:	libtool
BuildRequires:	keyutils-devel
BuildRequires:	pam-devel
BuildRequires:	python-sphinx
BuildRequires:	lmdb-devel
%ifarch riscv64
BuildRequires:	atomic-devel
%endif
# For _unitdir macro
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(com_err)
BuildRequires:	pkgconfig(libverto)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ss)
%if %{with docs}
BuildRequires:	texlive
BuildRequires:	texlive-latex-bin
%endif
%if %enable_check
BuildRequires:	dejagnu
%endif
%if !%{bootstrap}
BuildRequires:	openldap-devel
%endif
Conflicts:	%{_lib}krb53 < 1.9.2-3
%if %{with compat32}
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libncurses)
BuildRequires:	devel(libssl)
BuildRequires:	devel(libcom_err)
BuildRequires:	devel(libss)
BuildRequires:	devel(libncurses)
%endif
# (tpg) fix upgrade from older releases
Provides:	krb5 = 1.16.3-2
Provides:	krb5 = 1.16.3-1

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.

%package -n %{develname}
Summary:	Development files needed for compiling Kerberos 5 programs
Group:		Development/Other
Requires:	%{libname} >= %{version}
Requires:	%{libgssapi_krb5} >= %{version}
Requires:	%{libgssrpc} >= %{version}
Requires:	%{libnamesupport} >= %{version}
Requires:	%{libkadm5clnt_mit} >= %{version}
Requires:	%{libkadm5srv_mit} >= %{version}
Requires:	%{libkdb5} >= %{version}
Requires:	%{libnamerad} >= %{version}
Requires:	pkgconfig(ext2fs)
%if !%{bootstrap}
Requires:	%{libkdb_ldap} >= %{version}
%endif
Provides:	krb5-devel = %{EVRD}
Obsoletes:	%{_lib}krb53-devel

%description -n %{develname}
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.

%package -n %{libname}
Summary:	The shared library used by Kerberos 5
Group:		System/Libraries
Obsoletes:	%{_lib}krb53
%rename krb5-libs

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{libgssapi_krb5}
Summary:	The shared library used by Kerberos 5 - gssapi_krb5
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libgssapi_krb5}
This package contains the shared library gssrpc for %{name}.

%package -n %{libgssrpc}
Summary:	The shared library used by Kerberos 5 - gssrpc
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libgssrpc}
This package contains the shared library gssrpc for %{name}.

%package -n %{libk5crypto}
Summary:	The shared library used by Kerberos 5 - k5crypto
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libk5crypto}
This package contains the shared library k5crypto for %{name}.

%package -n %{libnamesupport}
Summary:	The shared library used by Kerberos 5 - krb5support
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libnamesupport}
This package contains the shared library krb5support for %{name}.

%package -n %{libnamerad}
Summary:	The shared library used by Kerberos 5 - krad
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libnamerad}
This package contains the shared library krad for %{name}.

%package -n %{libkadm5clnt_mit}
Summary:	The shared library used by Kerberos 5 - kadm5clnt_mit
Group:		System/Libraries
Requires:	%{name} >= %{version}
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libkadm5clnt_mit}
This package contains the shared library kadm5clnt_mit for %{name}.

%package -n %{libkadm5srv_mit}
Summary:	The shared library used by Kerberos 5 - kadm5srv_mit
Group:		System/Libraries
Requires:	%{name} >= %{version}
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libkadm5srv_mit}
This package contains the shared library kadm5srv_mit for %{name}.

%package -n %{libkdb5}
Summary:	The shared library used by Kerberos 5 - kdb5
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n %{libkdb5}
This package contains the shared library kdb5 for %{name}.

%package -n %{libkdb_ldap}
Summary:	The shared library used by Kerberos 5 - kdb_ldap
Group:		System/Libraries
Conflicts:	krb5-server-ldap < 1.9.2-3

%description -n %{libkdb_ldap}
This package contains the shared library kdb_ldap for %{name}.

%package server
Summary:	The server programs for Kerberos 5
Group:		System/Servers
Requires(post,preun):	rpm-helper
Requires(post,preun,postun):	systemd
# we drop files in its directory, but we don't want to own that directory
Requires:	logrotate
# mktemp is used by krb5-send-pr
Requires:	coreutils
# portreserve is used by init scripts for kadmind, kpropd, and krb5kdc
Requires:	portreserve

%description server
Kerberos is a network authentication system.  The krb5-server package
contains the programs that must be installed on a Kerberos 5 server.
If you're installing a Kerberos 5 server, you need to install this
package (in other words, most people should NOT install this
package).

%package server-ldap
Summary:	The LDAP storage plugin for the Kerberos 5 KDC
Group:		System/Servers
Requires:	%{name}-server >= %{version}

%description server-ldap
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC). If you are installing a Kerberos 5 KDC,
and you wish to use a directory server to store the data for your
realm, you need to install this package. 

%package workstation
Summary:	Kerberos 5 programs for use on workstations
Group:		System/Base
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Provides:	kerberos-workstation

%description workstation
Kerberos is a network authentication system.  The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be installed
on every workstation.

%package pkinit-openssl
Summary:	The PKINIT module for Kerberos 5
Group:		System/Libraries

%description pkinit-openssl
Kerberos is a network authentication system. The krb5-pkinit-openssl
package contains the PKINIT plugin, which uses OpenSSL to allow clients
to obtain initial credentials from a KDC using a private key and a
certificate.

%if %{with compat32}
%package -n libverto0
Summary:	Verto library (32-bit)
Group:		System/Libraries

%description -n libverto0
Verto library (32-bit)

%files -n libverto0
%{_prefix}/lib/libverto.so.0*

%package -n %{devel32name}
Summary:	Development files needed for compiling Kerberos 5 programs (32-bit)
Group:		Development/Other
Requires:	%{develname} = %{EVRD}
Requires:	%{lib32name} >= %{version}
Requires:	%{lib32gssapi_krb5} >= %{version}
Requires:	%{lib32gssrpc} >= %{version}
Requires:	%{lib32namesupport} >= %{version}
Requires:	%{lib32kadm5clnt_mit} >= %{version}
Requires:	%{lib32kadm5srv_mit} >= %{version}
Requires:	%{lib32kdb5} >= %{version}
Requires:	%{lib32namerad} >= %{version}
Requires:	devel(libcom_err)
Requires:	devel(libss)
%if !%{bootstrap}
Requires:	%{lib32kdb_ldap} >= %{version}
%endif

%description -n %{devel32name}
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.

%package -n %{lib32name}
Summary:	The shared library used by Kerberos 5 (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the shared library for %{name}.

%package -n %{lib32gssapi_krb5}
Summary:	The shared library used by Kerberos 5 - gssapi_krb5 (32-bit)
Group:		System/Libraries

%description -n %{lib32gssapi_krb5}
This package contains the shared library gssrpc for %{name}.

%package -n %{lib32gssrpc}
Summary:	The shared library used by Kerberos 5 - gssrpc (32-bit)
Group:		System/Libraries

%description -n %{lib32gssrpc}
This package contains the shared library gssrpc for %{name}.

%package -n %{lib32k5crypto}
Summary:	The shared library used by Kerberos 5 - k5crypto (32-bit)
Group:		System/Libraries

%description -n %{lib32k5crypto}
This package contains the shared library k5crypto for %{name}.

%package -n %{lib32namesupport}
Summary:	The shared library used by Kerberos 5 - krb5support (32-bit)
Group:		System/Libraries

%description -n %{lib32namesupport}
This package contains the shared library krb5support for %{name}.

%package -n %{lib32namerad}
Summary:	The shared library used by Kerberos 5 - krad (32-bit)
Group:		System/Libraries

%description -n %{lib32namerad}
This package contains the shared library krad for %{name}.

%package -n %{lib32kadm5clnt_mit}
Summary:	The shared library used by Kerberos 5 - kadm5clnt_mit (32-bit)
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n %{lib32kadm5clnt_mit}
This package contains the shared library kadm5clnt_mit for %{name}.

%package -n %{lib32kadm5srv_mit}
Summary:	The shared library used by Kerberos 5 - kadm5srv_mit (32-bit)
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n %{lib32kadm5srv_mit}
This package contains the shared library kadm5srv_mit for %{name}.

%package -n %{lib32kdb5}
Summary:	The shared library used by Kerberos 5 - kdb5 (32-bit)
Group:		System/Libraries

%description -n %{lib32kdb5}
This package contains the shared library kdb5 for %{name}.

%package -n %{lib32kdb_ldap}
Summary:	The shared library used by Kerberos 5 - kdb_ldap (32-bit)
Group:		System/Libraries

%description -n %{lib32kdb_ldap}
This package contains the shared library kdb_ldap for %{name}.
%endif

%prep
%setup -q -a 23 -n krb5-%{version}
ln -s NOTICE LICENSE

%patch60 -p1 -b .pam

#patch5  -p1 -b .ksu-access
%patch7 -p1 -b .compile~
#patch16 -p1 -b .buildconf
%patch23 -p1 -b .dns
%patch39 -p1 -b .api
#patch75 -p1 -b .pkinit-debug
%patch86 -p1 -b .debuginfo
#patch107 -p1 -b .aarch64

sed -i s,^attributetype:,attributetypes:,g \
    src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif 

%build
cd src
    autoreconf -fi
cd -
%if %{with crosscompile}
export krb5_cv_attr_constructor_destructor=yes
export ac_cv_func_regcomp=yes
export ac_cv_printf_positional=yes
export ac_cv_file__etc_environment=no
export ac_cv_file__etc_TIMEZONE=no
sed -i "406d" src/include/k5-platform.h
%endif

%serverbuild
# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=$(echo $CFLAGS|sed -e 's|-fPIE||g')
CXXFLAGS=$(echo $CXXFLAGS|sed -e 's|-fPIE||g')
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS|sed -e 's|-fPIE||g')

cd src
# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="$(echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC)"
CPPFLAGS="$(echo $DEFINES $INCLUDES)"

export CONFIGURE_TOP="$(pwd)"
mkdir build32
cd build32
export krb5_cv_attr_constructor_destructor=yes
export ac_cv_func_regcomp=yes
export ac_cv_printf_positional=yes
%configure32 \
	--host=i686-openmandriva-linux-gnu \
	--target=i686-openmandriva-linux-gnu \
	--with-system-et \
	--with-system-ss
sed -i -e 's,/\* #undef CONSTRUCTOR_ATTR_WORKS \*/,#define CONSTRUCTOR_ATTR_WORKS 1,g' include/autoconf.h
sed -i -e 's,/\* #undef DESTRUCTOR_ATTR_WORKS \*/,#define DESTRUCTOR_ATTR_WORKS 1,g' include/autoconf.h
%make_build || :
# Something regenerates autoconf.h in the middle of the build, so we have to patch it again
sed -i -e 's,/\* #undef CONSTRUCTOR_ATTR_WORKS \*/,#define CONSTRUCTOR_ATTR_WORKS 1,g' include/autoconf.h
sed -i -e 's,/\* #undef DESTRUCTOR_ATTR_WORKS \*/,#define DESTRUCTOR_ATTR_WORKS 1,g' include/autoconf.h
%make_build
unset krb5_cv_attr_constructor_destructor
unset ac_cv_func_regcomp
unset ac_cv_printf_positional
cd ..

mkdir build
cd build
%configure \
	CC="%{__cc}" \
	CFLAGS="$CFLAGS" \
	CPPFLAGS="$CPPFLAGS" \
	--enable-shared \
	--localstatedir=%{_sysconfdir}/kerberos \
	--enable-dns-for-realm \
	--enable-pkinit \
	--with-system-verto \
	--without-tcl \
	--with-system-et \
	--with-system-ss \
	--disable-static \
	--disable-rpath \
	--with-prng-alg=os \
	--with-crypto-impl=openssl \
	--with-tls-impl=openssl \
%if !%{bootstrap}
	--with-ldap \
%endif
	--with-pam

	#--with-netlib=-lresolv

%make
cd -

%if %{with docs}
# Build the docs.
make -C src/build/doc paths.py version.py
cp src/doc/paths.py doc/
mkdir -p build-man build-html build-pdf
sphinx-build -a -b man   -t pathsubs doc build-man
sphinx-build -a -b html  -t pathsubs doc build-html
rm -fr build-html/_sources
sphinx-build -a -b latex -t pathsubs doc build-pdf
make -C build-pdf
%endif


%check
# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_tmppath}

%install
%if %{with compat32}
# 32-bit stuff...
make -C src/build32 \
    DESTDIR=%{buildroot} \
    EXAMPLEDIR=%{_docdir}/%{develname}/examples\
    install
%endif


# Sample KDC config files (bundled kdc.conf and kadm5.acl).
install -d %{buildroot}%{_sysconfdir}/kerberos/krb5kdc
install -m0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kdc.conf
install -m0600 %{SOURCE11} %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

# Default configuration file for everything.
install -d %{buildroot}%{_sysconfdir}
install -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/krb5.conf

# Server init scripts (krb5kdc,kadmind,kpropd) and their sysconfig files.
install -d %{buildroot}%{_unitdir}
for init in \
    %{SOURCE5} \
    %{SOURCE4} \
    %{SOURCE2} ; do
    install -m0644 ${init} %{buildroot}%{_unitdir}
done

install -d %{buildroot}%{_sysconfdir}/sysconfig
for sysconfig in \
    %{SOURCE19} \
    %{SOURCE20} ; do
    install -m0644 ${sysconfig} \
    %{buildroot}%{_sysconfdir}/sysconfig/`basename ${sysconfig} .sysconfig`
done

# portreserve configuration files.
install -d %{buildroot}%{_sysconfdir}/portreserve
for portreserve in \
    %{SOURCE30} \
    %{SOURCE31} \
    %{SOURCE32} ; do
    install -m0644 ${portreserve} \
    %{buildroot}/%{_sysconfdir}/portreserve/`basename ${portreserve} .portreserve`
done

# logrotate configuration files
install -d %{buildroot}%{_sysconfdir}/logrotate.d
for logrotate in \
    %{SOURCE33} \
    %{SOURCE34} ; do
    install -m0644 ${logrotate} \
    %{buildroot}%{_sysconfdir}/logrotate.d/`basename ${logrotate} .logrotate`
done

# PAM configuration files.
install -d %{buildroot}%{_sysconfdir}/pam.d/
for pam in \
    %{SOURCE29} ; do
    install -m0644 ${pam} \
    %{buildroot}/%{_sysconfdir}/pam.d/`basename ${pam} .pamd`
done

# Plug-in directories.
install -d %{buildroot}%{_libdir}/krb5/plugins/preauth
install -d %{buildroot}%{_libdir}/krb5/plugins/kdb
install -d %{buildroot}%{_libdir}/krb5/plugins/authdata

# The rest of the binaries, headers, libraries, and docs.
make -C src/build \
    DESTDIR=%{buildroot} \
    EXAMPLEDIR=%{_docdir}/%{develname}/examples\
    install

# logdir
install -d %{buildroot}/var/log/kerberos

# clear the LDFLAGS
perl -pi -e "s|^LDFLAGS.*|LDFLAGS=''|g" %{buildroot}%{_bindir}/krb5-config

%if %{bootstrap}
rm %{buildroot}%{_mandir}/man8/kdb5_ldap_util.8*
%endif

%find_lang mit-krb5

%if %{with docs}
# Install processed man pages.
for section in 1 5 8; do
    install -m 644 build-man/*.$section %{buildroot}%{_mandir}/man$section/
done
%endif

%post server
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
exit 0

%preun server
if [ "$1" -eq "0" ] ; then
    /bin/systemctl --no-reload disable krb5kdc.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable kadmin.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable kprop.service > /dev/null 2>&1 || :
    /bin/systemctl stop krb5kdc.service > /dev/null 2>&1 || :
    /bin/systemctl stop kadmin.service > /dev/null 2>&1 || :
    /bin/systemctl stop kprop.service > /dev/null 2>&1 || :
fi
exit 0

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart krb5kdc.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart kadmin.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart kprop.service >/dev/null 2>&1 || :
fi

%triggerun server -- krb5-server < 1.9.2-1
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del krb5kdc >/dev/null 2>&1 || :
/sbin/chkconfig --del kadmin >/dev/null 2>&1 || :
/sbin/chkconfig --del kprop >/dev/null 2>&1 || :
/bin/systemctl try-restart krb5kdc.service >/dev/null 2>&1 || :
/bin/systemctl try-restart kadmin.service >/dev/null 2>&1 || :
/bin/systemctl try-restart kprop.service >/dev/null 2>&1 || :


%files -f mit-krb5.lang
%doc README
%config(noreplace) %{_sysconfdir}/krb5.conf
%dir %{_sysconfdir}/kerberos
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/authdata
%dir %{_libdir}/krb5/plugins/tls
#{_libdir}/krb5/plugins/*
#%{_libdir}/krb5/plugins/preauth/encrypted_challenge.so
%{_libdir}/krb5/plugins/preauth/otp.so
%{_libdir}/krb5/plugins/preauth/test.so
%{_libdir}/krb5/plugins/preauth/spake.so
%{_libdir}/krb5/plugins/kdb/db2.so 
%{_libdir}/krb5/plugins/tls/k5tls.so

%files workstation
%doc src/config-files/services.append
%if %{with docs}
%doc build-html/*
%doc build-pdf/user.pdf build-pdf/basic.pdf
%endif
%attr(0755,root,root) %doc src/config-files/convert-config-files
%{_mandir}/man7/kerberos.7*
%{_mandir}/man5/krb5.conf.5*
%{_bindir}/kdestroy
%{_bindir}/kswitch
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kswitch.1*
%{_bindir}/kinit
%{_mandir}/man5/.k5identity.5*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_mandir}/man1/kpasswd.1*
%{_bindir}/kvno
%{_mandir}/man1/kvno.1*
%{_bindir}/kadmin
%{_mandir}/man1/kadmin.1*
%{_bindir}/k5srvutil
%{_mandir}/man1/k5srvutil.1*
%{_bindir}/ktutil
%{_mandir}/man1/ktutil.1*
%{_mandir}/man5/k5identity.5.*
%{_mandir}/man5/k5login.5.*
%attr(4755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%config(noreplace) /etc/pam.d/ksu
%{_sbindir}/krb5-send-pr

%files server
%if %{with docs}
%doc build-pdf/admin.pdf build-pdf/build.pdf
%endif
%{_unitdir}/krb5kdc.service
%{_unitdir}/kadmin.service
%{_unitdir}/kprop.service
%config(noreplace) %{_sysconfdir}/sysconfig/krb5kdc
%config(noreplace) %{_sysconfdir}/sysconfig/kadmin
%config(noreplace) %{_sysconfdir}/portreserve/kerberos-iv
%config(noreplace) %{_sysconfdir}/portreserve/kerberos-adm
%config(noreplace) %{_sysconfdir}/portreserve/krb5_prop
%config(noreplace) %{_sysconfdir}/logrotate.d/krb5kdc
%config(noreplace) %{_sysconfdir}/logrotate.d/kadmind
%dir /var/log/kerberos
%dir %{_sysconfdir}/kerberos/krb5kdc
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kadm5.acl
%{_mandir}/man5/kadm5.acl.5*
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/kproplog
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc
%{_mandir}/man8/krb5kdc.8*
%{_sbindir}/sim_server
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_mandir}/man1/krb5-config.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*

%files -n %{libgssapi_krb5}
%{_libdir}/libgssapi_krb5.so.%{gssapi_major}*

%files -n %{libgssrpc}
%{_libdir}/libgssrpc.so.%{gssrpc_major}*

%files -n %{libk5crypto}
%{_libdir}/libk5crypto.so.%{major}*

%files -n %{libname}
%{_libdir}/libkrb5.so.%{major}*

%files -n %{libnamesupport}
%{_libdir}/libkrb5support.so.%{support_major}*

%files -n %{libnamerad}
%{_libdir}/libkrad.so.%{rad_major}*

%files -n %{libkadm5clnt_mit}
%{_libdir}/libkadm5clnt_mit.so.%{mit_major}*

%files -n %{libkadm5srv_mit}
%{_libdir}/libkadm5srv_mit.so.%{mit_major}*

%files -n %{libkdb5}
%{_libdir}/libkdb5.so.%{kdb5_major}*

%if !%{bootstrap}
%files -n %{libkdb_ldap}
%{_libdir}/libkdb_ldap.so.%{ldap_major}*
%endif

%files -n %{develname}
%if %{with docs}
%doc build-pdf/appdev.pdf build-pdf/plugindev.pdf
%endif
%{_docdir}/%{_lib}krb5-devel
%{_includedir}/*.h
%{_includedir}/gssapi
%{_includedir}/gssrpc
%{_includedir}/kadm5
%{_includedir}/krb5
%{_bindir}/krb5-config
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so
%{_libdir}/libkrad.so
%if !%{bootstrap}
%{_libdir}/libkdb_ldap.so
%endif
%{_libdir}/pkgconfig/*

# Protocol test clients
%{_bindir}/sim_client
%{_bindir}/gss-client
%{_bindir}/uuclient

# Protocol test servers
%{_sbindir}/gss-server
%{_sbindir}/uuserver

%files pkinit-openssl
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files server-ldap
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%{_libdir}/krb5/plugins/kdb/klmdb.so
%if !%{bootstrap}
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_sbindir}/kdb5_ldap_util
%{_mandir}/man8/kdb5_ldap_util.8*
%endif

%if %{with compat32}
%files -n %{lib32gssapi_krb5}
%{_prefix}/lib/libgssapi_krb5.so.%{gssapi_major}*

%files -n %{lib32gssrpc}
%{_prefix}/lib/libgssrpc.so.%{gssrpc_major}*

%files -n %{lib32k5crypto}
%{_prefix}/lib/libk5crypto.so.%{major}*

%files -n %{lib32name}
%{_prefix}/lib/libkrb5.so.%{major}*
%{_prefix}/lib/krb5/plugins

%files -n %{lib32namesupport}
%{_prefix}/lib/libkrb5support.so.%{support_major}*

%files -n %{lib32namerad}
%{_prefix}/lib/libkrad.so.%{rad_major}*

%files -n %{lib32kadm5clnt_mit}
%{_prefix}/lib/libkadm5clnt_mit.so.%{mit_major}*

%files -n %{lib32kadm5srv_mit}
%{_prefix}/lib/libkadm5srv_mit.so.%{mit_major}*

%files -n %{lib32kdb5}
%{_prefix}/lib/libkdb5.so.%{kdb5_major}*

%if !%{bootstrap}
%files -n %{lib32kdb_ldap}
%{_prefix}/lib/libkdb_ldap.so.%{ldap_major}*
%endif

%files -n %{devel32name}
%{_prefix}/lib/libgssapi_krb5.so
%{_prefix}/lib/libgssrpc.so
%{_prefix}/lib/libk5crypto.so
%{_prefix}/lib/libkadm5clnt.so
%{_prefix}/lib/libkadm5clnt_mit.so
%{_prefix}/lib/libkadm5srv.so
%{_prefix}/lib/libkadm5srv_mit.so
%{_prefix}/lib/libkdb5.so
%{_prefix}/lib/libkrb5.so
%{_prefix}/lib/libkrb5support.so
%{_prefix}/lib/libkrad.so
%{_prefix}/lib/libverto.so
%if !%{bootstrap}
%{_prefix}/lib/libkdb_ldap.so
%endif
%{_prefix}/lib/pkgconfig/*
%endif
