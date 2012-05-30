Name:		tinyerp
Version:	4.2.3.4
Release:	3
License:	GPLv2+
Group:		Databases
Summary:	ERP Client
URL:		http://tinyerp.org
Source0:	http://tinyerp.org/download/sources/tinyerp-server-%{version}.tar.bz2
Source1:	http://tinyerp.org/download/sources/tinyerp-client-%{version}.tar.bz2
Source2:	tinyerp-server.conf
Source3:	tinyerp-server.init
Source4:	tinyerp-server.logrotate
Source5:	tinyerp-README.urpmi
BuildArch:	noarch
BuildRequires:	python pygtk2.0-devel pygtk2.0-libglade python-libxslt
BuildRequires:	python-psycopg python-dot
BuildRequires:	desktop-file-utils
BuildRequires:	x11-server-xvfb
Requires:       pygtk2.0 pygtk2.0-libglade
Requires:	tinyerp-client tinyerp-server
Patch0:		tinyerp-client.patch
Patch1:		tinyerp-server.patch

%description
Tiny ERP is a free enterprise management software package. It
covers all domains for small to medium businesses; accounting,
stock management, sales, customer relationship, purchases,
project management...

%package	client
Group:		Databases
Summary:	ERP Client
Requires:       pygtk2.0 pygtk2.0-libglade python-dot
Requires(post):	desktop-file-utils
Requires(postun):desktop-file-utils

%description	client
Client components for Tiny ERP.

%package	server
Group:		System/Servers
Summary:	ERP Server
Requires:	pygtk2.0 pygtk2.0-libglade
Requires:	python-psycopg python-libxslt
Requires:	postgresql8.2-plpython
Requires:	python-imaging
Requires:	python-psycopg python-reportlab
Requires:	graphviz python-parsing postgresql8.2-server
Requires:	ghostscript
Requires(pre):	rpm-helper
Requires(postun):rpm-helper

%description server
Server components for Tiny ERP.

IMPORTANT: Please read the INSTALL file in /usr/share/doc/tinyerp-server for
the first
time run.

%prep
%setup -q -a 1 -c %{name}-%{version}

%build
cd %{name}-client-%{version}
Xvfb:69 -nolisten tcp -ac -terminate &
DISPLAY=:69 ./setup.py build
cd ../%{name}-server-%{version}
DISPLAY=:69 ./setup.py build

%install
cd %{name}-client-%{version}
Xvfb:69 -nolisten tcp -ac -terminate &
DISPLAY=:69 ./setup.py install --root=%{buildroot}
cd ../%{name}-server-%{version}
DISPLAY=:69 ./setup.py install --root=%{buildroot}
cd ..

%find_lang tinyerp-client

mv %{buildroot}%{_datadir}/tinyerp-client/* %{buildroot}%{python_sitelib}/tinyerp-client
rm -rf %{buildroot}%{_datadir}/tinyerp-client

mkdir -P %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Tiny ERP
Comment=Open Source ERP Client
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Databases;
EOF

install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/tinyerp-server.conf
install -m755 %{SOURCE3} -D %{buildroot}%{_initrddir}/tinyerp-server
install -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/logrotate.d/tinyerp-server
install -m755 %{SOURCE5} -D %{buildroot}%{_defaultdocdir}/%{name}-%{version}/README.urpmi
mkdir -p %{buildroot}%{_var}/log/tinyerp
mkdir -p %{buildroot}%{_var}/spool/tinyerp
mkdir -p %{buildroot}%{_var}/run/tinyerp

%post client
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null

%postun client
if [ -x %{_bindir}/update-desktop-database ]; then
	%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null
fi


%pre server
%_pre_useradd tinyerp %{_var}/spool/tinyerp /sbin/nologin

%post server
%_post_service tinyerp-server

%preun server
%_preun_service tinyerp-server

%postun server
%_postun_service tinyerp-server
%_postun_userdel tinyerp

%files
%{_defaultdocdir}/%{name}-%{version}/README.urpmi

%files client -f %{name}-client.lang
%{_bindir}/tinyerp-client
%{python_sitelib}/tinyerp-client
%{python_sitelib}/tinyerp_client*
%{_defaultdocdir}/%{name}-client-%{version}/
%{_mandir}/man1/tinyerp-client.*
%{_datadir}/pixmaps/tinyerp-client/
%{_datadir}/applications/*.desktop

%files server
%attr(0755,tinyerp,tinyerp) %dir %{_var}/log/tinyerp
%attr(0755,tinyerp,tinyerp) %dir %{_var}/spool/tinyerp
%attr(0755,tinyerp,tinyerp) %dir %{_var}/run/tinyerp
%{_initrddir}/tinyerp-server
%attr(0644,tinyerp,tinyerp) %config(noreplace) %{_sysconfdir}/tinyerp-server.conf
%attr(0644,tinyerp,tinyerp) %config(noreplace) %{_sysconfdir}/logrotate.d/tinyerp-server
%{_bindir}/tinyerp-server
%{python_sitelib}/tinyerp-server
%{python_sitelib}/tinyerp_server*
%{_defaultdocdir}/%{name}-server-%{version}/
%{_mandir}/man1/tinyerp-server.*
%{_mandir}/man5/terp_serverrc.5*
