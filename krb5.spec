%define	name	krb5
%define version 1.6.3
%define rel	15
%define release %mkrel %rel

%define	major	3
%define	libname	%mklibname %name %major

# enable checking after compile
%define enable_check 0
%{?_with_check: %global %enable_check 1}

%define with_krb4 0

Summary:	The Kerberos network authentication system
Name:		%{name}
Version:	%{version}
Release:	%{release}
# from http://web.mit.edu/kerberos/dist/krb5/1.4/krb5-1.4.1-signed.tar
Source0:	%{name}-%{version}.tar.gz
Source1:	kpropd.init
Source2:	krb524d.init
Source3:	kadmind.init
Source4:	krb5kdc.init
Source5:	krb5.conf
Source6:	krb5.sh
Source7:	krb5.csh
Source8:	kdcrotate
Source9:	kdc.conf
Source10:	kadm5.acl
Source11:	krsh
Source12:	krlogin
Source13:	eklogin.xinetd
Source14:	klogin.xinetd
Source15:	kshell.xinetd
Source16:	telnet-krb5.xinetd
Source17:	ftp-krb5.xinetd
Source18:	krb5server.init
Source19:	statglue.c
Source20:	telnet.16.xpm
Source21:	telnet.32.xpm
Source22:	telnet.48.xpm
Source23:	Mandriva-Kerberos-HOWTO.html
Source24:	%{name}-%{version}.tar.gz.asc
Source25:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.tar.gz
Source26:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.sig
Source27:	krb5-ldap.conf.sample
Source28:	usr.bin.telnet.apparmor
Patch0:		krb5-1.2.2-telnetbanner.patch
Patch1:		krb5-1.2.5-biarch-utmp.patch
Patch4:		krb5-1.3-no-rpath.patch
Patch5:		krb5-1.6.3-fix-link.patch
# stolen from fedora
Patch6:		krb5-1.3-large-file.patch
Patch7:		krb5-1.5.1-ksu-path.patch
Patch8:		krb5-1.3-ksu-access.patch
Patch9:		krb5-1.3-pass-by-address.patch
Patch10:	krb5-1.3-netkit-rsh.patch
Patch13:	krb5-1.3-ftp-glob.patch
Patch19:	krb5-1.3.3-rcp-sendlarge.patch
Patch20:	krb5-1.7-openssl-1.0.patch
# (gb) preserve file names when generating files from *.et (multiarch fixes)
Patch23:	krb5-1.3.6-et-preserve-file-names.patch
# http://qa.mandriva.com/show_bug.cgi?id=9410
Patch24:	krb5-1.4.1-ftplfs.patch
Patch25:	krb5-1.6.1-rh-CVE-2007-5901.patch
Patch26:	krb5-1.6.1-rh-CVE-2007-5971.patch
Patch27:	krb5-1.6.1-rh-CVE-2008-0062_0063.patch
Patch28:	krb5-1.6.1-rh-CVE-2008-0947.patch
Patch29:	krb5-1.6.3-tcl86.patch
Patch30:	krb5-1.6.3-CVE-2009-0844-0845-2.patch
Patch31:	krb5-1.6.3-fix-format-errors.patch
Patch32:	krb5-1.6.3-CVE-2009-0846.patch
Patch33:	krb5-1.6.3-CVE-2009-0847.patch
Patch34:	krb5-1.6.3-CVE-2009-4212.diff
Patch35:	krb5-1.6.2-CVE-2010-0629.diff
License:	MIT
URL:		http://web.mit.edu/kerberos/www/
Group:		System/Libraries
# we moved some files from the lib package to this one, see
# http://qa.mandriva.com/show_bug.cgi?id=32580
Conflicts:      %{libname} <= 1.6.2-4mdv2008.0
# (anssi) biarch conflicts as well:
Conflicts:	libkrb53 <= 1.6.2-4mdv2008.0
Requires(pre):	info-install
Requires:	info-install
BuildRequires:	bison flex termcap-devel texinfo e2fsprogs-devel
BuildRequires:	tcl tcl-devel chrpath
%if %enable_check
BuildRequires:	dejagnu
%endif
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	openldap-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.

