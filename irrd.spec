Summary:	IRRd - Internet Routing Registry Daemon
Summary(pl):	IRRd - demon Internet Routing Registry
Name:		irrd
Version:	2.2b31
Release:	0.5
License:	BSD-like
Group:		Networking/Deamons
Source0:	http://www.irrd.net/%{name}%{version}.tgz
# Source0-md5:	07b583bdf133332d47461fbcb5d0b78c
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
PreReq:		rc-scripts
Requires(post,preun): /sbin/chkconfig
Requires:	setup >= 2.2.4-1.4
#Suggest:	%{name}-cacher
#Suggest:	mailer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IRRd is a freely available, stand-alone Internet Routing Registry
database server. IRRd supports the RPSL routing registry syntax.

The IRRd package includes all required IRR support services,
including: automated near real-time mirroring of other IRR databases,
update syntax checking, authentication/security, and notification.

%description -l pl
IRRd to wolnodostêpny, samodzielny serwer bazy danych Internet
Routing Registry (rejestru tras internetowych). IRRd obs³uguje
sk³adniê rejestru tras (routingu) RPSL.

Pakiet IRRd zawiera wszystkie wymagane us³ugi wspieraj±ce IRR, w tym:
automatyczny mirroring innych baz danych IRR dzia³aj±cy niemal w
czasie rzeczywistym, kontrolê sk³adni przy uaktualnianiu,
uwierzytelnianie/bezpieczeñstwo oraz powiadomienia.

%package submit-inetd
Summary:	IRRd - Internet Routing Registry Daemon - irr_rpsl_submit server
Summary(pl):	IRRd - demon Internet Routing Registry - serwer irr_rpsl_submit
Group:		Networking/Deamons
PreReq:		rc-inetd
Requires:	%{name} = %{version}-%{release}

%description submit-inetd
irr_rpsl_submit server - you can update IRRd database via TCP
connection.

%description submit-inetd -l pl
Serwer irr_rpsl_submit - pozwala uaktualniæ bazê IRRd przez po³±czenie
TCP.

%package cacher
Summary:	Irrdcacher - retrieves remote database files for the IRRd cache
Summary(pl):	Irrdcacher - odtwarzaj±cy pliki zdalnej bazy danych dla cache IRRd
Group:		Networking/Deamons
Requires:	%{name} = %{version}-%{release}

%description cacher
Irrdcacher retrieves remote database files for the IRRd cache.
Irrdcacher is used to retrieve database copies that are not mirrored.
The irrdcacher software package differs from ftp in that it can
convert RIPE181 databases to RPSL databases, recognize the databases
that make up the IRR and automatically unzip them and send a cache
refresh signal to IRRd.

%description cacher -l pl
Irrdcacher odtwarza pliki pliki zdalnej bazy danych dla cache IRRd.
Jest u¿ywany do odtwarzania kopii bazy danych, która nie jest
mirrorowana. Pakiet ró¿ni siê od tego z ftp tym, ¿e potrafi
konwertowaæ bazy danych RIPE181 na RPSL, rozpoznawaæ bazy danych
tworz±ce IRR, automatycznie rozpakowywaæ je i wysy³aæ sygna³
od¶wie¿enia cache do IRRd.


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
if [ -f /var/lock/subsys/irrd ]; then
	/etc/rc.d/init.d/irrd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/irrd start\" to start irrd daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/irrd ]; then
		/etc/rc.d/init.d/irrd stop >&2
	fi
	/sbin/chkconfig --del irrd
fi

%post submit-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun submit-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/irrd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irrd.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/logrotate.d/irrd

%dir %attr(750,root,root) /var/lib/irrd
%dir %attr(750,root,root) /var/log/irrd

%files submit-inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/rc-inetd/irr_rpsl_submit

%files cacher
%defattr(644,root,root,755)
%doc src/programs/irrdcacher/README src/programs/irrdcacher/sample-cron
%attr(755,root,root) %{_sbindir}/irrdcacher
%attr(755,root,root) %{_bindir}/ripe2rpsl
