Name:             h2o
Version:          1.5.0
Release:          2%{?dist}
Summary:          An optimized HTTP server with support for HTTP/1.x and HTTP/2

License:          MIT
Url:              https://h2o.github.io/
Source0:          https://github.com/h2o/h2o/archive/v%{version}.tar.gz
Source1:          h2o.conf
Source2:          h2o.service
Source3:          h2o.logrotate
Source4:          h2o.1

# https://github.com/h2o/h2o/issues/537
Patch0:           setuidgid.patch

BuildRequires:    cmake, openssl-devel, gcc-c++, make, systemd
Requires:         perl-Server-Starter, openssl
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
H2O is a very fast HTTP server written in C.

%global _hardened_build 1

%prep
%setup -q
%patch0 -p 1

%build
%cmake -DWITH_BUNDLED_SSL=on .
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

# https://github.com/h2o/h2o/issues/536
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_prefix}/lib/libh2o-evloop.so

%check
ctest -V %{?_smp_mflags}

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%doc %{_datarootdir}/doc/%{name}
%doc %{_mandir}/man1/%{name}.1.gz
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%attr(755,nobody,nobody) %dir %{_localstatedir}/log/%{name}
%{_datarootdir}/%{name}
%{_libexecdir}/%{name}/setuidgid

%changelog
* Mon Oct 05 2015 Martin Hagstrom <marhag87@gmail.com> 1.5.0-2
- Set pidfile correctly in systemd service file
* Fri Oct 02 2015 Martin Hagstrom <martin@mrhg.se> 1.5.0-1
- Initial release
