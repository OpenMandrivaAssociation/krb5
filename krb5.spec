%bcond_with	crosscompile
%if %{with crosscompile}
%define bootstrap 1
%else
%define bootstrap 0
%endif
%define oname mit-krb5

%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define	major 3
%define	libname	%mklibname %{name}_ %{major}
%define	libk5crypto	%mklibname k5crypto %{major}

%define	support_major 0
%define	libnamesupport	%mklibname %{name}support %{support_major}

%define rad_major 0
%define libnamerad %mklibname krad %{rad_major}

%define	mit_major 9
%define	libkadm5clnt_mit	%mklibname kadm5clnt_mit %{mit_major}
%define	libkadm5srv_mit	%mklibname kadm5srv_mit %{mit_major}

%define	gssapi_major 2
%define	libgssapi_krb5	%mklibname gssapi_%{name}_ %{gssapi_major}

%define	gssrpc_major 4
%define	libgssrpc	%mklibname gssrpc %{gssrpc_major}

%define	kdb5_major 8
%define	libkdb5	%mklibname kdb5_ %{kdb5_major}

%define	ldap_major 1
%define	libkdb_ldap	%mklibname kdb_ldap %{ldap_major}

%define develname	%mklibname -d %{name}
# enable checking after compile
%define enable_check 0
%{?_with_check: %global %enable_check 1}

%bcond_with	selinux

Summary:	The Kerberos network authentication system
Name:		krb5
Version:	1.13.1
Release:	3
License:	MIT
Url:		http://web.mit.edu/kerberos/www/
Group:		System/Libraries
# from http://web.mit.edu/kerberos/dist/krb5/1.9/krb5-1.9.2-signed.tar
Source0:	krb5-%{version}.tar.gz
Source1:	krb5-%{version}.tar.gz.asc
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
Patch6:		krb5-1.12-ksu-path.patch
Patch12:	krb5-1.12-ktany.patch
Patch16:	krb5-1.12-buildconf.patch
Patch23:	krb5-1.3.1-dns.patch
Patch39:	krb5-1.12-api.patch
Patch60:	krb5-1.12.1-pam.patch
Patch63:	krb5-1.10.2-selinux-label.patch
Patch71:	krb5-1.13-dirsrv-accountlock.patch
Patch75:	krb5-pkinit-debug.patch
Patch86:	krb5-1.9-debuginfo.patch
Patch105:	krb5-kvno-230379.patch
Patch107:	krb5-aarch64.patch
Patch108:	krb5-1.12.2-python3.patch
Patch109:	krb5-1.13.1-warning.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	diffutils
BuildRequires:	libtool
BuildRequires:	systemd-units
BuildRequires:	keyutils-devel
BuildRequires:	pam-devel
%if %{with selinux}
BuildRequires:	selinux-devel
%endif
BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(com_err)
BuildRequires:	pkgconfig(libverto)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	texlive
BuildRequires:	texlive-latex-bin
%if %enable_check
BuildRequires:	dejagnu
%endif
%if !%{bootstrap}
BuildRequires:	openldap-devel
%endif
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.

%package -n	%{develname}
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
%if !%{bootstrap}
Requires:	%{libkdb_ldap} >= %{version}
%endif
Provides:	krb5-devel = %{version}-%{release}
Obsoletes:	%{_lib}krb53-devel
Requires:	rpm-build

%description -n	%{develname}
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.

%package -n	%{libname}
Summary:	The shared library used by Kerberos 5
Group:		System/Libraries
Obsoletes:	%{_lib}krb53
%rename	krb5-libs

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	%{libgssapi_krb5}
Summary:	The shared library used by Kerberos 5 - gssapi_krb5
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libgssapi_krb5}
This package contains the shared library gssrpc for %{name}.

%package -n	%{libgssrpc}
Summary:	The shared library used by Kerberos 5 - gssrpc
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libgssrpc}
This package contains the shared library gssrpc for %{name}.

%package -n	%{libk5crypto}
Summary:	The shared library used by Kerberos 5 - k5crypto
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libk5crypto}
This package contains the shared library k5crypto for %{name}.

%package -n	%{libnamesupport}
Summary:	The shared library used by Kerberos 5 - krb5support
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libnamesupport}
This package contains the shared library krb5support for %{name}.

%package -n     %{libnamerad}
Summary:        The shared library used by Kerberos 5 - krad
Group:          System/Libraries
Conflicts:      %{_lib}krb53 < 1.9.2-3

%description -n %{libnamerad}
This package contains the shared library krad for %{name}.

%package -n	%{libkadm5clnt_mit}
Summary:	The shared library used by Kerberos 5 - kadm5clnt_mit
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libkadm5clnt_mit}
This package contains the shared library kadm5clnt_mit for %{name}.

%package -n	%{libkadm5srv_mit}
Summary:	The shared library used by Kerberos 5 - kadm5srv_mit
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libkadm5srv_mit}
This package contains the shared library kadm5srv_mit for %{name}.

%package -n	%{libkdb5}
Summary:	The shared library used by Kerberos 5 - kdb5
Group:		System/Libraries
Conflicts:	%{_lib}krb53 < 1.9.2-3

%description -n	%{libkdb5}
This package contains the shared library kdb5 for %{name}.

%package -n	%{libkdb_ldap}
Summary:	The shared library used by Kerberos 5 - kdb_ldap
Group:		System/Libraries
Conflicts:	krb5-server-ldap < 1.9.2-3