%package -n	%{libname}-devel
Summary:	Development files needed for compiling Kerberos 5 programs
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	krb-devel = %{version}-%{release}
Provides:	krb5-devel = %{version}-%{release}
Provides:	libkrb-devel
Obsoletes:	krb-devel 
Obsoletes:	krb5-devel
Obsoletes:	libkrb51-devel

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
Requires:       %{name} >= %{version}

%description -n	%{libname}
Kerberos is a network authentication system.  The krb5-libs package
contains the shared libraries needed by Kerberos 5.  If you're using
Kerberos, you'll need to install this package.

%package	server
Group:		System/Servers
Summary:	The server programs for Kerberos 5
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name}-workstation = %{version}-%{release}
Requires:	words
Requires(pre):	info-install
Requires:	info-install

%description	server
Kerberos is a network authentication system.  The krb5-server package
contains the programs that must be installed on a Kerberos 5 server.
If you're installing a Kerberos 5 server, you need to install this
package (in other words, most people should NOT install this
package).

%package	workstation
Summary:	Kerberos 5 programs for use on workstations
Group:		System/Base
Requires:	%{libname} = %{version}-%{release}
Requires(pre):	info-install
Requires:	info-install
Provides:       kerberos-workstation
Conflicts:	rsh <= 0.17-12mdk

%description	workstation
Kerberos is a network authentication system.  The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be installed
on every workstation.

%package -n	telnet-server-krb5
Summary:	A telnet-server with kerberos support
Group:		Networking/Remote access
Requires:	%{libname} = %{version}-%{release}
Requires:	xinetd
Obsoletes:	telnet-server
Provides:	telnet-server

%description -n	telnet-server-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet-server package provides a telnet daemon, which will support remote
logins into the host machine. The telnet daemon is enabled by default. You may
disable the telnet daemon by editing /etc/inetd.conf.

Install the telnet-server package if you want to support remote logins to your
machine.

This version supports kerberos authentication.

%package -n	telnet-client-krb5
Summary:	A telnet-client with kerberos support
Group:		Networking/Remote access
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	telnet
Provides:	telnet
 
%description -n	telnet-client-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet package provides a command line telnet client.

Install the telnet package if you want to telnet to remote machines.

This version supports kerberos authentication.

%package -n	ftp-client-krb5
Summary:	A ftp-client with kerberos support
Group:		Networking/File transfer
Requires:	%{libname} = %{version}
Obsoletes:	ftp
Provides:	ftp

%description -n	ftp-client-krb5
The ftp package provides the standard UNIX command-line FTP client.
FTP is the file transfer protocol, which is a widely used Internet
protocol for transferring files and for archiving files.

If your system is on a network, you should install ftp in order to do
file transfers.

This version supports kerberos authentication.

%package -n	ftp-server-krb5
Summary:	A ftp-server with kerberos support
Group:		Networking/File transfer
Requires:	%{libname} = %{version}
Provides:	ftpserver

%description -n	ftp-server-krb5
The ftp-server package provides an ftp server.

This version supports kerberos authentication.

%prep
%setup -q -a 25
%patch0 -p1 -b .banner
%patch1 -p1 -b .biarch-utmp
%patch4 -p0 -b .no-rpath
%patch5 -p0 -b .link
%patch6 -p1 -b .large-file
%patch7 -p1 -b .ksu-path
%patch8 -p1 -b .ksu-access
%patch9 -p1 -b .pass-by-address
%patch10 -p1 -b .netkit-rsh
%patch13 -p1 -b .ftp-glob
%patch19 -p1 -b .rcp-sendlarge
%patch20 -p0 -b .openssl
%patch23 -p1 -b .et-preserve-file-names
%patch24 -p1 -b .lfs
%patch25 -p0 -b .cve-2007-5901
%patch26 -p0 -b .cve-2007-5971
%patch27 -p0 -b .cve-2008-0062_0063
%patch28 -p1 -b .cve-2008-0947
%patch29 -p1 -b .tcl86
%patch30 -p1 -b .CVE-2009-0844_0845
%patch31 -p1 -b .format
%patch32 -p1 -b .CVE-2009-0846
%patch33 -p1 -b .CVE-2009-0847
%patch34 -p1 -b .CVE-2009-4212
%patch35 -p1 -b .CVE-2010-0629

