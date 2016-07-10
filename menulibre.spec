Name:           menulibre
Version:        2.1.3.git
Release:        2%{?dist}
Summary:        FreeDesktop.org compliant menu editor

License:        GPLv3
URL:            https://smdavis.us/projects/menulibre/
Source0:        https://launchpad.net/menulibre/2.1/%{version}/+download/menulibre-%{version}.tar.gz

# Exit early when adding a new launcher and no directory is selected
# https://bugs.launchpad.net/menulibre/+bug/1556664
#Patch0:         %{name}-add-launcher-none-check.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  python3-devel
BuildRequires:  python3-distutils-extra
Requires:       gnome-menus
Requires:       gtk3
Requires:       python3-psutil

%description
MenuLibre is a graphical FreeDesktop.org compliant menu editor that lets you
edit menu entries.

%prep
%setup -q
#%patch0 -p0

%build

%install
%{__python3} setup.py install --root=%{buildroot}

# Remove hashbang line from non-executable library files
for lib in %{buildroot}%{python3_sitelib}/menulibre{,_lib}/*.py; do
    sed '1{\@^#!/usr/bin/python3@d}' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done

desktop-file-validate %{buildroot}/%{_datadir}/applications/menulibre.desktop
%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS NEWS PKG-INFO README
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/menulibre.desktop
%{_datadir}/icons/hicolor/16x16/apps/menulibre.svg
%{_datadir}/icons/hicolor/24x24/apps/menulibre.svg
%{_datadir}/icons/hicolor/32x32/apps/menulibre.svg
%{_datadir}/icons/hicolor/48x48/apps/menulibre.svg
%{_datadir}/icons/hicolor/64x64/apps/menulibre.svg
%{_datadir}/icons/hicolor/scalable/apps/menulibre.svg
%{_datadir}/menulibre/
%{_datadir}/pixmaps/menulibre.png
%{_mandir}/man1/menulibre.1.gz
%{python3_sitelib}/menulibre
%{python3_sitelib}/menulibre_lib
#%{python3_sitelib}/menulibre-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/menulibre-2.1.3-py%{python3_version}.egg-info

%changelog
* Sun Apr 10 2016 Marcus Karlsson <mk@acc.umu.se> - 2.1.3-1
- Update to upstream release 2.1.3.

* Sun Mar 13 2016 Marcus Karlsson <mk@acc.umu.se> - 2.1.2-4
- Fix a problem where adding a launcher and no directory was selected would
  emit a type error

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 10 2015 Marcus Karlsson <mk@acc.umu.se> - 2.1.2-1
- Update to 2.1.2

* Sun May 31 2015 Marcus Karlsson <mk@acc.umu.se> - 2.0.6-1
- Initial build
