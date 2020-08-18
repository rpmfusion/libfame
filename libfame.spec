Name:       libfame
Summary:    Fast Assembly MPEG Encoding library
Version:    0.9.1
Release:    26%{?dist}
License:    LGPLv2+
URL:        http://fame.sourceforge.net/
Source0:    http://download.sourceforge.net/fame/%{name}-%{version}.tar.gz
Patch0:     %{name}-aclocal18.patch
Patch1:     %{name}-config-rpath.patch
Patch2:     %{name}-gccver.patch
Patch3:     %{name}-nomarch.patch
# Patch from http://www.linuxfromscratch.org/blfs/downloads/svn/
Patch4:     %{name}-0.9.1-gcc34-1.patch
Patch5:     %{name}-0.9.1-fstrict-aliasing.patch
Patch6:     %{name}-0.9.1-x86_64.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
FAME is a library for fast MPEG encoding.

%package devel
Summary:    Libraries and include to develop using FAME
Requires:   %{name}%{?isa} = %{version}-%{release}

%description devel
FAME is a library for fast MPEG encoding.
This package contains the libraries, include files and other resources
you can use to develop FAME applications.


%prep
%setup -q
%patch0 -p0 -b .aclocal18
%patch1 -p0 -b .config-rpath
%patch2 -p1 -b .gccver
%patch3 -p1 -b .nomarch
%patch4 -p1 -b .mmxone
%patch5 -p1 -b .fstrict-aliasing
%patch6 -p1 -b .x86_64
# This is required since the included libtool stuff is too old and breaks
# linking (-lm and -lc functions not found!) on FC5 x86_64.
%{__rm} -f acinclude.m4 aclocal.m4
%{__cp} -f %{_datadir}/aclocal/libtool.m4 libtool.m4
touch NEWS ChangeLog
autoreconf -fiv

# Fix lib stuff for lib64
%{__perl} -pi.orig -e 's|/lib"|/%{_lib}"|g' configure.in


%build
# Note: SSE support does nothing (as of 0.9.1).  grep for HAS_SSE.
%configure --disable-dependency-tracking \
%ifarch %{ix86} ia64
  --enable-mmx
%else
  --disable-mmx
%endif
%{make_build}


%install
%{make_install}

#Remove libtool archives.
find %buildroot -name '*.la' -or -name '*.a' | xargs rm -f

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS BUGS CHANGES README TODO
%license COPYING
%{_libdir}/libfame*.so.*

%files devel
%{_bindir}/libfame-config
%{_includedir}/fame*.h
%{_libdir}/libfame.so
%{_datadir}/aclocal/libfame.m4
%{_mandir}/man3/fame*.3*

%changelog
* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Leigh Scott <leigh123linux@gmail.com> - 0.9.1-24
- Remove BuildRoot tag
- Remove Group tag
- Add isa to devel requires
- Remove clean section
- Remove defattr from files
- Delete .a and .la files
- Spec file clean up
- Install license file correctly
- Fix license type
- Fix mixed use of tabs and whitespace

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.9.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.1-16
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.1-14
- rebuild for new F11 features

* Fri Aug 15 2008 Jarod Wilson <jarod@wilsonet.com> 0.9.1-13
- Merge livna and freshrpms packages for rpmfusion

* Mon Sep 18 2006 Matthias Saou <http://freshrpms.net/> 0.9.1-12
- Update underquoted patch, which stopped applying cleanly for some reason.

* Mon Mar 20 2006 Matthias Saou <http://freshrpms.net/> 0.9.1-11
- Remove old libtool/m4 files to fix x86_64 FC5 linking.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.9.1-9
- Release bump to drop the disttag number in FC5 build.

* Fri Sep 30 2005 Matthias Saou <http://freshrpms.net/> 0.9.1-8
- Include x86_64 patch from Andy Loening, fixes some segfaults.
- Update underquoted patch to also remove warnings at libfame build time.

* Sun Jun  5 2005 Matthias Saou <http://freshrpms.net/> 0.9.1-7
- Make the underquoted patch apply to the .in file too, so it actually works.
- Put ldconfig calls back as programs to have rpm's deps pick them up.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 0.9.1-6
- Run plain "./autogen.sh" instead of autoreconf to avoid libm problem on
  x86_64 (weird one!).
- Actually really apply the last patch too...

* Sun May  1 2005 Matthias Saou <http://freshrpms.net/> 0.9.1-5
- Patch the m4 file to fix underquoted warning.