# krb5-ldap.conf.sample
install -m 0644 %{SOURCE27} .

find . -type f -name "*.fixinfo" -exec rm -fv "{}" ";"
gzip doc/*.ps

find -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

%build
%serverbuild
export CFLAGS="$CFLAGS -I/usr/include/et"
find . -name "*.[ch]"|xargs grep -r -l "^extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;|#include <errno.h>|"
find . -name "*.[ch]"|xargs grep -r -l "extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;||"

cd src
%{?__cputoolize: %{__cputoolize} -c config}

DEFINES="-D_FILE_OFFSET_BITS=64" ; export DEFINES
%configure2_5x \
	--localstatedir=%{_sysconfdir}/kerberos \
%if %{with_krb4}
	--with-krb4 \
%else
	--without-krb4 \
%endif
	--enable-dns-for-realm \
	--with-tcl=%{_prefix} \
	--with-system-et \
	--with-system-ss \
	--enable-shared   \
	--disable-static  \
	--with-ldap

%make

# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_tmppath}

%install
rm -rf %{buildroot}
pushd src
%makeinstall_std
popd

# Our shell scripts.
install -d %{buildroot}%{_bindir}
install -m 0755 %{SOURCE11} %{buildroot}%{_bindir}/krsh
install -m 0755 %{SOURCE12} %{buildroot}%{_bindir}/krlogin

# Extra headers.
install -d %{buildroot}%{_includedir}
pushd src/include
	find kadm5 krb5 gssrpc gssapi -name "*.h" | cpio -pdm  %{buildroot}%{_includedir}
popd
perl -pi -e 's#k5-int#krb5/kdb#g' %{buildroot}%{_includedir}/kadm5/admin.h
find %{buildroot}%{_includedir} -type d | xargs chmod 755
find %{buildroot}%{_includedir} -type f | xargs chmod 644

# logdir
install -d %{buildroot}/var/log/kerberos

# Info docs.
install -d %{buildroot}%{_infodir}
install -m 644 doc/*.info* %{buildroot}%{_infodir}/
%if ! %{with_krb4}
rm -f %{buildroot}%{_infodir}/krb425.info*
%endif

# KDC config files.
install -d %{buildroot}%{_sysconfdir}/kerberos/krb5kdc
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kdc.conf
install -m 0600 %{SOURCE10} %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

# Client config files and scripts.
install -d %{buildroot}/etc/profile.d
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/krb5.conf
install -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/profile.d/krb5.sh
install -m 0755 %{SOURCE7} %{buildroot}%{_sysconfdir}/profile.d/krb5.csh

# KDC init script.
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE4} %{buildroot}%{_initrddir}/krb5kdc
install -m 0755 %{SOURCE3} %{buildroot}%{_initrddir}/kadmin
install -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/kprop
%if %{with_krb4}
install -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/krb524
%endif
install -m 0755 %{SOURCE8} %{buildroot}%{_sbindir}/kdcrotate
install -m 0755 %{SOURCE18} %{buildroot}%{_initrddir}/krb5server

# fix some permissions
chmod 755 %{buildroot}%{_libdir}/*.so*
find %{buildroot}%{_includedir} -type d | xargs chmod 755
find %{buildroot}%{_includedir} -type f | xargs chmod 644

# Xinetd configuration files.
install -d %{buildroot}%{_sysconfdir}/xinetd.d/
install -m 0644 %{SOURCE16} %{buildroot}%{_sysconfdir}/xinetd.d/telnet
install -m 0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/xinetd.d/ftp
install -m 0644 %{SOURCE23} doc/Mandrake-Kerberos-HOWTO.html

# Rename rsh, rlogin and rcp to not conflict with those provided by netkit
for i in rcp rlogin rsh; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i.krb5
    mv %{buildroot}%{_mandir}/man1/$i.1 %{buildroot}%{_mandir}/man1/$i.krb5.1
done

# dump un-FHS examples location (files included in doc list now)
rm -Rf %{buildroot}/%{_datadir}/examples

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/krb5-config
%multiarch_includes %{buildroot}%{_includedir}/gssapi/gssapi.h
# (gb) this one could be fixed differently and properly using <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/gssrpc/types.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/k5-config.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/autoconf.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/osconf.h
%multiarch_includes %{buildroot}%{_includedir}/krb5.h

%if ! %{with_krb4}
rm -rf %{buildroot}%{_includedir}/kerberosIV
%endif

# install missing manpage
mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 src/plugins/kdb/ldap/ldap_util/kdb5_ldap_util.M \
	%{buildroot}%{_mandir}/man8/kdb5_ldap_util.8

# apparmor profile(s)
mkdir -p %{buildroot}%{_sysconfdir}/apparmor.d
install -m 0644 %{SOURCE28} %{buildroot}%{_sysconfdir}/apparmor.d/usr.bin.telnet

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post server
# Remove the init script for older servers.
[ -x /etc/rc.d/init.d/krb5server ] && /sbin/chkconfig --del krb5server
# Install the new ones.
/sbin/chkconfig --add krb5kdc
/sbin/chkconfig --add kadmin
%if %{with_krb4}
/sbin/chkconfig --add krb524
%_install_info krb425.info
%endif
/sbin/chkconfig --add kprop
%_install_info krb5-admin.info
%_install_info krb5-install.info

%preun server
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del krb5kdc
	/sbin/chkconfig --del kadmin
%if %{with_krb4}
	/sbin/chkconfig --del krb524
	/sbin/service krb524 stop > /dev/null 2>&1 || :
%endif
	/sbin/chkconfig --del kprop
	/sbin/service krb5kdc stop > /dev/null 2>&1 || :
	/sbin/service kadmin stop > /dev/null 2>&1 || :
	/sbin/service kprop stop > /dev/null 2>&1 || :
fi
%if %{with_krb4}
%_remove_install_info krb425.info
%endif
%_remove_install_info krb5-admin.info
%_remove_install_info krb5-install.info

%postun server
if [ "$1" -ge 1 ] ; then
	/sbin/service krb5kdc condrestart > /dev/null 2>&1 || :
%if %{with_krb4}
	/sbin/service krb524 condrestart > /dev/null 2>&1 || :
%endif
	/sbin/service kadmin condrestart > /dev/null 2>&1 || :
	/sbin/service kprop condrestart > /dev/null 2>&1 || :
fi

%post workstation
%_install_info krb5-user.info
/sbin/service xinetd reload > /dev/null 2>&1 || :

%{_sbindir}/update-alternatives \
	--install %{_bindir}/rcp rcp %{_bindir}/rcp.krb5 20 \
	--slave %{_mandir}/man1/rcp.1%{_extension} man-rcp %{_mandir}/man1/rcp.krb5.1%{_extension}

%{_sbindir}/update-alternatives \
	--install %{_bindir}/rlogin rlogin %{_bindir}/rlogin.krb5 20 \
	--slave %{_mandir}/man1/rlogin.1%{_extension} man-rlogin %{_mandir}/man1/rlogin.krb5.1%{_extension}

%{_sbindir}/update-alternatives \
	--install %{_bindir}/rsh rsh %{_bindir}/rsh.krb5 20 \
	--slave %{_mandir}/man1/rsh.1%{_extension} man-rsh %{_mandir}/man1/rsh.krb5.1%{_extension}


%preun workstation
%_remove_install_info krb5-user.info
if [ $1 -eq 0 ]; then
  %{_sbindir}/update-alternatives --remove rcp %{_bindir}/rcp.krb5
  %{_sbindir}/update-alternatives --remove rlogin %{_bindir}/rlogin.krb5
  %{_sbindir}/update-alternatives --remove rsh %{_bindir}/rsh.krb5
fi

%postun workstation
/sbin/service xinetd reload > /dev/null 2>&1 || :

%triggerpostun workstation -- %{name}-workstation <= 1.3-4mdk
if [ ! -f %{_bindir}/rcp ]; then
  %{_sbindir}/update-alternatives \
	  	--install %{_bindir}/rcp rcp %{_bindir}/rcp.krb5 20 \
		--slave %{_mandir}/man1/rcp.1%{_extension} man-rcp %{_mandir}/man1/rcp.krb5.1%{_extension}

  %{_sbindir}/update-alternatives \
	  	--install %{_bindir}/rlogin rlogin %{_bindir}/rlogin.krb5 20 \
		--slave %{_mandir}/man1/rlogin.1%{_extension} man-rlogin %{_mandir}/man1/rlogin.krb5.1%{_extension}

	%{_sbindir}/update-alternatives \
		--install %{_bindir}/rsh rsh %{_bindir}/rsh.krb5 20 \
		--slave %{_mandir}/man1/rsh.1%{_extension} man-rsh %{_mandir}/man1/rsh.krb5.1%{_extension}
fi

%post -n telnet-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
ln -sf /bin/login /usr/sbin/login.krb5
file="/etc/xinetd.d/telnet"
if [ ! -f $file ] ; then
	echo "Can't find xinetd file for telnet."
	exit 0
fi
perl -pi -e "s|/usr/sbin/in\.telnetd|/usr/sbin/telnetd|g" $file
# We already have the required flags (-a <some_auth_mode>)
cat $file|egrep -q "server_args.*=.*-a[[:space:]]+.*$" && exit 0
# Don't have -a <some_auth_mode>, check if we have server_args or not
cat $file|egrep -q "server_args.*=.*$" && \
	perl -pi -e "s|(server_args.*=.*$)|\1\ -a\ none|" $file && exit 0
# Say, no server_args in xinetd file.
perl -pi -e "s|(server.*=.*/usr/sbin/telnetd.*$)|\1\n\tserver_args\t=\ -a\ none|" $file && exit 0

