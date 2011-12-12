%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define	major 3
%define	libname	%mklibname %name %major

# enable checking after compile
%define enable_check 0
%{?_with_check: %global %enable_check 1}

Summary:	The Kerberos network authentication system
Name:		krb5
Version:	1.9.2
Release:	2
License:	MIT
URL:		http://web.mit.edu/kerberos/www/
Group:		System/Libraries
# from http://web.mit.edu/kerberos/dist/krb5/1.9/krb5-1.9.2-signed.tar
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc
Source2:	kprop.service
Source4:	kadmin.service
Source5:	krb5kdc.service
Source6:	krb5.conf
Source10:	kdc.conf
Source11:	kadm5.acl
Source19:	krb5kdc.sysconfig
Source20:	kadmin.sysconfig
# The same source files we "check", generated with "krb5-tex-pdf.sh create" and tarred up.
Source23:	krb5-%{version}-pdf.tar.bz2
Source24:	krb5-tex-pdf.sh
Source25:	krb5-1.8-manpaths.txt
Source29:	ksu.pamd
Source30:	kerberos-iv.portreserve
Source31:	kerberos-adm.portreserve
Source32:	krb5_prop.portreserve
Source33:	krb5kdc.logrotate
Source34:	kadmind.logrotate
# stolen from fedora
Patch5:		krb5-1.8-ksu-access.patch
Patch12:	krb5-1.7-ktany.patch
Patch23:	krb5-1.3.1-dns.patch
Patch30:	krb5-1.3.4-send-pr-tempfile.patch
Patch39:	krb5-1.8-api.patch
Patch53:	krb5-1.7-nodeplibs.patch
Patch56:	krb5-1.7-doublelog.patch
Patch59:	krb5-1.8-kpasswd_tcp.patch
Patch60:	krb5-1.8-pam.patch
Patch61:	krb5-1.9-manpaths.patch
Patch71:	krb5-1.9-dirsrv-accountlock.patch
Patch74:	krb5-1.9-buildconf.patch
Patch75:	krb5-1.9-kprop-mktemp.patch
Patch76:	krb5-1.9-ksu-path.patch
Patch78:	http://web.mit.edu/kerberos/advisories/2011-007-patch.txt
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	e2fsprogs-devel
BuildRequires:	flex
BuildRequires:	keyutils-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	systemd-units
BuildRequires:	termcap-devel
%if %enable_check
BuildRequires:	dejagnu
%endif
%if !%bootstrap
BuildRequires:	openldap-devel
%endif

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.

%package -n	%{libname}-devel
Summary:	Development files needed for compiling Kerberos 5 programs
Group:		Development/Other
Requires:	%{libname} >= %{version}
Provides:	krb-devel = %{version}-%{release}
Provides:	krb5-devel = %{version}-%{release}
Provides:	libkrb-devel
Obsoletes:	krb-devel
Obsoletes:	krb5-devel
Obsoletes:	libkrb51-devel
Requires:	rpm-build

%description -n	%{libname}-devel
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.

%package -n	%{libname}
Summary:	The shared libraries used by Kerberos 5
Group:		System/Libraries
Provides:	krb5-libs = %{version}-%{release}
Obsoletes:	krb5-libs
Obsoletes:	libkrb51
# we need the conf file, and better make sure it's a recent version
# for example, previous MIT kerberos versions didn't have ldap support,
# and this is specified in the conf file
Requires:       %{name} >= %{version}-%{release}

%description -n	%{libname}
Kerberos is a network authentication system.  The krb5-libs package
contains the shared libraries needed by Kerberos 5.  If you're using
Kerberos, you'll need to install this package.

%package	server
Summary:	The server programs for Kerberos 5
Group:		System/Servers
Requires:	%{libname} >= %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(post): info-install
Requires(preun): info-install
# systemd-sysv was added in systemd 37-2
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
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
Requires:	%{libname} >= %{version}-%{release}
Requires(post): info-install
Requires(preun): info-install
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Provides:       kerberos-workstation

%description	workstation
Kerberos is a network authentication system.  The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be installed
on every workstation.

%package	pkinit-openssl
Summary:	The PKINIT module for Kerberos 5
Group:		System/Libraries
Requires:	%{libname} >= %{version}-%{release}

%description	pkinit-openssl
Kerberos is a network authentication system. The krb5-pkinit-openssl
package contains the PKINIT plugin, which uses OpenSSL to allow clients
to obtain initial credentials from a KDC using a private key and a
certificate. 

%prep

%setup -q -a 23
%patch60 -p1 -b .pam
%patch61 -p1 -b .manpaths
%patch5 -p1 -b .ksu-access
%patch12 -p1 -b .ktany
%patch23 -p1 -b .dns
%patch30 -p1 -b .send-pr-tempfile
%patch39 -p1 -b .api
%patch53 -p1 -b .nodeplibs
%patch56 -p1 -b .doublelog
%patch59 -p1 -b .kpasswd_tcp
%patch71 -p1 -b .dirsrv-accountlock
%patch74 -p1 -b .buildconf
%patch75 -p1
%patch76 -p1
%patch78 -p1 -b .CVE-2011-1530

