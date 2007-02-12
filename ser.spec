#
# Conditional build:
%bcond_without	shm_mmap	# Don't use mmap() on SHM. Neccesary for kernel v2.2.
#
Summary:	SIP proxy, redirect and registrar server
Summary(pl.UTF-8):   Serwer SIP rejestrujący, przekierowujący i robiący proxy
Name:		ser
Version:	0.8.10
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://ftp.berlios.de/pub/ser/%{version}/src/%{name}-%{version}_src.tar.gz
# Source0-md5:	a3a06a9bc15f82321a6d9bc31d582c33
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-paths.patch
Patch1:		%{name}-shm.patch
Patch2:		%{name}-bison.patch
URL:		http://www.iptel.org/ser/
BuildRequires:	bison
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	mysql-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SIP Express Router (ser) is a high-performance, configurable, free SIP
(RFC 3261) server. It can act as registrar, proxy or redirect server.
SER features an application-server interface, presence support, SMS
gateway, SIMPLE2Jabber gateway, RADIUS/syslog accounting and
authorization, server status monitoring, FCP security, etc. Web-based
user provisioning, serweb, available. Its performance allows it to
deal with operational burdens, such as broken network components,
attacks, power-up reboots and rapidly growing user population. SER's
configuration ability meets needs of a whole range of scenarios
including small-office use, enterprise PBX replacements and carrier
services.

%description -l pl.UTF-8
SIP Express Router (ser) to wysoko wydajny, konfigurowalny, darmowy
serwer SIP (RFC 3261). Może działać jako serwer rejestrujący, proxy
lub przekierowujący. Możliwości SER-a obejmują interfejs serwera
aplikacji, obsługę obecności, bramkę SMS, bramkę SIMPLE2Jabber,
rozliczanie przez RADIUS/syslog oraz autoryzację, monitorowanie stanu
serwera, bezpieczeństwo FCP itp. Jest dostępny oparty na WWW serwer
opiekujący się użytkownikami - serweb. Wydajność pozwala na raczenie
sobie z obciążeniem operacyjnym, takim jak uszkodzone elementy sieci,
ataki, zaniki zasilania i szybko rosnące grono użytkowników.
Możliwości konfiguracyjne SER-a zaspokajają potrzeby w szerokim
zakresie scenariuszy włącznie z użyciem w małych biurach,
zastępowaniem poważnych PBX-ów i usług transportowych.

%package mysql
Summary:	SER MySQL module
Summary(pl.UTF-8):   Moduł MySQL do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mysql
MySQL module for SER.

%description mysql -l pl.UTF-8
Moduł MySQL do SER.

%package jabber
Summary:	SER Jabber module
Summary(pl.UTF-8):   Moduł Jabber do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description jabber
Jabber module for SER.

%description jabber -l pl.UTF-8
Moduł Jabber do SER.

%prep
%setup -q
%patch0 -p1
%{!?with_shm_mmap:%patch1 -p1}
%patch2 -p1

%build
%{__make} all \
	PREFIX="%{_prefix}" \
	CFLAGS="%{rpmcflags} -Wcast-align"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{ser,sysconfig,rc.d/init.d}

find . -name CVS -0 | xargs -0 rm -rf

%{__make} install \
	PREFIX="%{_prefix}" \
	basedir=$RPM_BUILD_ROOT

for i in modules/*; do \
	[ -f modules/$i/README ] && cp -f modules/$i/README README.$i; \
done

#cd doc/serdev
#docbook2html serdev.sgml
#rm -f serdev.sgml
#cd ../seruser
#docbook2html seruser.sgml
#rm -f seruser.sgml
#cd ../..

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ser
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ser

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ser
if [ -f /var/lock/subsys/ser ]; then
	etc/rc.d/init.d/ser restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ser start\" to start sip Daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ser ]; then
		/etc/rc.d/init.d/ser stop 1>&2
fi
	/sbin/chkconfig --del ser
fi

%files
%defattr(644,root,root,755)
%doc README* ISSUES TODO doc/ser* scripts examples
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/ser
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ser/ser.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ser
%attr(754,root,root) /etc/rc.d/init.d/ser
%dir %{_libdir}/ser
%dir %{_libdir}/ser/modules
%attr(755,root,root) %{_libdir}/ser/modules/acc.so
%attr(755,root,root) %{_libdir}/ser/modules/auth.so
%attr(755,root,root) %{_libdir}/ser/modules/exec.so
%attr(755,root,root) %{_libdir}/ser/modules/im.so
%attr(755,root,root) %{_libdir}/ser/modules/maxfwd.so
%attr(755,root,root) %{_libdir}/ser/modules/msilo.so
%attr(755,root,root) %{_libdir}/ser/modules/pike.so
%attr(755,root,root) %{_libdir}/ser/modules/print.so
%attr(755,root,root) %{_libdir}/ser/modules/registrar.so
%attr(755,root,root) %{_libdir}/ser/modules/rr.so
%attr(755,root,root) %{_libdir}/ser/modules/sl.so
%attr(755,root,root) %{_libdir}/ser/modules/sms.so
%attr(755,root,root) %{_libdir}/ser/modules/textops.so
%attr(755,root,root) %{_libdir}/ser/modules/tm.so
%attr(755,root,root) %{_libdir}/ser/modules/usrloc.so
%{_mandir}/man*/*

%files jabber
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/jabber.so

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/mysql.so