%postun -n telnet-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :

%post -n ftp-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
ln -sf /bin/login /usr/sbin/login.krb5
file="/etc/xinetd.d/ftp"
if [ ! -f $file ] ; then
	echo "Can't find xinetd file for ftp."
	exit 0
fi

%postun -n ftp-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :

%posttrans -n telnet-client-krb5
# if we have apparmor installed, reload if it's being used
if [ -x /sbin/apparmor_parser ]; then
        /sbin/service apparmor condreload
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/krb5.conf
%dir %{_sysconfdir}/kerberos
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins

%files workstation
%defattr(-,root,root)
%attr(0755,root,root) %config(noreplace) /etc/profile.d/krb5.sh
%attr(0755,root,root) %config(noreplace) /etc/profile.d/krb5.csh
%doc doc/*.html doc/user*.ps.gz src/config-files/services.append
%doc src/config-files/krb5.conf
%attr(0755,root,root) %doc src/config-files/convert-config-files
%{_infodir}/krb5-user.info*
%{_bindir}/gss-client
%{_bindir}/kdestroy
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kerberos.1*
%{_bindir}/kinit
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_mandir}/man1/kpasswd.1*
%if %{with_krb4}
%{_bindir}/krb524init
%attr(0755,root,root) %{_bindir}/v4rcp
%{_mandir}/man1/v4rcp.1*
%endif
%{_sbindir}/kadmin
%{_mandir}/man8/kadmin.8*
%{_sbindir}/ktutil
%{_mandir}/man8/ktutil.8*
%attr(0755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%{_bindir}/kvno
%{_mandir}/man1/kvno.1*
%{_bindir}/rcp.krb5
%{_mandir}/man1/rcp.krb5.1*
%attr(0755,root,root) %{_bindir}/krlogin
%{_bindir}/rlogin.krb5
%{_mandir}/man1/rlogin.krb5.1*
%attr(0755,root,root) %{_bindir}/krsh
%{_bindir}/rsh.krb5
%{_mandir}/man1/rsh.krb5.1*
%{_mandir}/man1/tmac.doc*
#%{_bindir}/v5passwd
#%{_mandir}/man1/v5passwd.1*
%{_bindir}/sim_client
%{_bindir}/uuclient
%{_sbindir}/login.krb5
%{_mandir}/man8/login.krb5.8*
%{_sbindir}/gss-server
%{_sbindir}/klogind
%{_mandir}/man8/klogind.8*
%{_sbindir}/krb5-send-pr
%{_mandir}/man1/krb5-send-pr.1*
%{_sbindir}/kshd
%{_mandir}/man8/kshd.8*
%{_sbindir}/uuserver
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/krb5kdc
%attr(0755,root,root) %{_initrddir}/kadmin
%if %{with_krb4}
%attr(0755,root,root) %{_initrddir}/krb524
%endif
%attr(0755,root,root) %{_initrddir}/kprop
%attr(0755,root,root) %{_initrddir}/krb5server
%doc doc/admin*.ps.gz doc/*html
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%if %{with_krb4}
%doc doc/krb425*.ps.gz 
%{_infodir}/krb425.info*
%endif
%doc krb5-ldap.conf.sample
%doc doc/install*.ps.gz
%doc src/config-files/kdc.conf
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
#%{_sbindir}/kadmind4
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kdb5_ldap_util
%{_mandir}/man8/kdb5_ldap_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%if %{with_krb4}
%{_sbindir}/krb524d
%{_mandir}/man8/krb524d.8*
%endif
%{_sbindir}/krb5kdc
%{_mandir}/man8/k5srvutil.8*
%{_sbindir}/k5srvutil
%{_mandir}/man8/krb5kdc.8*
%{_sbindir}/sim_server
#%{_sbindir}/v5passwdd
# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*
%attr(0755,root,root) %{_sbindir}/kdcrotate
%{_datadir}/gnats/mit
%dir %{_libdir}/krb5/plugins/kdb
%{_libdir}/krb5/plugins/kdb/db2.so
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/api
%doc doc/implement
%doc doc/kadm5
%doc doc/kadmin
%doc doc/krb5-protocol
%doc doc/rpc
%multiarch %{multiarch_bindir}/krb5-config
%multiarch %{multiarch_includedir}/gssapi/gssapi.h
%multiarch %{multiarch_includedir}/gssrpc/types.h
# multiarch %{multiarch_includedir}/krb5/k5-config.h
#multiarch %{multiarch_includedir}/krb5/autoconf.h
#multiarch %{multiarch_includedir}/krb5/osconf.h
%multiarch %{multiarch_includedir}/krb5.h
%{_includedir}/*.h
%{_includedir}/gssapi
%{_includedir}/gssrpc
%{_includedir}/kadm5
%{_includedir}/krb5
%{_bindir}/krb5-config
%{_libdir}/lib*.so
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*
%{_mandir}/man1/krb5-config.1*

%files -n telnet-server-krb5
%defattr(-,root,root)
%config(noreplace) /etc/xinetd.d/telnet
%{_sbindir}/telnetd
%{_mandir}/man8/telnetd.8*

%files -n telnet-client-krb5
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apparmor.d/usr.bin.telnet
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*

%files -n ftp-client-krb5
%defattr(-,root,root)
%{_bindir}/ftp
%{_mandir}/man1/ftp.1*

%files -n ftp-server-krb5
%defattr(-,root,root)
%config(noreplace) /etc/xinetd.d/ftp
%{_sbindir}/ftpd
%{_mandir}/man8/ftpd.8*
