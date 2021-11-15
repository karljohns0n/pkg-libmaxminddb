Name:				libmaxminddb
Summary:			C library for the MaxMind DB file format
Version:			1.6.0
Release:			1%{?dist}
Group:				System/Libraries
URL:				https://maxmind.github.io/libmaxminddb
Source0:			https://github.com/maxmind/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
License:			ASL 2.0 and BSD

BuildRequires:		gcc
BuildRequires:		perl-interpreter

%description
The package contains libmaxminddb library.

%package devel
Requires:			%{name}%{?_isa} = %{version}-%{release}
Requires:			pkgconfig
Summary:			Development header files for libmaxminddb
Group:				System/Libraries

%description devel
The package contains development header files for the libmaxminddb library
and the mmdblookup utility which allows IP address lookup in a MaxMind DB file.

%prep
%setup -q

%build
%configure --disable-static
# remove embeded RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# link only requried libraries
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%check
# tests are linked dynamically, preload the library as we have removed RPATH
LD_PRELOAD=%{buildroot}%{_libdir}/libmaxminddb.so make check

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libmaxminddb.so.*

%files devel
%license NOTICE
%doc Changes.md
%{_bindir}/mmdblookup
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_libdir}/libmaxminddb.so
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Mon Nov 15 2021 Karl Johnson <karljohnson.it@gmail.com> 1.6.0-1
- Bump to 1.6.0

* Fri Jan 10 2020 Karl Johnson <karljohnson.it@gmail.com> 1.3.2-2
- Add CentOS 8 support

* Tue Dec 4 2018 Karl Johnson <karljohnson.it@gmail.com> 1.3.2-1
- Rebase package from EPEL
- Bump to 1.3.2

* Sun Mar 27 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.2.0-1
- rebase to new version

* Mon Mar 21 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.5-1
- rebase to new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-5
- add pkg-config file from the upcoming upstream version

* Mon Sep 14 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-4
- remove utils subpackage and place mmdblookup into devel subpackage
- remove Group from the spec file
- move NOTICE and Changes.md to devel subpackage

* Thu Sep 03 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-3
- updated package licence
- added --as-needed linker flag

* Tue Sep 01 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-1
- initial version of the package
