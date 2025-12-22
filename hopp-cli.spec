%global debug_package %{nil}
%global gittag 2025.11.0
%global appversion 0.30.0

# Fallback if nodejs macros are not present
%{!?nodejs_sitelib:%global nodejs_sitelib %{_prefix}/lib/node_modules}

Name:           hoppscotch-cli
Version:        %{appversion}
Release:        1%{?dist}
Summary:        CLI to run Hoppscotch Test Scripts in CI environments

License:        MIT
URL:            https://hoppscotch.io/
Source0:        https://github.com/hoppscotch/hoppscotch/archive/refs/tags/%{gittag}.tar.gz

ExclusiveArch:  %{nodejs_arches}

BuildRequires:  nodejs >= 22
BuildRequires:  pnpm
BuildRequires:  git
BuildRequires:  python3
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  brotli-devel
BuildRequires:  libuv-devel

Requires:       nodejs >= 22

%description
A CLI to run Hoppscotch Test Scripts in CI environments.

This package is built from source using the upstream pnpm workspace.
Due to the use of workspace-scoped dependencies, the CLI is bundled
using pnpm deploy as a production-ready dependency tree.

%prep
%autosetup -n hoppscotch-%{gittag}

%build
pnpm install --frozen-lockfile --ignore-scripts

pnpm -r --filter @hoppscotch/data build
pnpm -r --filter @hoppscotch/js-sandbox build
pnpm -r --filter @hoppscotch/kernel build
pnpm -r --filter @hoppscotch/cli build

# PRODUCE PRODUCTION RUNTIME TREE
pnpm --filter @hoppscotch/cli deploy %{_builddir}/cli-prod --prod --legacy

%install
rm -rf %{buildroot}

cat > .npmrc <<'EOF'
node-linker=hoisted
EOF

pnpm deploy \
  --filter @hoppscotch/cli \
  --prod --legacy \
  --no-optional \
  %{buildroot}%{nodejs_sitelib}/@hoppscotch/cli

rm -f .npmrc

# Install full production tree
mkdir -p %{buildroot}%{_bindir}
ln -s ../lib/node_modules/@hoppscotch/cli/bin/hopp.js %{buildroot}%{_bindir}/hopp

%check
test -f %{buildroot}%{nodejs_sitelib}/@hoppscotch/cli/bin/hopp.js

%files
%license LICENSE
%doc packages/hoppscotch-cli/README.md
%{nodejs_sitelib}/@hoppscotch/cli
%{_bindir}/hopp

%changelog
* Sun Dec 21 2025 Moh. Anif Yuliansyah <anifyuli007@outlook.co.id> - 0.30.0-1
- Initial RPM build from Hoppscotch %{gittag}
- Built using pnpm workspace and deploy --legacy
- Bundled CLI with production dependencies