gzip doc/*.ps

sed -i -e '1s!\[twoside\]!!;s!%\(\\usepackage{hyperref}\)!\1!' \
    doc/api/library.tex
sed -i -e '1c\
\\documentclass{article}\
\\usepackage{fixunder}\
\\usepackage{functions}\
\\usepackage{fancyheadings}\
\\usepackage{hyperref}' doc/implement/implement.tex

# Take the execute bit off of documentation.
chmod -x doc/krb5-protocol/*.txt doc/*.html doc/*/*.html 

# Rename the man pages so that they'll get generated correctly. Uses the
# "krb5-1.8-manpaths.txt" source file.
pushd src
cat %{SOURCE25} | while read manpage ; do
    mv "$manpage" "$manpage".in
done
popd 

# Check that the PDFs we built earlier match this source tree, using the
# "krb5-tex-pdf.sh" source file.
#sh %{SOURCE24} check << EOF
#doc/api       library krb5
#doc/implement implement
#doc/kadm5     adb-unit-test
#doc/kadm5     api-unit-test
#doc/kadm5     api-funcspec
#doc/kadm5     api-server-design
#EOF

sed -i s,^attributetype:,attributetypes:,g \
    src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif 

pushd src
    autoreconf -fi
popd

%build
%serverbuild

cd src
# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC`"
CPPFLAGS="`echo $DEFINES $INCLUDES`" 

%configure2_5x \
    CC="%{__cc}" \
    CFLAGS="$CFLAGS" \
    CPPFLAGS="$CPPFLAGS" \
    --enable-shared \
    --localstatedir=%{_sysconfdir}/kerberos \
    --without-krb4 \
    --enable-dns-for-realm \
    --enable-pkinit \
    --without-tcl \
    --with-system-et \
    --with-system-ss \
    --disable-static \
    --disable-rpath \
%if !%bootstrap
    --with-ldap \
%endif
    --with-pam

    #--with-netlib=-lresolv

%make

%check
# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_tmppath}

%install
rm -rf %{buildroot}

# Info docs.
install -d %{buildroot}%{_infodir}
install -m 644 doc/*.info* %{buildroot}%{_infodir}

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
    EXAMPLEDIR=%{_docdir}/%{libname}-devel/examples\
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

%post server
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%_install_info krb5-admin.info
%_install_info krb5-install.info
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
%_remove_install_info krb5-admin.info
%_remove_install_info krb5-install.info
exit 0

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart krb5kdc.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart kadmin.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart kprop.service >/dev/null 2>&1 || :
fi

%post workstation
%_install_info krb5-user.info

%preun workstation
%_remove_install_info krb5-user.info

%triggerun server -- krb5-server < 1.9.2-1
# Save the current service runlevel info
# User must manually run 
#  systemd-sysv-convert --apply krb5kdc
#  systemd-sysv-convert --apply kadmin
#  systemd-sysv-convert --apply kprop
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save krb5kdc >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save kadmin >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save kprop >/dev/null 2>&1 ||:

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
%{_mandir}/man1/kerberos.1*
%{_mandir}/man5/.k5login.5*

%files workstation
%doc doc/user*.ps.gz src/config-files/services.append
%doc doc/{kdestroy,kinit,klist,kpasswd,ksu}.html
%doc doc/krb5-user.html 
%attr(0755,root,root) %doc src/config-files/convert-config-files
%{_infodir}/krb5-user.info*
%{_mandir}/man5/krb5.conf.5*

%{_bindir}/kdestroy
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kinit
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

%attr(4755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%config(noreplace) /etc/pam.d/ksu

# Problem-reporting tool
%{_datadir}/gnats
%{_sbindir}/krb5-send-pr
%{_mandir}/man1/krb5-send-pr.1*

%files server
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
%doc doc/admin*.ps.gz
%doc doc/install*.ps.gz
%doc doc/krb5-admin.html
%doc doc/krb5-install.html
%{_infodir}/krb5-admin.info*
%{_infodir}/krb5-install.info*
%dir /var/log/kerberos
%dir %{_sysconfdir}/kerberos/krb5kdc
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kadm5.acl
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%if !%bootstrap
%{_sbindir}/kdb5_ldap_util
%{_mandir}/man8/kdb5_ldap_util.8*
%endif
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/kproplog
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc
%{_mandir}/man8/krb5kdc.8*
%{_sbindir}/sim_server

# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*

%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/authdata

%files -n %{libname}
%{_libdir}/libgssapi_krb5.so.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%{_libdir}/krb5/plugins/preauth/encrypted_challenge.so
%{_libdir}/krb5/plugins/kdb/db2.so 

%files -n %{libname}-devel
%doc doc/api
%doc doc/implement
%doc doc/kadm5
%doc doc/kadmin
%doc doc/krb5-protocol
%doc doc/rpc
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
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*
%{_mandir}/man1/krb5-config.1*

# Protocol test clients
%{_bindir}/sim_client
%{_bindir}/gss-client
%{_bindir}/uuclient

# Protocol test servers
%{_sbindir}/gss-server
%{_sbindir}/uuserver
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*

%files pkinit-openssl
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files server-ldap
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%if !%bootstrap
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_libdir}/libkdb_ldap.so
%{_libdir}/libkdb_ldap.so.*
%{_sbindir}/kdb5_ldap_util
%endif
