#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#

# git tag is 1.9.6, but release name is 2.0-beta4
# https://github.com/falkTX/Carla/releases/tag/1.9.6
%define	tag	1.9.6

%define	beta	beta4
Summary:	Audio plugin host
Name:		Carla
Version:	2.0
Release:	0.%{beta}.1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/falkTX/Carla/archive/%{tag}/%{name}-%{tag}.tar.gz
# Source0-md5:	43e27bd3e1fe226e078ca1b90ea49426
Patch0:		libdir.patch
Patch1:		pyqt5.5.patch
URL:		http://kxstudio.linuxaudio.org/Applications:Carla
BuildRequires:	Mesa-libGL-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	fltk-devel
BuildRequires:	fluidsynth-devel
BuildRequires:	gtk+2-devel
BuildRequires:	gtk+3-devel
BuildRequires:	liblo-devel
BuildRequires:	libprojectM-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	python-PyQt5-devel-tools
BuildRequires:	python3
BuildRequires:	python3-PyQt5-uic
BuildRequires:	rpm-pythonprov
Requires:	python3-PyQt5
Requires:	python3-numpy
Suggests:	python3-rdflib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoprovfiles	%{_libdir}/lv2

%description
Carla is a fully-featured audio plugin host, with support for many
audio drivers and plugin formats.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -n %{name}-%{tag}
%patch0 -p1
%patch1 -p1

%build
%{__make} -j1 \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -i -e '1s,^#!.*python3\?,#!%{__python3},' \
	$RPM_BUILD_ROOT/%{_datadir}/carla/resources/*-* \
	$RPM_BUILD_ROOT/%{_bindir}/*

%py3_comp $RPM_BUILD_ROOT%{_datadir}/carla

ln -s ../__pycache__ $RPM_BUILD_ROOT%{_datadir}/carla/resources/__pycache__

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/carla
%dir %{_libdir}/carla/styles
%{_libdir}/carla/styles/carlastyle.json
%attr(755,root,root) %{_libdir}/carla/styles/carlastyle.so
%attr(755,root,root) %{_libdir}/carla/carla-*
%attr(755,root,root) %{_libdir}/carla/libcarla*.so
%dir %{_libdir}/lv2/carla.lv2
%{_libdir}/lv2/carla.lv2/*.ttl
%attr(755,root,root) %{_libdir}/lv2/carla.lv2/*.so
%{_libdir}/lv2/carla.lv2/resources
%{_libdir}/lv2/carla.lv2/styles
%{_desktopdir}/carla.desktop
%dir %{_datadir}/carla
%dir %{_datadir}/carla/resources
%{_datadir}/carla/resources/nekofilter
%{_datadir}/carla/resources/zynaddsubfx
%{_datadir}/carla/resources/*.py
%{_datadir}/carla/resources/__pycache__
%attr(755,root,root) %{_datadir}/carla/resources/bigmeter-ui
%attr(755,root,root) %{_datadir}/carla/resources/carla-plugin
%attr(755,root,root) %{_datadir}/carla/resources/carla-plugin-patchbay
%attr(755,root,root) %{_datadir}/carla/resources/midiseq-ui
%attr(755,root,root) %{_datadir}/carla/resources/nekofilter-ui
%attr(755,root,root) %{_datadir}/carla/resources/notes-ui
%{_datadir}/carla/*.py
%{_datadir}/carla/__pycache__
%{_datadir}/carla/carla
%{_datadir}/carla/carla-patchbay
%{_datadir}/carla/carla-rack
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/mime/packages/carla.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/carla
%{_pkgconfigdir}/carla-standalone.pc
