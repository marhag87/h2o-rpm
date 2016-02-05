Name:             h2o
Version:          1.7.0
Release:          1%{?dist}
Summary:          HTTP server

License:          MIT
Url:              https://h2o.github.io/
Source0:          https://github.com/h2o/h2o/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:          h2o.conf
Source2:          h2o.service
Source3:          h2o.logrotate
Source4:          h2o.1

BuildRequires:    cmake, openssl-devel, gcc-c++, make, systemd
# Required for tests
BuildRequires:    perl-Test-Harness, perl-Digest-MD5, perl-Test-TCP, perl-Scope-Guard, perl-URI, perl-IO-Socket-SSL
# These are required as well, but tests fail on fedora 23 with them for some reason: nghttp2, httpd-tools, memcached, curl >= 7.43.0-2
Requires:         perl-Server-Starter, openssl
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd


%description
H2O is a very fast HTTP server written in C. It supports HTTP/1.x and HTTP/2

%global _hardened_build 1

%prep
%autosetup -p 1

%build
%cmake -DWITHOUT_LIBS=ON .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -p -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}
install -p -d -m 0755 %{buildroot}%{_unitdir}
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -d -m 0755 %{buildroot}%{_datarootdir}/%{name}/www
install -p -d -m 0755 %{buildroot}%{_mandir}/man1

install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -m 0644 %{SOURCE4} %{buildroot}%{_mandir}/man1/%{name}.1

%check
make check

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_datarootdir}/doc/%{name}
%{_mandir}/man1/%{name}.1.gz
%license LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%attr(755,nobody,nobody) %dir %{_localstatedir}/log/%{name}
%{_datarootdir}/%{name}

%changelog
* Tue Jan 26 2016 Martin Hagstrom <marhag87@gmail.com> 1.7.0-1
- Update to version 1.7.0
* Tue Jan 26 2016 Martin Hagstrom <marhag87@gmail.com> 1.6.3-1
- Update to version 1.6.3
* Fri Dec 18 2015 Martin Hagstrom <marhag87@gmail.com> 1.6.2-1
- Update to version 1.6.2
* Fri Dec 18 2015 Martin Hagstrom <marhag87@gmail.com> 1.6.1-2
- Add dependencies for check
* Fri Dec 18 2015 Martin Hagstrom <marhag87@gmail.com> 1.6.1-1
- Update to version 1.6.1
* Fri Dec 04 2015 Martin Hagstrom <marhag87@gmail.com> 1.6.0-1
- Update to version 1.6.0
* Sat Nov 14 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.4-1
- Update to version 1.5.4
* Tue Oct 20 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.2-1
- Update to version 1.5.2
* Wed Oct 14 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.0-5
- Don't bundle SSL
- Don't build libs
- Take proper ownership of files
- Run tests properly
* Mon Oct 05 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.0-4
- Update summary and description
- Remove ldconfig
- Take ownership of more directories
* Mon Oct 05 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.0-3
- Set source name according to https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Tags
- Use autosetup
- Remove %defattr
* Mon Oct 05 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.0-2
- Set pidfile correctly in systemd service file
* Fri Oct 02 2015 Martin Hagstrom <martin@mrhg.se> 1.5.0-1
- Initial release
