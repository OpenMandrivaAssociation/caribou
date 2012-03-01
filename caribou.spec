%define major		0
%define gir_major	1.0
%define libname		%mklibname %{name} %{major}
%define libnamedevel	%mklibname -d %{name}
%define girname		%mklibname %{name}-gir %{gir_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		caribou
Version:	0.4.1
Release:	%mkrel 4
Summary:	A simplified in-place on-screen keyboard
Group:		Accessibility
License:	LGPLv2+
URL:		http://live.gnome.org/Caribou
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	python-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gdk-3.0)
BuildRequires:	python-gi
BuildRequires:	pkgconfig(pyclutter-1.0)
BuildRequires:	python-at-spi
BuildRequires:	python-virtkey
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	pkgconfig(clutter-1.0)
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	libjson-glib-devel
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	gobject-introspection-devel
BuildRequires:	pkgconfig(pygobject-3.0)
Requires:	pyatspi

%description
Caribou is a text entry application that currently manifests itself as
a simplified in-place on-screen keyboard.

%package	gtk2
Summary:	GTK2 Integration for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	gtk2
GTK2 Integration for %{name}.

%package	gtk3
Summary:	GTK3 Integration for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	gtk3
GTK3 Integration for %{name}.

%package -n	%{libname}
Summary:	Library files for %{name}
Group:		System/Libraries

%description -n %{libname}
Library files for %{name}.

%package -n	%{libnamedevel}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libnamedevel}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

find %{buildroot} -name '*.la' -exec rm -f {} ';'

echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/caribou.desktop
echo "OnlyShowIn=GNOME;" >> %{buildroot}%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/caribou.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop || :

%find_lang caribou

%files -f caribou.lang
%doc NEWS README
%{_bindir}/caribou
%{_bindir}/caribou-preferences
%{_datadir}/caribou
%{_datadir}/antler
%{_datadir}/dbus-1/services/org.gnome.Caribou.Antler.service
%{_libexecdir}/antler-keyboard
%{_datadir}/applications/caribou.desktop
%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
%{_datadir}/glib-2.0/schemas/*
%{py_puresitedir}/caribou

%files gtk2
%{_libdir}/gtk-2.0/modules/libcaribou-gtk-module.so

%files gtk3
%{_libdir}/gtk-3.0/modules/libcaribou-gtk-module.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Caribou-%{gir_major}.typelib

%files -n %{libnamedevel}
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/Caribou-%{gir_major}.gir


