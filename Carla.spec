#
# Conditional build:
%bcond_with	zynaddsubfx		# build with built-in ZynAddSubFx synth

# current revision of source/native-plugins/external git submodule
%define plugins_rev   859bc98

Summary:	Audio plugin host
Name:		Carla
Version:	2.0.0
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/falkTX/Carla/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	48fb7b0b8ee2e451798767ae779e8483
Source1:	https://github.com/falkTX/Carla-Plugins/archive/%{plugins_rev}/Carla-Plugins-%{plugins_rev}.tar.gz
# Source1-md5:	d1f05c048b8c813d7768ef40fc9badaa
Patch0:		pypkgdir.patch
Patch1:		soundfonts_path.patch
URL:		http://kxstudio.linuxaudio.org/Applications:Carla
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	fftw3-devel
BuildRequires:	fltk-devel
BuildRequires:	fluidsynth-devel >= 2.0.0
BuildRequires:	gtk+2-devel
BuildRequires:	gtk+3-devel
BuildRequires:	liblo-devel
BuildRequires:	libprojectM-devel
BuildRequires:	mxml-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	python3
BuildRequires:	python3-PyQt5
BuildRequires:	python3-PyQt5-uic
BuildRequires:	python-PyQt5-devel-tools >= 5.8.2-2
BuildRequires:	python-PyQt5-uic
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
Requires:	python3-PyQt5
Requires:	python3-numpy
Suggests:	python3-rdflib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoprovfiles	%{_libdir}/(lv2|vst|carla/jack/libjack.so)

%description
Carla is a fully-featured audio plugin host, with support for many
audio drivers and plugin formats.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -n %{name}-%{version} -a 1

rmdir source/native-plugins/external
mv Carla-Plugins-%{plugins_rev}* source/native-plugins/external

#%patch0 -p1
%patch1 -p1

%build
# to make sure all needed features are available
%{__make} -j1 features \
	EXTERNAL_PLUGINS=true \
	SKIP_STRIPPING=true \
%if %{without zynaddsubfx}
	SKIP_ZYN_SYNTH=true \
	HAVE_ZYN_DEPS=false \
%endif
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix} \
	PYUIC4=%{_bindir}/pyuic4-3 \
	PYUIC5=%{_bindir}/pyuic5-3 \
	PYUIC=%{_bindir}/pyuic5-3 \
	LIBDIR=%{_libdir}

%{__make} -j1 all \
	--trace \
	EXTERNAL_PLUGINS=true \
	SKIP_STRIPPING=true \
%if %{without zynaddsubfx}
	SKIP_ZYN_SYNTH=true \
	HAVE_ZYN_DEPS=false \
%endif
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix} \
	PYUIC4=%{_bindir}/pyuic4-3 \
	PYUIC5=%{_bindir}/pyuic5-3 \
	PYUIC=%{_bindir}/pyuic5-3 \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
%if %{without zynaddsubfx}
	SKIP_ZYN_SYNTH=true \
	HAVE_ZYN_DEPS=false \
%endif
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	PYPKGDIR=%{py3_sitescriptdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -i -e '1s,^#!.*python3\?,#!%{__python3},' \
	$RPM_BUILD_ROOT/%{_datadir}/carla/resources/*-* \
	$RPM_BUILD_ROOT/%{_bindir}/*

%py3_comp $RPM_BUILD_ROOT%{_datadir}/carla

# so debuginfo is properly extracted
chmod a+x $RPM_BUILD_ROOT%{_libdir}/carla/{,*/}*.so

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
%dir %{_libdir}/carla/jack
%attr(755,root,root) %{_libdir}/carla/jack/libjack.so.0
%dir %{_libdir}/lv2/carla.lv2
%{_libdir}/lv2/carla.lv2/*.ttl
%attr(755,root,root) %{_libdir}/lv2/carla.lv2/*.so
%attr(755,root,root) %{_libdir}/lv2/carla.lv2/carla-bridge-lv2-*
%attr(755,root,root) %{_libdir}/lv2/carla.lv2/carla-bridge-native
%attr(755,root,root) %{_libdir}/lv2/carla.lv2/carla-discovery-native
%{_libdir}/lv2/carla.lv2/jack
%{_libdir}/lv2/carla.lv2/resources
%{_libdir}/lv2/carla.lv2/styles
%dir %{_libdir}/vst
%dir %{_libdir}/vst/carla.vst
%attr(755,root,root) %{_libdir}/vst/carla.vst/*.so
%attr(755,root,root) %{_libdir}/vst/carla.vst/carla-bridge-lv2-*
%attr(755,root,root) %{_libdir}/vst/carla.vst/carla-bridge-native
%attr(755,root,root) %{_libdir}/vst/carla.vst/carla-discovery-native
%{_libdir}/vst/carla.vst/jack
%{_libdir}/vst/carla.vst/resources
%{_libdir}/vst/carla.vst/styles
%{_desktopdir}/carla.desktop
%{_desktopdir}/carla-control.desktop
%dir %{_datadir}/carla
%dir %{_datadir}/carla/resources
%{_datadir}/carla/resources/widgets
%{?with_zynaddsubfx:%{_datadir}/carla/resources/zynaddsubfx}
%{_datadir}/carla/resources/*.py
%{_datadir}/carla/resources/__pycache__
%attr(755,root,root) %{_datadir}/carla/carla-control
%attr(755,root,root) %{_datadir}/carla/carla-jack-multi
%attr(755,root,root) %{_datadir}/carla/carla-jack-single
%attr(755,root,root) %{_datadir}/carla/resources/bigmeter-ui
%attr(755,root,root) %{_datadir}/carla/resources/carla-plugin
%attr(755,root,root) %{_datadir}/carla/resources/carla-plugin-patchbay
%attr(755,root,root) %{_datadir}/carla/resources/midipattern-ui
%attr(755,root,root) %{_datadir}/carla/resources/notes-ui
%{?with_zynaddsubfx:%attr(755,root,root) %{_datadir}/carla/resources/zynaddsubfx-ui}
%{_datadir}/carla/widgets
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
%{_pkgconfigdir}/carla-native-plugin.pc
%{_pkgconfigdir}/carla-standalone.pc
%{_pkgconfigdir}/carla-utils.pc
