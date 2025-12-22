# Hoppscotch Desktop and CLI for Fedora

<div align="center">

![Hoppscotch Logo](https://raw.githubusercontent.com/hoppscotch/hoppscotch/main/packages/hoppscotch-common/public/icon.svg)

**Open source API development ecosystem**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Fedora](https://img.shields.io/badge/Fedora-39%2B-blue.svg)](https://getfedora.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.kernel.org/)

[Features](#features) • [Installation](#installation) • [Building](#building-from-source) • [Usage](#usage) • [Troubleshooting](#troubleshooting)

</div>

---

## 📖 About

Hoppscotch is a lightweight, fast, and beautiful open-source API development ecosystem. It helps you create, test, and document your APIs with ease, making it an excellent alternative to Postman and Insomnia.

This repository provides RPM packages for **Fedora Linux** users:
- 🖥️ **Hoppscotch Desktop** - Full-featured GUI application
- ⌨️ **Hoppscotch CLI** - Command-line tool for CI/CD integration

## ✨ Features

### Desktop Application
- 🚀 Fast and lightweight Tauri-based desktop app
- 🎨 Beautiful and intuitive user interface
- 🔒 Privacy-focused - all data stored locally
- 🌙 Dark mode support
- 📱 Responsive design
- 🔌 REST, GraphQL, WebSocket, SSE support
- 📚 Request collections and environments
- 💾 Import/Export collections (Postman, Insomnia compatible)

### CLI Tool
- 🤖 Perfect for CI/CD pipelines
- 📝 Run test collections from command line
- 🔄 Environment variable support
- 📊 Detailed test reports
- ✅ Exit codes for automation

## 📋 Requirements

### Hoppscotch Desktop
- Fedora Linux 41 or later
- Dependencies (automatically installed):
  - `cairo`, `gdk-pixbuf2`, `gtk3`
  - `webkit2gtk4.1`
  - `openssl-libs`
  - `libsoup`, `pango`

### Hoppscotch CLI
- Fedora Linux 41 or later
- Node.js 22.0.0 or later

## 🚀 Installation

### Quick Install (Pre-built RPMs)

#### Add Copr
```bash
sudo dnf copr enable anifyuliansyah/hoppscotch
```

#### Desktop
```bash
sudo dnf install hoppscotch-desktop
```

#### CLI
```bash
sudo dnf install hoppscotch-cli
```

### Manual Installation

#### 1. Install build dependencies

**For Desktop:**
```bash
sudo dnf install rpmdevtools rpmlint binutils tar gzip
```

**For CLI:**
```bash
sudo dnf install rpmdevtools rpmlint nodejs npm git
```

#### 2. Setup RPM build environment
```bash
rpmdev-setuptree
```

#### 3. Download spec files
```bash
cd ~/rpmbuild/SPECS
wget https://raw.githubusercontent.com/Anifyuli/hoppscotch-rpm/main/hoppscotch-desktop.spec
wget https://raw.githubusercontent.com/Anifyuli/hoppscotch-rpm/main/hoppscotch-cli.spec
```

## 🔨 Building from Source

### Hoppscotch Desktop

#### 1. Download source
```bash
cd ~/rpmbuild/SPECS
spectool -g -R hoppscotch-desktop.spec
```

#### 2. Build RPM
```bash
rpmbuild -ba hoppscotch-desktop.spec
```

#### 3. Install
```bash
sudo dnf install ~/rpmbuild/RPMS/x86_64/hoppscotch-desktop-*.rpm
```

### Hoppscotch CLI

#### 1. Download source
```bash
cd ~/rpmbuild/SPECS
spectool -g -R hoppscotch-cli.spec
```

**Note:** This will download a ~200MB tarball from GitHub. Ensure you have a stable internet connection.

#### 2. Build RPM
```bash
rpmbuild -ba hoppscotch-cli.spec
```

**Note:** Building CLI requires significant time (15-30 minutes) and resources as it compiles from source using pnpm workspace.

#### 3. Install
```bash
sudo dnf install ~/rpmbuild/RPMS/x86_64/hoppscotch-cli-*.rpm
```

## 💻 Usage

### Desktop Application

Launch from your application menu (Development → Hoppscotch) or via command line:

```bash
hoppscotch-desktop
```

#### Wayland Compatibility

The package includes a wrapper script with WebKit optimizations for Wayland. To customize:

```bash
# Disable workarounds if you experience issues
WEBKIT_DISABLE_COMPOSITING_MODE=0 WEBKIT_DISABLE_DMABUF_RENDERER=0 hoppscotch-desktop

# Force X11 backend
GDK_BACKEND=x11 hoppscotch-desktop
```

### CLI Tool

```bash
# Show version
hopp --version

# Show help
hopp --help

# Test a collection
hopp test collection.json

# Test with environment
hopp test collection.json --env production.json

# Run in CI mode (non-interactive)
hopp test collection.json --ci

# Output results as JSON
hopp test collection.json --reporter json > results.json
```

## 🗂️ Package Details

### Desktop

| Item | Location |
|------|----------|
| Binary | `/usr/bin/hoppscotch-desktop` |
| Actual binary | `/usr/bin/hoppscotch-desktop-bin` |
| Desktop file | `/usr/share/applications/Hoppscotch.desktop` |
| Icons | `/usr/share/icons/hicolor/{32x32,128x128,256x256@2}/apps/` |
| Categories | Development |

**Note:** The binary is wrapped with a shell script that sets WebKit environment variables for better Wayland compatibility.

### CLI

| Item | Location |
|------|----------|
| Binary | `/usr/bin/hopp` |
| Package files | `/usr/lib/node_modules/@hoppscotch/cli/` |
| Build system | pnpm workspace (monorepo) |
| Source | GitHub release tags |

## 🔧 Troubleshooting

### Desktop Issues

<details>
<summary><b>Black screen or rendering problems</b></summary>

Try different WebKit configurations:

```bash
# Disable both workarounds
WEBKIT_DISABLE_COMPOSITING_MODE=0 WEBKIT_DISABLE_DMABUF_RENDERER=0 hoppscotch-desktop

# Try only disabling DMABUF
WEBKIT_DISABLE_DMABUF_RENDERER=0 hoppscotch-desktop

# Force X11 (if using Xorg)
GDK_BACKEND=x11 hoppscotch-desktop
```
</details>

<details>
<summary><b>Application doesn't appear in menu</b></summary>

Update desktop database and icon cache:

```bash
sudo update-desktop-database /usr/share/applications
sudo gtk-update-icon-cache /usr/share/icons/hicolor
```
</details>

<details>
<summary><b>OpenSSL errors</b></summary>

Ensure openssl-libs is installed:

```bash
sudo dnf install openssl-libs
```
</details>

### CLI Issues

<details>
<summary><b>Command not found</b></summary>

Verify Node.js version:

```bash
node --version  # Should be >= v22.0.0
```

Check binary exists:

```bash
ls -la /usr/bin/hopp
ls -la /usr/lib/node_modules/@hoppscotch/cli/
```
</details>

<details>
<summary><b>Build fails</b></summary>

Common causes:
1. **Insufficient memory** - Building requires at least 4GB RAM
2. **Old Node.js** - Update to Node.js 22+:
   ```bash
   sudo dnf install nodejs
   ```
3. **Network issues** - Ensure internet connection for pnpm to download dependencies
</details>

<details>
<summary><b>pnpm: command not found during build</b></summary>

This is normal. The spec file uses Node.js corepack to enable pnpm automatically during the build process.
</details>

## 📦 Version Information

| Package | Version | Source |
|---------|---------|--------|
| Desktop | 25.11.2-0 | [hoppscotch/releases](https://github.com/hoppscotch/releases) |
| CLI | 0.30.0 | [hoppscotch/hoppscotch](https://github.com/hoppscotch/hoppscotch) tag 2025.11.0 |

## 🔗 Links

- **Official Website:** https://hoppscotch.io
- **Documentation:** https://docs.hoppscotch.io
- **GitHub (Desktop):** https://github.com/hoppscotch/releases
- **GitHub (CLI & Web):** https://github.com/hoppscotch/hoppscotch
- **Community:** https://hoppscotch.io/discord

## 📜 License

Hoppscotch is licensed under the **MIT License**.

These RPM packages are also licensed under the **MIT License**.

## 🙏 Credits

- **Hoppscotch Team** - For creating this amazing tool
- **Gowtham2003** - Original AUR PKGBUILD maintainer
- **Fedora Community** - For packaging guidelines and tools

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Based on:
- [AUR hoppscotch-bin](https://aur.archlinux.org/packages/hoppscotch-bin) by Gowtham2003
- [Fedora Node.js Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Node.js/)
- [Fedora Desktop Application Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)

---

<div align="center">

**Made with ❤️ for the Fedora Community**

If you find this useful, please give it a ⭐!

</div>
