Summary:	SIP proxy, redirect and registrar server
Summary(pl):	Serwer SIP rejestruj±cy, przekierowuj±cy i robi±cy proxy
Name:		ser
Version:	0.8.10
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://ftp.berlios.de/pub/ser/%{version}/src/%{name}-%{version}_src.tar.gz
# Source0-md5:	a3a06a9bc15f82321a6d9bc31d582c33
#Source1:	%{name}.init
#Source2:	%{name}.sysconfig
URL:		http://www.iptel.org/ser/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	mysql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SIP Express Router (ser) is a high-performance, configurable, free SIP
( RFC3261 ) server . It can act as registrar, proxy or redirect
server. SER features an application-server interface, presence
support, SMS gateway, SIMPLE2Jabber gateway, RADIUS/syslog accounting
and authorization, server status monitoring, FCP security, etc.
Web-based user provisioning, serweb, available. Its performance allows
it to deal with operational burdens, such as broken network
components, attacks, power-up reboots and rapidly growing user
population. SER's configuration ability meets needs of a whole range
of scenarios including small-office use, enterprise PBX replacements
and carrier services.

%prep
%setup -q

%build
%{__make} prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir},%{_sysconfdir}/{ser,sysconfig,rc.d/init.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ser
#install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ser

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
%doc AUTHORS
#%doc README doc/*.{html,gif,css} ser/{BUGS,README.*,TODO} scripts
#%doc tools/{addsipuser/*.html,canonicalize/*.html,ishere/*.html,tracker/*.html}
#%attr(755,root,root) %{_bindir}/base64-*
#%attr(755,root,root) %{_sbindir}/*
#%dir %{_sysconfdir}/ser
#%config(noreplace) %{_sysconfdir}/ser/ser.conf
#%config(noreplace) /etc/sysconfig/ser
#%attr(754,root,root) /etc/rc.d/init.d/ser
#%dir /var/lib/ser
#%dir /var/lib/ser/logs
#/var/lib/ser/gateways.sample
