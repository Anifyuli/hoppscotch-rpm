%global appver  25.11.2
%global apprel  0

Name:           hoppscotch-desktop
Version:        %{appver}
Release:        1%{?dist}
Summary:        Open source API development ecosystem

License:        MIT
URL:            https://hoppscotch.io/
Source0:        https://github.com/hoppscotch/releases/releases/download/v%{appver}-%{apprel}/Hoppscotch_linux_x64.deb

BuildArch:      x86_64

# Dependencies based on Arch Linux PKGBUILD
Requires:       cairo
Requires:       desktop-file-utils
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libsoup
Requires:       openssl-libs
Requires:       pango
Requires:       webkit2gtk4.1

# Build requires for extract DEB
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  gzip

%description
Hoppscotch is an open-source API development ecosystem that helps you 
create and test your API requests, saving precious time in development.

%prep
# Extract .deb file
ar x %{SOURCE0}
tar -xzf data.tar.gz

%build
# No build stuff

%install
rm -rf %{buildroot}

# Copying stuff to buildroot
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{32x32,128x128,256x256@2}/apps
cp -p usr/bin/hoppscotch-desktop %{buildroot}%{_bindir}/hoppscotch-desktop-bin
cp -p usr/share/applications/Hoppscotch.desktop %{buildroot}%{_datadir}/applications/
cp -p usr/share/icons/hicolor/32x32/apps/hoppscotch-desktop.png \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
cp -p usr/share/icons/hicolor/128x128/apps/hoppscotch-desktop.png \
   %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
cp -p usr/share/icons/hicolor/256x256@2/apps/hoppscotch-desktop.png \
   %{buildroot}%{_datadir}/icons/hicolor/256x256@2/apps/

# Add Development categories to desktop files
sed -i '/^Categories=/d' %{buildroot}%{_datadir}/applications/Hoppscotch.desktop
echo "Categories=Development;" >> %{buildroot}%{_datadir}/applications/Hoppscotch.desktop

# Create a wrapper script
cat > %{buildroot}%{_bindir}/hoppscotch-desktop <<'EOF'
#!/usr/bin/env sh
# Wrapper to launch Hoppscotch Desktop with WebKit fallbacks.
# Users can override by exporting the variables before running.

export WEBKIT_DISABLE_COMPOSITING_MODE="${WEBKIT_DISABLE_COMPOSITING_MODE:-1}"
export WEBKIT_DISABLE_DMABUF_RENDERER="${WEBKIT_DISABLE_DMABUF_RENDERER:-1}"

exec %{_bindir}/hoppscotch-desktop-bin "$@"
EOF

chmod 755 %{buildroot}%{_bindir}/hoppscotch-desktop

%post
# Update desktop database & icon cache
update-desktop-database %{_datadir}/applications &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
# Update desktop database & icon cache after uninstall
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_bindir}/hoppscotch-desktop
%{_bindir}/hoppscotch-desktop-bin
%{_datadir}/applications/Hoppscotch.desktop
%{_datadir}/icons/hicolor/32x32/apps/hoppscotch-desktop.png
%{_datadir}/icons/hicolor/128x128/apps/hoppscotch-desktop.png
%{_datadir}/icons/hicolor/256x256@2/apps/hoppscotch-desktop.png

%changelog
* Sun Dec 21 2025 Anifyuliansyah <anifyuli007@outlook.co.id> - 25.11.2-0
- Initial package for Fedora
- Added WebKit workaround wrapper for Wayland compatibility
