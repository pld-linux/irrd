
%define _rel 0.3

Summary:	IRRd - Internet Routing Registry Daemon
Summary(pl):	IRRd - demon Internet Routing Registry
Name:		irrd
Version:	2.1.5
Release:	%{_rel}
License:	BSD-like
Group:		Networking/Deamons
Source0:	http://www.irrd.net/%{name}%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
# Source0-md5:	49a6e471b1e9b65ae8ebcdbb9ee4341b
Patch0:		%{name}-install.patch
Patch1:		%{name}-bison.patch
URL:		http://www.irrd.net/
BuildRequires:	autoconf
BuildRequires:	automake
Requires(post,preun): /sbin/chkconfig
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

%package -n %{name}-cacher
Summary:	Irrdcacher retrieves remote database files for the IRRd cache.
Group:		Networking/Deamons
Release:	%{_rel}

%description -n %{name}-cacher
Irrdcacher retrieves remote database files for the IRRd cache.
Irrdcacher is used to retrieve database copies that are not mirrored.
The irrdcacher software package  differs from ftp in that it can 
convert RIPE181 databases to RPSL databases, recognize the databases 
that make up the IRR and automatically unzip them and send a cache 
refresh signal to IRRd.

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

%configure --with-gdbm --enable-ipv6 --enable-threads 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

install -d $RPM_BUILD_ROOT/var/lib/irrd

cd src
%{__make} install DESTDIR=$RPM_BUILD_ROOT%{_sbindir}

cp programs/IRRd/irrd.8 $RPM_BUILD_ROOT%{_mandir}/man8/
cp programs/irrdcacher/irrdcacher $RPM_BUILD_ROOT%{_sbindir}/
cp programs/irrdcacher/ripe2rpsl $RPM_BUILD_ROOT%{_bindir}/

install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/irrd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/irrd

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
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

%files
%defattr(644,root,root,755)
%doc COPYRIGHT irrd-user.pdf samples/irrd.conf.sample NOTES README 
%doc src/programs/IRRd/COMMANDS.INFO
%attr(755,root,root) %{_sbindir}/irr_check
%attr(755,root,root) %{_sbindir}/irr_notify
%attr(755,root,root) %{_sbindir}/irr_rpsl_submit
%attr(755,root,root) %{_sbindir}/irrd
%{_mandir}/man8/*

%attr(754,root,root) /etc/rc.d/init.d/irrd
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/irrd

%dir %attr(750,root,root) /var/lib/irrd

%files -n %{name}-cacher
%defattr(644,root,root,755)
%doc src/programs/irrdcacher/README src/programs/irrdcacher/sample-cron
%doc src/programs/irrdcacher/update_source
%attr(755,root,root) %{_sbindir}/irrdcacher
%attr(755,root,root) %{_bindir}/ripe2rpsl
