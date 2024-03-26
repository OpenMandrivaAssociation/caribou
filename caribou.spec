%define _disable_ld_no_undefined 1

%global optflags %{optflags} -Wno-incompatible-function-pointer-types

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major 0
%define api 1.0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname -d %{name}

Summary:	A simplified in-place on-screen keyboard
Name:		caribou
Version:	0.4.21
Release:	12
Group:		Accessibility
License:	LGPLv2+
URL:		https://live.gnome.org/Caribou
Source0:	https://ftp.gnome.org/pub/GNOME/sources/caribou/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		caribou-0.4.20-fix-python-exec.patch
# caribou isn't needed in gnome-shell so don't start there
Patch1:		change_autostart_cinnamon.patch
Patch2:		fix-style-css.patch
Patch3:		Fix-compilation-error.patch
Patch4:		Fix-subkey-popmenu-not-showing-after-being-dismissed.patch
Patch5:		xadapter.vala-Remove-XkbKeyTypesMask-and-f.patch
Patch6:   drop_gir_patch.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	python-gi
BuildRequires:	vala
BuildRequires:	vala-devel
BuildRequires:	python-pkg-resources
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	pkgconfig(atspi-2)
BuildRequires:	pkgconfig(clutter-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gdk-3.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(xtst)

%description
Caribou is a text entry application that currently manifests itself as
a simplified in-place on-screen keyboard.

%package gtk2
Summary:	GTK2 Integration for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description gtk2
GTK2 Integration for %{name}.

%package gtk3
Summary:	GTK3 Integration for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description gtk3
GTK3 Integration for %{name}.

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/Libraries

%description -n %{libname}
Library files for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
export PYTHON=%{__python3}
%configure --disable-schemas-compile
%make_build

%install
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'

echo "OnlyShowIn=GNOME;" >> %{buildroot}%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop || :

%find_lang caribou

%files -f caribou.lang
%doc NEWS README
%{_bindir}/caribou-preferences
%{_datadir}/caribou
%{_libexecdir}/caribou
%{_datadir}/antler
%{_datadir}/dbus-1/services/org.gnome.Caribou.Antler.service
%{_libexecdir}/antler-keyboard
%{_datadir}/vala/vapi/caribou*
%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/dbus-1/services/org.gnome.Caribou.Daemon.service
%{py3_puresitedir}/caribou

%files gtk2
%{_libdir}/gtk-2.0/modules/libcaribou-gtk-module.so

%files gtk3
%{_libdir}/gtk-3.0/modules/libcaribou-gtk-module.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Caribou-%{api}.typelib

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Caribou-%{api}.gir
