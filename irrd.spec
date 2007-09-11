Summary:	IRRd - Internet Routing Registry Daemon
Summary(pl.UTF-8):	IRRd - demon Internet Routing Registry
Name:		irrd
Version:	2.2.2
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://www.irrd.net/%{name}%{version}.tgz
# Source0-md5:	665799d6810ec28a3f611a9bd8d65979
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.inetd
Source4:	%{name}.logrotate
Source5:	%{name}.conf
Patch0:		%{name}-install.patch
Patch1:		%{name}-bison.patch
URL:		http://www.irrd.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	setup >= 2.2.4-1.4
Conflicts:	logrotate < 3.7-4
#Suggests:	%{name}-cacher
#Suggests:	mailer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IRRd is a freely available, stand-alone Internet Routing Registry
database server. IRRd supports the RPSL routing registry syntax.

The IRRd package includes all required IRR support services,
including: automated near real-time mirroring of other IRR databases,
update syntax checking, authentication/security, and notification.

%description -l pl.UTF-8
IRRd to wolnodostępny, samodzielny serwer bazy danych Internet Routing
Registry (rejestru tras internetowych). IRRd obsługuje składnię
rejestru tras (routingu) RPSL.

Pakiet IRRd zawiera wszystkie wymagane usługi wspierające IRR, w tym:
automatyczny mirroring innych baz danych IRR działający niemal w
czasie rzeczywistym, kontrolę składni przy uaktualnianiu,
uwierzytelnianie/bezpieczeństwo oraz powiadomienia.

%package submit-inetd
Summary:	IRRd - Internet Routing Registry Daemon - irr_rpsl_submit server
Summary(pl.UTF-8):	IRRd - demon Internet Routing Registry - serwer irr_rpsl_submit
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd

%description submit-inetd
irr_rpsl_submit server - you can update IRRd database via TCP
connection.

%description submit-inetd -l pl.UTF-8
Serwer irr_rpsl_submit - pozwala uaktualnić bazę IRRd przez połączenie
TCP.

%package cacher
Summary:	Irrdcacher - retrieves remote database files for the IRRd cache
Summary(pl.UTF-8):	Irrdcacher - odtwarzający pliki zdalnej bazy danych dla cache IRRd
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description cacher
Irrdcacher retrieves remote database files for the IRRd cache.
Irrdcacher is used to retrieve database copies that are not mirrored.
The irrdcacher software package differs from FTP in that it can
convert RIPE181 databases to RPSL databases, recognize the databases
that make up the IRR and automatically unzip them and send a cache
refresh signal to IRRd.

%description cacher -l pl.UTF-8
Irrdcacher odtwarza pliki pliki zdalnej bazy danych dla cache IRRd.
Jest używany do odtwarzania kopii bazy danych, która nie jest
mirrorowana. Pakiet różni się od tego z FTP tym, że potrafi
konwertować bazy danych RIPE181 na RPSL, rozpoznawać bazy danych
tworzące IRR, automatycznie rozpakowywać je i wysyłać sygnał
odświeżenia cache do IRRd.


%prep
%setup -q -n %{name}%{version}
%patch0 -p1
# quick dirty hack...
%patch1 -p1

%build
cd src
rm -f missing
%{__aclocal}
%{__autoheader}
%{__autoconf}

%configure \
	--with-gdbm \
	--enable-ipv6 \
	--enable-threads

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm src/programs/irr_util/.templates.config.swp
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8,%{_initrddir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig{,/rc-inetd},logrotate.d},/var/{lib,log}/irrd}

cd src
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_sbindir}

cp programs/IRRd/irrd.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp programs/irrdcacher/irrdcacher $RPM_BUILD_ROOT%{_sbindir}
cp programs/irrdcacher/ripe2rpsl $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/irr_rpsl_submit
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/irrd
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/irrd
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/irrd.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/irrd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add irrd
%service irrd restart "irrd daemon"

%preun
if [ "$1" = "0" ]; then
	%service irrd stop
	/sbin/chkconfig --del irrd
fi

%post submit-inetd
%service -q rc-inetd reload

%postun submit-inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc COPYRIGHT irrd-user.pdf samples/irrd.conf.sample NOTES README
%doc src/programs/IRRd/COMMANDS.INFO
%doc src/programs/irr_util
%attr(755,root,root) %{_sbindir}/irr_notify
%attr(755,root,root) %{_sbindir}/irr_rpsl_check
%attr(755,root,root) %{_sbindir}/irr_rpsl_submit
%attr(755,root,root) %{_sbindir}/irrd
%{_mandir}/man8/*

%attr(754,root,root) %{_initrddir}/irrd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/irrd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/irrd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/irrd

%dir %attr(750,root,root) /var/lib/irrd
%dir %attr(750,root,root) /var/log/irrd

%files submit-inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/irr_rpsl_submit

%files cacher
%defattr(644,root,root,755)
%doc src/programs/irrdcacher/README src/programs/irrdcacher/sample-cron
%attr(755,root,root) %{_sbindir}/irrdcacher
%attr(755,root,root) %{_bindir}/ripe2rpsl
