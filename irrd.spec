Summary:	IRRd - Internet Routing Registry Daemon
Summary(pl):	IRRd - demon Internet Routing Registry
Name:		irrd
Version:	2.1.5
Release:	0.1
License:	BSD-like
Group:		Networking/Deamons
Source0:	http://www.irrd.net/%{name}%{version}.tgz
# Source0-md5:	49a6e471b1e9b65ae8ebcdbb9ee4341b
Patch0:		%{name}-install.patch
URL:		http://www.irrd.net/
BuildRequires:	autoconf
BuildRequires:	automake
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

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
cd src
rm -f missing
%{__aclocal}
%{__autoheader}
%{__autoconf}

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

cd src
%{__make} install DESTDIR=$RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT irrd-user.pdf samples/irrd.conf.sample
%attr(755,root,root) %{_sbindir}/*