%description -n	%{libkdb_ldap}
This package contains the shared library kdb_ldap for %{name}.

%package	server
Summary:	The server programs for Kerberos 5
Group:		System/Servers
Requires(post,preun): rpm-helper
Requires(post,preun,postun): systemd-units
# we drop files in its directory, but we don't want to own that directory
Requires:	logrotate
# mktemp is used by krb5-send-pr
Requires:	mktemp
# portreserve is used by init scripts for kadmind, kpropd, and krb5kdc
Requires:	portreserve

%description	server
Kerberos is a network authentication system.  The krb5-server package
contains the programs that must be installed on a Kerberos 5 server.
If you're installing a Kerberos 5 server, you need to install this
package (in other words, most people should NOT install this
package).

%package	server-ldap
Summary:	The LDAP storage plugin for the Kerberos 5 KDC
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	server-ldap
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC). If you are installing a Kerberos 5 KDC,
and you wish to use a directory server to store the data for your
realm, you need to install this package. 

%package	workstation
Summary:	Kerberos 5 programs for use on workstations
Group:		System/Base
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Provides:	kerberos-workstation

%description	workstation
Kerberos is a network authentication system.  The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be installed
on every workstation.

%package	pkinit-openssl
Summary:	The PKINIT module for Kerberos 5
Group:		System/Libraries

%description	pkinit-openssl
Kerberos is a network authentication system. The krb5-pkinit-openssl
package contains the PKINIT plugin, which uses OpenSSL to allow clients
to obtain initial credentials from a KDC using a private key and a
certificate. 

%prep
%setup -q -a 23 -n krb5-%{version}
ln -s NOTICE LICENSE

%patch60 -p1 -b .pam

%if %{with selinux}
%patch63 -p1 -b .selinux-label
%endif

#patch5  -p1 -b .ksu-access
%patch6  -p1 -b .ksu-path
%patch12 -p1 -b .ktany
%patch16 -p1 -b .buildconf
%patch23 -p1 -b .dns
%patch39 -p1 -b .api
%patch71 -p1 -b .dirsrv-accountlock
#patch75 -p1 -b .pkinit-debug
%patch86 -p0 -b .debuginfo
%patch105 -p1 -b .kvno
#patch107 -p1 -b .aarch64
%patch108 -p1 -b .py3
%patch109 -p1 -b .warn

# Take the execute bit off of documentation.
chmod -x doc/krb5-protocol/*.txt 

sed -i s,^attributetype:,attributetypes:,g \
    src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif 


%build
pushd src
    autoreconf -fi
popd
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
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's|-fPIE||g'`

pushd src
# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC`"
CPPFLAGS="`echo $DEFINES $INCLUDES`"

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
%if !%{bootstrap}
	--with-ldap \
%endif
	--with-pam

	#--with-netlib=-lresolv

%make
popd

# Build the docs.
make -C src/doc paths.py version.py
cp src/doc/paths.py doc/
mkdir -p build-man build-html build-pdf
sphinx-build -a -b man   -t pathsubs doc build-man
sphinx-build -a -b html  -t pathsubs doc build-html
rm -fr build-html/_sources
sphinx-build -a -b latex -t pathsubs doc build-pdf
make -C build-pdf


%check
# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_tmppath}

%install

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
make -C src \
    DESTDIR=%{buildroot} \
    EXAMPLEDIR=%{_docdir}/%{develname}/examples\
    install

# logdir
install -d %{buildroot}/var/log/kerberos

# clear the LDFLAGS
perl -pi -e "s|^LDFLAGS.*|LDFLAGS=''|g" %{buildroot}%{_bindir}/krb5-config


# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/krb5-config

%multiarch_includes %{buildroot}%{_includedir}/gssapi/gssapi.h

# (gb) this one could be fixed differently and properly using <stdint.h>

%multiarch_includes %{buildroot}%{_includedir}/gssrpc/types.h

%multiarch_includes %{buildroot}%{_includedir}/krb5.h

# Install processed man pages.
for section in 1 5 8; do
	install -m 644 build-man/*.$section %{buildroot}%{_mandir}/man$section/
done

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


%files
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
%{_libdir}/krb5/plugins/kdb/db2.so 
%{_libdir}/krb5/plugins/tls/k5tls.so
%{_datadir}/locale/en_US/LC_MESSAGES/mit-krb5.mo

%files workstation
%doc src/config-files/services.append
%doc build-html/*
%doc build-pdf/user.pdf build-pdf/basic.pdf
%attr(0755,root,root) %doc src/config-files/convert-config-files
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
%doc build-pdf/admin.pdf build-pdf/build.pdf
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
%doc build-pdf/appdev.pdf build-pdf/plugindev.pdf
%doc doc/krb5-protocol
%{_includedir}/*.h
%{_includedir}/gssapi
%{_includedir}/gssrpc
%{_includedir}/kadm5
%{_includedir}/krb5
%dir %{multiarch_includedir}/gssapi
%{multiarch_includedir}/gssapi/gssapi.h
%dir %{multiarch_includedir}/gssrpc
%{multiarch_includedir}/gssrpc/types.h
%{multiarch_includedir}/krb5.h
%{_bindir}/krb5-config
%{multiarch_bindir}/krb5-config
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
%if !%{bootstrap}
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_sbindir}/kdb5_ldap_util
%{_mandir}/man8/kdb5_ldap_util.8*
%endif

