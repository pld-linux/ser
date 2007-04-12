Summary:	SIP proxy, redirect and registrar server
Summary(pl.UTF-8):	Serwer SIP rejestrujący, przekierowujący i robiący proxy
Name:		ser
Version:	0.9.6
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://ftp.iptel.org/pub/ser/%{version}/src/%{name}-%{version}_src.tar.gz
# Source0-md5:	31031225d483c0d5ac43e8eb5d0428e0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-paths.patch
Patch1:		%{name}-shm.patch
URL:		http://www.iptel.org/ser/
BuildRequires:	bison
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	libpqxx-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	radiusclient-ng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# cpl - build fails
# extcmd -  build fails
%define exclude_modules cpl extcmd

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
Summary(pl.UTF-8):	Moduł MySQL do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mysql
MySQL module for SER.

%description mysql -l pl.UTF-8
Moduł MySQL do SER.

%package postgres
Summary:	SER PostgreSQL module
Summary(pl.UTF-8):	Moduł PostgreSQL do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description postgres
PostgreSQL module for SER.

%description postgres -l pl.UTF-8
Moduł PostgreSQL do SER.

%package radius
Summary:	SER Radius module
Summary(pl.UTF-8):	Moduł Radius do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description radius
Radius module for SER.

%description radius -l pl.UTF-8
Moduł Radius do SER.

%package jabber
Summary:	SER Jabber module
Summary(pl.UTF-8):	Moduł Jabber do SER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description jabber
Jabber module for SER.

%description jabber -l pl.UTF-8
Moduł Jabber do SER.

%prep
%setup -q
%patch0 -p1
sed -i -e 's#modules-dir = lib/ser/modules/#modules-dir = %{_lib}/ser/modules/#g' Makefile.defs

find -type d -name CVS | xargs rm -rf

%build
%{__make} all \
	exclude_modules="%{exclude_modules}" \
	CC="%{__cc}" \
	PREFIX="%{_prefix}" \
	CFLAGS="%{rpmcflags} -Wcast-align -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{ser,sysconfig,rc.d/init.d}

%{__make} install \
	exclude_modules="%{exclude_modules}" \
	PREFIX="%{_prefix}" \
	basedir=$RPM_BUILD_ROOT

for i in modules/*; do \
	i=$(basename $i)
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
%service ser restart "sip Daemon"

%preun
if [ "$1" = "0" ]; then
	%service openser stop
	/sbin/chkconfig --del ser
fi

%files
%defattr(644,root,root,755)
%doc README* ISSUES TODO doc/ser* scripts examples
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/ser
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ser/ser.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ser/dictionary.ser
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ser
%attr(754,root,root) /etc/rc.d/init.d/ser
%dir %{_libdir}/ser
%dir %{_libdir}/ser/modules

# Put explict list here without using globs (to avoid missing some important
# module since build doesn't fail even if module compilation fails) !

%attr(755,root,root) %{_libdir}/ser/modules/acc.so
%attr(755,root,root) %{_libdir}/ser/modules/auth.so
%attr(755,root,root) %{_libdir}/ser/modules/auth_db.so
%attr(755,root,root) %{_libdir}/ser/modules/auth_diameter.so
%attr(755,root,root) %{_libdir}/ser/modules/avp.so
%attr(755,root,root) %{_libdir}/ser/modules/avp_db.so
%attr(755,root,root) %{_libdir}/ser/modules/avpops.so
%attr(755,root,root) %{_libdir}/ser/modules/cpl-c.so
%attr(755,root,root) %{_libdir}/ser/modules/dbtext.so
%attr(755,root,root) %{_libdir}/ser/modules/dispatcher.so
%attr(755,root,root) %{_libdir}/ser/modules/diversion.so
%attr(755,root,root) %{_libdir}/ser/modules/domain.so
%attr(755,root,root) %{_libdir}/ser/modules/enum.so
%attr(755,root,root) %{_libdir}/ser/modules/exec.so
%attr(755,root,root) %{_libdir}/ser/modules/ext.so
%attr(755,root,root) %{_libdir}/ser/modules/flatstore.so
%attr(755,root,root) %{_libdir}/ser/modules/gflags.so
%attr(755,root,root) %{_libdir}/ser/modules/group.so
%attr(755,root,root) %{_libdir}/ser/modules/mangler.so
%attr(755,root,root) %{_libdir}/ser/modules/maxfwd.so
%attr(755,root,root) %{_libdir}/ser/modules/mediaproxy.so
%attr(755,root,root) %{_libdir}/ser/modules/msilo.so
%attr(755,root,root) %{_libdir}/ser/modules/nathelper.so
%attr(755,root,root) %{_libdir}/ser/modules/options.so
%attr(755,root,root) %{_libdir}/ser/modules/pa.so
%attr(755,root,root) %{_libdir}/ser/modules/pdt.so
%attr(755,root,root) %{_libdir}/ser/modules/permissions.so
%attr(755,root,root) %{_libdir}/ser/modules/pike.so
%attr(755,root,root) %{_libdir}/ser/modules/print.so
%attr(755,root,root) %{_libdir}/ser/modules/registrar.so
%attr(755,root,root) %{_libdir}/ser/modules/rr.so
%attr(755,root,root) %{_libdir}/ser/modules/sl.so
%attr(755,root,root) %{_libdir}/ser/modules/sms.so
%attr(755,root,root) %{_libdir}/ser/modules/speeddial.so
%attr(755,root,root) %{_libdir}/ser/modules/textops.so
%attr(755,root,root) %{_libdir}/ser/modules/tm.so
%attr(755,root,root) %{_libdir}/ser/modules/uri.so
%attr(755,root,root) %{_libdir}/ser/modules/uri_db.so
%attr(755,root,root) %{_libdir}/ser/modules/usrloc.so
%attr(755,root,root) %{_libdir}/ser/modules/xlog.so
%{_mandir}/man*/*

%files jabber
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/jabber.so

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/mysql.so

%files postgres
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/postgres.so

%files radius
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ser/modules/auth_radius.so
%attr(755,root,root) %{_libdir}/ser/modules/avp_radius.so
%attr(755,root,root) %{_libdir}/ser/modules/group_radius.so
%attr(755,root,root) %{_libdir}/ser/modules/uri_radius.so
