%define release_name Rawhide
%define is_rawhide 1

%define dist_version 35
%define rhel_dist_version 10

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%if 0%{?eln}
%bcond_with basic
%bcond_with cinnamon
%bcond_with cloud
%bcond_with compneuro
%bcond_with container
%bcond_with coreos
%bcond_with designsuite
%bcond_without eln
%bcond_with iot
%bcond_with kde
%bcond_with matecompiz
%bcond_with server
%bcond_with silverblue
%bcond_with kinoite
%bcond_with snappy
%bcond_with soas
%bcond_with workstation
%bcond_with xfce
%else
%bcond_without basic
%bcond_without cinnamon
%bcond_without cloud
%bcond_without compneuro
%bcond_without container
%bcond_without coreos
%bcond_without designsuite
%bcond_with eln
%bcond_without iot
%bcond_without kde
%bcond_without matecompiz
%bcond_without server
%bcond_without silverblue
%bcond_without kinoite
%bcond_without snappy
%bcond_without soas
%bcond_without workstation
%bcond_without xfce
%endif

# Changes should be submitted as pull requests under
#     https://src.fedoraproject.org/rpms/fedora-release

Summary:        Fedora release files
Name:           fedora-release
Version:        35
Release:        0.13%{?eln:.eln%{eln}}
License:        MIT
URL:            https://fedoraproject.org/

Source1:        LICENSE
Source2:        Fedora-Legal-README.txt

Source10:       85-display-manager.preset
Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset
Source14:       80-server.preset
Source15:       80-workstation.preset
Source16:       org.gnome.shell.gschema.override
Source17:       org.projectatomic.rpmostree1.rules
Source18:       80-iot.preset
Source19:       distro-template.swidtag
Source20:       distro-edition-template.swidtag
Source21:       gnome-shell.conf
Source22:       80-coreos.preset
Source23:       zezere-ignition-url
Source24:       80-iot-user.preset

BuildArch:      noarch

Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}

Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-basic if nothing else is already doing so.
Recommends:     fedora-release-identity-basic


BuildRequires:  redhat-rpm-config > 121-1
BuildRequires:  systemd-rpm-macros

%description
Fedora release files such as various /etc/ files that define the release
and systemd preset files that determine which services are enabled by default.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/ for details.


%package common
Summary: Fedora release files

Requires:   fedora-release-variant = %{version}-%{release}
Suggests:   fedora-release

Requires:   fedora-repos(%{version})
Requires:   fedora-release-identity = %{version}-%{release}

%if %{is_rawhide}
# Make $releasever return "rawhide" on Rawhide
# https://pagure.io/releng/issue/7445
Provides:       system-release(releasever) = %{releasever}
%endif

# Fedora ships a generic-release package to make the creation of Remixes
# easier, but it cannot coexist with the fedora-release[-*] packages, so we
# will explicitly conflict with it.
Conflicts:  generic-release

%description common
Release files common to all Editions and Spins of Fedora


%if %{with basic}
%package identity-basic
Summary:        Package providing the basic Fedora identity

RemovePathPostfixes: .basic
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-basic
Provides the necessary files for a Fedora installation that is not identifying
itself as a particular Edition or Spin.
%endif


%if %{with cinnamon}
%package cinnamon
Summary:        Base package for Fedora Cinnamon-specific default configurations

RemovePathPostfixes: .cinnamon
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-cinnamon if nothing else is already doing so.
Recommends:     fedora-release-identity-cinnamon


%description cinnamon
Provides a base package for Fedora Cinnamon-specific configuration files to
depend on as well as Cinnamon system defaults.


%package identity-cinnamon
Summary:        Package providing the identity for Fedora Cinnamon Spin

RemovePathPostfixes: .cinnamon
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-cinnamon
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Cinnamon.
%endif


%if %{with cloud}
%package cloud
Summary:        Base package for Fedora Cloud-specific default configurations

RemovePathPostfixes: .cloud
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-cloud if nothing else is already doing so.
Recommends:     fedora-release-identity-cloud


%description cloud
Provides a base package for Fedora Cloud-specific configuration files to
depend on.


%package identity-cloud
Summary:        Package providing the identity for Fedora Cloud Edition

RemovePathPostfixes: .cloud
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-cloud
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Cloud Edition.
%endif


%if %{with compneuro}
%package compneuro
Summary:        Base package for Fedora Comp Neuro specific default configurations

RemovePathPostfixes: .compneuro
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-compneuro if nothing else is already doing so.
Recommends:     fedora-release-identity-compneuro


%description compneuro
Provides a base package for Fedora Comp Neuro specific configuration files to
depend on as well as Comp Neuro system defaults.


%package identity-compneuro
Summary:        Package providing the identity for Fedora Comp Neuro Lab

RemovePathPostfixes: .compneuro
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-compneuro
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Comp Neuro Lab.
%endif


%if %{with container}
%package container
Summary:        Base package for Fedora container specific default configurations

RemovePathPostfixes: .container
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-container if nothing else is already doing so.
Recommends:     fedora-release-identity-container


%description container
Provides a base package for Fedora container specific configuration files to
depend on as well as container system defaults.


%package identity-container
Summary:        Package providing the identity for Fedora Container Base Image

RemovePathPostfixes: .container
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-container
Provides the necessary files for a Fedora installation that is identifying
itself as the Fedora Container Base Image.
%endif


%if %{with coreos}
%package coreos
Summary:        Base package for Fedora CoreOS-specific default configurations

RemovePathPostfixes: .coreos
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-coreos if nothing else is already doing so.
Recommends:     fedora-release-identity-coreos


%description coreos
Provides a base package for Fedora CoreOS Host-specific configuration files to
depend.


%package identity-coreos
Summary:        Package providing the identity for Fedora CoreOS

RemovePathPostfixes: .coreos
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-coreos
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora CoreOS.
%endif


%if %{with designsuite}
%package designsuite
Summary:        Base package for Fedora Design Suite specific default configurations

RemovePathPostfixes: .designsuite
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}
Provides:       system-release-product

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-designsuite if nothing else is already doing so.
Recommends:     fedora-release-identity-designsuite


%description designsuite
Provides a base package for Fedora Design Suite specific configuration files to
depend on.


%package identity-designsuite
Summary:        Package providing the identity for Fedora Design Suite Lab

RemovePathPostfixes: .designsuite
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-designsuite
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Design Suite Lab.
%endif


%if %{with eln}
%package eln
Summary:        Base package for Fedora ELN specific default configurations

RemovePathPostfixes: .eln
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:eln)
Requires:       fedora-release-common = %{version}-%{release}
Provides:       system-release-product
Requires:       fedora-repos-eln

Obsoletes:      redhat-release
Provides:       redhat-release

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-eln if nothing else is already doing so.
Recommends:     fedora-release-identity-eln


%description eln
Provides a base package for Fedora ELN specific configuration files to
depend on.


%package identity-eln
Summary:        Package providing the identity for Fedora ELN

RemovePathPostfixes: .eln
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-eln
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora ELN.
%endif


%if %{with iot}
%package iot
Summary:        Base package for Fedora IoT specific default configurations

RemovePathPostfixes: .iot
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}
Requires:       fedora-release-ostree-counting = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-iot if nothing else is already doing so.
Recommends:     fedora-release-identity-iot


%description iot
Provides a base package for Fedora IoT specific configuration files to
depend on as well as IoT system defaults.


%package identity-iot
Summary:        Package providing the identity for Fedora IoT Edition

RemovePathPostfixes: .iot
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-iot
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora IoT Edition.
%endif


%if %{with kde}
%package kde
Summary:        Base package for Fedora KDE Plasma-specific default configurations

RemovePathPostfixes: .kde
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-kde if nothing else is already doing so.
Recommends:     fedora-release-identity-kde


%description kde
Provides a base package for Fedora KDE Plasma-specific configuration files to
depend on as well as KDE Plasma system defaults.


%package identity-kde
Summary:        Package providing the identity for Fedora KDE Plasma Spin

RemovePathPostfixes: .kde
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-kde
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora KDE Plasma Spin.
%endif


%if %{with matecompiz}
%package matecompiz
Summary:        Base package for Fedora MATE-Compiz-specific default configurations

RemovePathPostfixes: .matecompiz
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-matecompiz if nothing else is already doing so.
Recommends:     fedora-release-identity-matecompiz


%description matecompiz
Provides a base package for Fedora MATE-compiz-specific configuration files to
depend on as well as MATE-Compiz system defaults.


%package identity-matecompiz
Summary:        Package providing the identity for Fedora MATE-Compiz Spin

RemovePathPostfixes: .matecompiz
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-matecompiz
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora MATE-Compiz.
%endif


%if %{with server}
%package server
Summary:        Base package for Fedora Server-specific default configurations

RemovePathPostfixes: .server
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-server if nothing else is already doing so.
Recommends:     fedora-release-identity-server


%description server
Provides a base package for Fedora Server-specific configuration files to
depend on.


%package identity-server
Summary:        Package providing the identity for Fedora Server Edition

RemovePathPostfixes: .server
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-server
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Server Edition.
%endif


%if %{with silverblue}
%package silverblue
Summary:        Base package for Fedora Silverblue-specific default configurations

RemovePathPostfixes: .silverblue
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}
Requires:       fedora-release-ostree-counting = %{version}-%{release}
Requires:       fedora-release-ostree-desktop = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-silverblue if nothing else is already doing so.
Recommends:     fedora-release-identity-silverblue


%description silverblue
Provides a base package for Fedora Silverblue-specific configuration files to
depend on as well as Silverblue system defaults.


%package identity-silverblue
Summary:        Package providing the identity for Fedora Silverblue

RemovePathPostfixes: .silverblue
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-silverblue
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Silverblue.
%endif


%if %{with kinoite}
%package kinoite
Summary:        Base package for Fedora Kinoite-specific default configurations

RemovePathPostfixes: .kinoite
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}
Requires:       fedora-release-ostree-counting = %{version}-%{release}
Requires:       fedora-release-ostree-desktop = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-kinoite if nothing else is already doing so.
Recommends:     fedora-release-identity-kinoite


%description kinoite
Provides a base package for Fedora Kinoite-specific configuration files to
depend on as well as Kinoite system defaults.


%package identity-kinoite
Summary:        Package providing the identity for Fedora Kinoite

RemovePathPostfixes: .kinoite
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-kinoite
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Kinoite.
%endif


%if %{with silverblue} || %{with iot} || %{with kinoite}
%package ostree-counting
Summary:        Configuration package for rpm-ostree variants to enable counting

%description ostree-counting
Configuration package for rpm-ostree variants to enable counting
%endif


%if %{with silverblue} || %{with kinoite}
%package ostree-desktop
Summary:        Configuration package for rpm-ostree variants to add rpm-ostree polkit rules

%description ostree-desktop
Configuration package for rpm-ostree variants to add rpm-ostree polkit rules
%endif


%if %{with snappy}
%package snappy
Summary:        Base package for Fedora snap specific default configurations

RemovePathPostfixes: .snappy
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-snappy if nothing else is already doing so.
Recommends:     fedora-release-identity-snappy


%description snappy
Provides a base package for Fedora snap specific configuration files to
depend on as well as Snappy system defaults.


%package identity-snappy
Summary:        Package providing the identity for Fedora Snappy environments

RemovePathPostfixes: .snappy
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-snappy
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora's snappy environment.
%endif


%if %{with soas}
%package soas
Summary:        Base package for Fedora Sugar on a Stick-specific default configurations

RemovePathPostfixes: .soas
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-soas if nothing else is already doing so.
Recommends:     fedora-release-identity-soas


%description soas
Provides a base package for Fedora Sugar on a Stick-specific configuration
files to depend on as well as SoaS system defaults.


%package identity-soas
Summary:        Package providing the identity for Fedora Sugar on a Stick

RemovePathPostfixes: .soas
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-soas
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Sugar on a Stick.
%endif


%if %{with workstation}
%package workstation
Summary:        Base package for Fedora Workstation-specific default configurations

RemovePathPostfixes: .workstation
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}
Provides:       system-release-product

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-workstation if nothing else is already doing so.
Recommends:     fedora-release-identity-workstation


%description workstation
Provides a base package for Fedora Workstation-specific configuration files to
depend on.


%package identity-workstation
Summary:        Package providing the identity for Fedora Workstation Edition

RemovePathPostfixes: .workstation
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-workstation
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Workstation Edition.
%endif


%if %{with xfce}
%package xfce
Summary:        Base package for Fedora Xfce specific default configurations

RemovePathPostfixes: .xfce
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-xfce if nothing else is already doing so.
Recommends:     fedora-release-identity-xfce


%description xfce
Provides a base package for Fedora Xfce specific configuration files to
depend on as well as Xfce system defaults.


%package identity-xfce
Summary:        Package providing the identity for Fedora Xfce Spin

RemovePathPostfixes: .xfce
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity


%description identity-xfce
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Xfce.
%endif


%prep
sed -i 's|@@VERSION@@|%{dist_version}|g' %{SOURCE2}

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Fedora release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}
%define starts_with(str,prefix) (%{expand:%%{lua:print(starts_with(%1, %2) and "1" or "0")}})
%if %{starts_with "a%{release}" "a0"}
  %global prerelease \ Prerelease
%endif

cat << EOF >> os-release
NAME="Fedora Linux"
VERSION="%{dist_version} (%{release_name}%{?prerelease})"
ID=fedora
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PLATFORM_ID="platform:f%{dist_version}"
PRETTY_NAME="Fedora Linux %{dist_version} (%{release_name}%{?prerelease})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:%{dist_version}"
HOME_URL="https://fedoraproject.org/"
DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora/%{doc_version}/system-administrators-guide/"
SUPPORT_URL="https://fedoraproject.org/wiki/Communicating_and_getting_help"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL="https://fedoraproject.org/wiki/Legal:PrivacyPolicy"
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different editions

%if %{with basic}
# Basic
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic
%endif

%if %{with cinnamon}
# Cinnamon
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.cinnamon
echo "VARIANT=\"Cinnamon\"" >> %{buildroot}%{_prefix}/lib/os-release.cinnamon
echo "VARIANT_ID=cinnamon" >> %{buildroot}%{_prefix}/lib/os-release.cinnamon
sed -i -e "s|(%{release_name}%{?prerelease})|(Cinnamon%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.cinnamon
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Cinnamon/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cinnamon
%endif

%if %{with cloud}
# Cloud
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT=\"Cloud Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT_ID=cloud" >> %{buildroot}%{_prefix}/lib/os-release.cloud
sed -i -e "s|(%{release_name}%{?prerelease})|(Cloud Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.cloud
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Cloud/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cloud
%endif

%if %{with compneuro}
# Comp Neuro
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.compneuro
echo "VARIANT=\"Comp Neuro\"" >> %{buildroot}%{_prefix}/lib/os-release.compneuro
echo "VARIANT_ID=compneuro" >> %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e "s|(%{release_name}%{?prerelease})|(CompNeuro%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://neuro.fedoraproject.org"|' %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e 's|HOME_URL=.*|HOME_URL="https://labs.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.compneuro
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/CompNeuro/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.compneuro
%endif

%if %{with container}
# Container
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT=\"Container Image\"" >> %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT_ID=container" >> %{buildroot}%{_prefix}/lib/os-release.container
sed -i -e "s|(%{release_name}%{?prerelease})|(Container Image%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.container
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Container/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.container
%endif

%if %{with coreos}
# CoreOS
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.coreos
echo "VARIANT=\"CoreOS\"" >> %{buildroot}%{_prefix}/lib/os-release.coreos
echo "VARIANT_ID=coreos" >> %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e "s|(%{release_name}%{?prerelease})|(CoreOS%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-coreos/"|' %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e 's|HOME_URL=.*|HOME_URL="https://getfedora.org/coreos/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|SUPPORT_URL=.*|SUPPORT_URL="https://github.com/coreos/fedora-coreos-tracker/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://github.com/coreos/fedora-coreos-tracker/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Fedora CoreOS %{dist_version}"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/CoreOS/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.coreos
install -Dm0644 %{SOURCE22} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif


%if %{with designsuite}
# Design Suite
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.designsuite
echo "VARIANT=\"Design Suite\"" >> %{buildroot}%{_prefix}/lib/os-release.designsuite
echo "VARIANT_ID=designsuite" >> %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e "s|(%{release_name}%{?prerelease})|(Design Suite%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://fedoraproject.org/wiki/Design_Suite"|' %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e 's|HOME_URL=.*|HOME_URL="https://labs.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.designsuite
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/DesignSuite/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.designsuite
%endif

%if %{with eln}
# ELN
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT=\"ELN\"" >> %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT_ID=eln" >> %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e 's|PLATFORM_ID=.*|PLATFORM_ID="platform:eln"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Fedora ELN"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/eln/"|' %{buildroot}%{_prefix}/lib/os-release.eln
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/ELN/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif

%if %{with iot}
# IoT
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.iot
echo "VARIANT=\"IoT Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.iot
echo "VARIANT_ID=iot" >> %{buildroot}%{_prefix}/lib/os-release.iot
sed -i -e "s|(%{release_name}%{?prerelease})|(IoT Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.iot
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/IoT/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.iot
install -p %{SOURCE23} %{buildroot}/%{_prefix}/lib/
install -Dm0644 %{SOURCE18} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE24} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
%endif

%if %{with kde}
# KDE Plasma
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT=\"KDE Plasma\"" >> %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT_ID=kde" >> %{buildroot}%{_prefix}/lib/os-release.kde
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
%endif

%if %{with matecompiz}
# MATE-Compiz
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.matecompiz
echo "VARIANT=\"MATE-Compiz\"" >> %{buildroot}%{_prefix}/lib/os-release.matecompiz
echo "VARIANT_ID=matecompiz" >> %{buildroot}%{_prefix}/lib/os-release.matecompiz
sed -i -e "s|(%{release_name}%{?prerelease})|(MATE-Compiz%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.matecompiz
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/MATE-Compiz/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.matecompiz
%endif

%if %{with server}
# Server
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT=\"Server Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT_ID=server" >> %{buildroot}%{_prefix}/lib/os-release.server
sed -i -e "s|(%{release_name}%{?prerelease})|(Server Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.server
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Server/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
install -Dm0644 %{SOURCE14} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif

%if %{with silverblue}
# Silverblue
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.silverblue
echo "VARIANT=\"Silverblue\"" >> %{buildroot}%{_prefix}/lib/os-release.silverblue
echo "VARIANT_ID=silverblue" >> %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -i -e "s|(%{release_name}%{?prerelease})|(Silverblue%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-silverblue/"|' %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Silverblue/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.silverblue
%endif

%if %{with kinoite}
# Kinoite
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kinoite
echo "VARIANT=\"Kinoite\"" >> %{buildroot}%{_prefix}/lib/os-release.kinoite
echo "VARIANT_ID=kinoite" >> %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -i -e "s|(%{release_name}%{?prerelease})|(Kinoite%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-kinoite/"|' %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Kinoite/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kinoite
%endif

%if %{with snappy}
# Snappy
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.snappy
echo "VARIANT=\"Snappy\"" >> %{buildroot}%{_prefix}/lib/os-release.snappy
echo "VARIANT_ID=snappy" >> %{buildroot}%{_prefix}/lib/os-release.snappy
sed -i -e "s|(%{release_name}%{?prerelease})|(Snappy%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.snappy
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Snappy/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.snappy
%endif

%if %{with soas}
# Sugar on a Stick
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.soas
echo "VARIANT=\"Sugar on a Stick\"" >> %{buildroot}%{_prefix}/lib/os-release.soas
echo "VARIANT_ID=soas" >> %{buildroot}%{_prefix}/lib/os-release.soas
sed -i -e "s|(%{release_name}%{?prerelease})|(Sugar on a Stick%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.soas
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Sugar/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.soas
%endif

%if %{with workstation}
# Workstation
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT=\"Workstation Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT_ID=workstation" >> %{buildroot}%{_prefix}/lib/os-release.workstation
sed -i -e "s|(%{release_name}%{?prerelease})|(Workstation Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.workstation
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Workstation/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
# Add gnome-shell to dnf protected packages list for Workstation
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with silverblue} || %{with workstation}
# Silverblue and Workstation
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Override the list of enabled gnome-shell extensions for Workstation
install -Dm0644 %{SOURCE16} -t %{buildroot}%{_datadir}/glib-2.0/schemas/
%endif

%if %{with silverblue} || %{with kinoite}
# Install rpm-ostree polkit rules
install -Dm0644 %{SOURCE17} -t %{buildroot}%{_datadir}/polkit-1/rules.d/
%endif

%if %{with silverblue} || %{with iot} || %{with kinoite}
# Pull Count Me timer for rpm-ostreed
install -dm0755 %{buildroot}%{_unitdir}/rpm-ostreed.service.wants/
ln -snf %{_unitdir}/rpm-ostree-countme.timer %{buildroot}%{_unitdir}/rpm-ostreed.service.wants/
%endif

%if %{with xfce}
# Xfce
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT=\"Xfce\"" >> %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT_ID=xfce" >> %{buildroot}%{_prefix}/lib/os-release.xfce
sed -i -e "s|(%{release_name}%{?prerelease})|(Xfce%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.xfce
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Xfce/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.xfce
%endif

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release


# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%if 0%{?eln}
%%rhel              %{rhel_dist_version}
%%el%{rhel_dist_version}                1
# Although eln is set in koji tags, we put it in the macros.dist file for local and mock builds.
%%eln              %{eln}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%%{eln}%%{?with_bootstrap:%{__bootstrap}}
%else
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.fc%%{fedora}%%{?with_bootstrap:%{__bootstrap}}
%endif
EOF

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/Fedora-Legal-README.txt

# Default system wide
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s %{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/fedoraproject.org


%files common
%license licenses/LICENSE licenses/Fedora-Legal-README.txt
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif


%if %{with cinnamon}
%files cinnamon
%files identity-cinnamon
%{_prefix}/lib/os-release.cinnamon
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cinnamon
%endif


%if %{with cloud}
%files cloud
%files identity-cloud
%{_prefix}/lib/os-release.cloud
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cloud
%endif


%if %{with compneuro}
%files compneuro
%files identity-compneuro
%{_prefix}/lib/os-release.compneuro
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.compneuro
%endif


%if %{with container}
%files container
%files identity-container
%{_prefix}/lib/os-release.container
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.container
%endif


%if %{with coreos}
%files coreos
%files identity-coreos
%{_prefix}/lib/systemd/system-preset/80-coreos.preset
%{_prefix}/lib/os-release.coreos
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.coreos
%endif


%if %{with designsuite}
%files designsuite
%files identity-designsuite
%{_prefix}/lib/os-release.designsuite
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.designsuite
%endif


%if %{with eln}
%files eln
%files identity-eln
%{_prefix}/lib/os-release.eln
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif


%if %{with iot}
%files iot
%files identity-iot
%{_prefix}/lib/os-release.iot
%{_prefix}/lib/systemd/system-preset/80-iot.preset
%{_prefix}/lib/systemd/user-preset/80-iot-user.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.iot
%{_prefix}/lib/zezere-ignition-url
%endif


%if %{with kde}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
%endif


%if %{with matecompiz}
%files matecompiz
%files identity-matecompiz
%{_prefix}/lib/os-release.matecompiz
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.matecompiz
%endif


%if %{with server}
%files server
%files identity-server
%{_prefix}/lib/os-release.server
%{_prefix}/lib/systemd/system-preset/80-server.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
%endif


%if %{with silverblue}
%files silverblue
%files identity-silverblue
%{_prefix}/lib/os-release.silverblue
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.silverblue
# Keep this in sync with workstation below
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%endif


%if %{with kinoite}
%files kinoite
%files identity-kinoite
%{_prefix}/lib/os-release.kinoite
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kinoite
%endif


%if %{with silverblue} || %{with iot} || %{with kinoite}
%files ostree-counting
%{_unitdir}/rpm-ostreed.service.wants/rpm-ostree-countme.timer
%endif


%if %{with silverblue} || %{with kinoite}
%files ostree-desktop
%attr(0644,root,root) %{_prefix}/share/polkit-1/rules.d/org.projectatomic.rpmostree1.rules
%endif


%if %{with snappy}
%files snappy
%files identity-snappy
%{_prefix}/lib/os-release.snappy
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.snappy
%endif


%if %{with soas}
%files soas
%files identity-soas
%{_prefix}/lib/os-release.soas
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.soas
%endif


%if %{with workstation}
%files workstation
%files identity-workstation
%{_prefix}/lib/os-release.workstation
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
%{_sysconfdir}/dnf/protected.d/gnome-shell.conf
# Keep this in sync with silverblue above
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%endif


%if %{with xfce}
%files xfce
%files identity-xfce
%{_prefix}/lib/os-release.xfce
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.xfce
%endif


%changelog
* Mon Jul 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 35-0.13
- Shuffle some power/resource management presets so all variants can use them

* Fri Jul 23 2021 Neal Gompa <ngompa@fedoraproject.org> - 35-0.12
- user session: drop duplicate pipewire-pulse preset

* Wed Jul 14 2021 Kevin Fenzi <kevin@scrye.com> - 35-0.11
- user session: wireplumber.service and pipewire-pulse.socket 

* Tue Jul 13 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.10
- user session: enable pipewire-media-session.service

* Fri Apr 30 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.9
- Change PRETTY_NAME to "Fedora Linux"

* Fri Apr 30 2021 Ben Cotton <bcotton@fedoraproject.org> - 35-0.8
- Automatically set the version in Fedora-Legal-README.txt

* Tue Apr 13 2021 Timothée Ravier <travier@redhat.com> - 35-0.7
- Add ostree-counting & ostree-desktop subpackages

* Thu Apr 01 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.6
- Enable certbot-renew.timer (bz1942011)

* Wed Mar 17 2021 Timothée Ravier <travier@redhat.com> - 35-0.5
- Add Fedora Kinoite variant sub package

* Wed Mar 17 2021 Timothée Ravier <travier@redhat.com> - 35-0.4
- Enable Count Me timer for Silverblue and IoT

* Sat Feb 20 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.3
- Update rhel_dist_version to track RHEL 10

* Tue Feb 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 35-0.2
- Remove earlyoom preset from workstation and kde identities
  (replaced by systemd-oomd)

* Tue Feb 09 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.1
- Setup for rawhide being F35

* Tue Jan 19 2021 Allison Karlitskaya <allison.karlitskaya@redhat.com> - 34-0.11
- Enable rpm-ostree repo-refresh for all active local users
- https://github.com/fedora-silverblue/issue-tracker/issues/55

* Tue Dec 15 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.10
- Enable pipewire-pulse socket-activated user service (ngompa)
- Fixing changelog

* Wed Oct 28 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.9
- Spec file and ELN improvements
- Conditionalize the creation of the identity subpackages
- Allow ELN to skip building all of the other Fedora identities
- Have ELN be the provider of the `redhat-release` virtual provides

* Fri Oct 23 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.8
- Enable power-profiles-daemon by default
- https://pagure.io/fedora-workstation/issue/191

* Wed Oct 14 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.7
- Enable low-memory-monitor for GMemoryMonitor API (hadess)

* Fri Oct 09 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.6
- Add ELN support to fedora-release (sgallagh)

* Thu Sep 17 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 34-0.5
- IoT: Enable parsec and dbus-parsec services

* Tue Aug 25 2020 Kalev Lember <klember@redhat.com> - 34-0.4
- Add gnome-shell to dnf protected packages list for Workstation

* Mon Aug 17 2020 Troy Dawson <tdawson@redhat.com> - 34-0.3
- Change release if building for eln

* Tue Aug 11 2020 Troy Dawson <tdawson@redhat.com> - 34-0.2
- Set %rhel and %eln when appropriate

* Mon Aug 10 2020 Tomas Hrcka <thrcka@redhat.com> - 34-0.1
- Setup for rawhide being F34

* Mon Aug 10 2020 Troy Dawson <tdawson@redhat.com> - 33-0.11
- No %fedora set for eln

* Thu Aug 06 2020 Ben Cotton <bcotton@fedoraproject.org> - 33-0.10
- KDE: Add EarlyOOM by default

* Fri Jun 05 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.9
- iot: Remove preset for greenboot.service (lorbus)

* Mon May 04 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.8
- Fix incorrect prerelease labeling for Editions and Spins
- Resolves: rhbz#1831102

* Tue Apr 21 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.7
- Add new "identity" subpackages to allow Edition and Spin environment groups
  to be installed together.

* Mon Apr 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.6
- Add "Prerelease" notation to PRETTY_NAME and VERSION in os-release

* Sun Apr 12 2020 Kevin Fenzi <kevin@scrye.com> - 33-0.5
- Update color to Fedora blue. Fixes bug #1823099

* Wed Apr 01 2020 Christian Glombek <cglombek@redhat.com> 33-0.4
- Add IoT user preset to disable grub-boot-success.timer
- Update links in 80-coreos.preset

* Fri Mar 20 2020 Patrick Uiterwijk <puiterwijk@redhat.com> 33-0.3
- Enable IoT provisioning service

* Wed Mar 18 2020 Peter Robinson <pbrobinson@fedoraproject.org> 33-0.2
- Add IoT provisioning URL config
- Enable fstrim.timer (crobinso)
- Enable kata-osbuilder-generate.service (crobinso)

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.1
- Setup for rawhide being F33

* Fri Feb  7 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 32-0.5
- Add 'disable *' default preset for user units (#1468501)

* Wed Oct 30 2019 Peter Robinson <pbrobinson@fedoraproject.org> 32-0.4
- Drop clevis IoT defaults change

* Mon Oct 21 2019 Michael Nguyen <mnguyen@redhat.com> - 32-0.3
- Update os-release information for Fedora CoreOS

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 32-0.2
- RPM macros: Redefining %%fedora now changes %%dist

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Setup for rawhide being F32
- Disable zram-swap service (sgallagh)

* Sat Aug 10 2019 Tom Callaway <spot@fedoraproject.org> - 31-0.9
- update legal text (reflect current release, refer to Fedora OS instead of Fedora)

* Sat Jul 13 2019 Colin Walters <walters@verbum.org> - 31-0.8
- Sync Silverblue with Workstation
  In particular, it should have the same "ssh disabled by default" etc.
  https://discussion.fedoraproject.org/t/strange-etc-os-release-contents-on-silverblue/2024/2
- Enable zram-swap on workstation installations
- Enable the session agent for snaps

* Thu Jun 06 2019 Stephen Gallagher <sgallagh@redhat.com> - 31-0.7
- Work around upgrade bug
- Resolves: rhbz#1710543

* Tue May 14 2019 Robert Fairley <rfairley@redhat.com> - 31-0.6
- Remove presets from 80-coreos.preset and add note referring to FCOS overlay RPM

* Wed Apr 10 2019 Stephen Gallagher <sgallagh@redhat.com> - 31-0.5
- Add Provides for the base module for Fedora (BZ #1688462)

* Mon Apr 8 2019 Michael Nguyen <mnguyen@redhat.com> - 31-0.4
- Add presets for CoreOS

* Thu Apr 04 2019 Kalev Lember <klember@redhat.com> - 31-0.3
- Enable the Fedora flatpak repos service (#1696225)

* Wed Mar 20 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 31-0.2
- Allow bootstrap suffix to be overridden.

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for rawhide being f30

* Fri Feb 15 2019 Sinny Kumari <skumari@redhat.com> - 30-0.23
- Don't build AtomicHost from F30 and onward releases in favor of coreos

* Fri Feb 08 2019 David Rheinsberg <david.rheinsberg@gmail.com> - 30-0.22
- Enable dbus-broker over dbus-daemon, to make new installs use the broker as
  new system- and user-bus implementation.

* Sun Feb 03 2019 Neal Gompa <ngompa13@gmail.com> - 30-0.21
- Add snappy variant

* Fri Jan 18 2019 Robert Fairley <rfairley@redhat.com> - 30-0.20
- Own /etc/issue.d directory.

* Fri Dec 28 2018 Kevin Fenzi <kevin@scrye.com> - 30-0.19
- Own /etc/swid directory.

* Wed Dec 12 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.18
- Include empty VERSION_CODENAME= field in os-release

* Tue Dec 11 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.17
- Use the icon logo for `LOGO`

* Mon Dec 03 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.16
- Add 'LOGO' to os-release(5) for Fedora
- Enable the Docker daemon socket

* Tue Nov 27 2018 Peter Robinson <pbrobinson@fedoraproject.org> 30-0.15
- Add IoT config to fix policy around TPM2 requirements

* Thu Nov 15 2018 Jan Pazdziora <jpazdziora@redhat.com> - 30-0.14
- Fix the supplemental edition SWID tag, add the supplemental attribute.

* Sun Nov 11 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.13
- Drop unneeded Requires(post) and Requires(postun) dependencies causing
  loops. The glib-compile-schemas dependency is now handled by file triggers
  and the systemd requirement was just completely erroneous.
- Also drop strict dependencies on edition packages. They are causing
  un-breakable dependency loops.

* Tue Oct 23 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.12
- Convert to more maintainable implementation of variant-handling

* Thu Oct 11 2018 Jan Pazdziora <jpazdziora@redhat.com> 30-0.10
- Add edition supplemental .swidtag files, and amend convert-to-edition.lua
  to keep symlink to the correct one in sync with os-release.
- Produce distro-level SWID tag in /usr/lib/swidtag/fedoraproject.org.
- Enable ostree-finalize-staged.path

* Mon Sep 24 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.9
- Enable the stratis daemon for managing stratis storage

* Fri Sep 14 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.8
- Set cpi.service as enabled in the systemd presets
- Set device_cio_free service as enabled

* Mon Aug 27 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.7
- Remove specialized handling for /etc/issue.
- Drop convert-to-edition script

* Fri Aug 24 2018 Matthew Miller <mattdm@fedoraproject.org> - 30-0.6
- add container
- add coreos
- add desktop spins

* Thu Aug 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 30-0.5
- Add Fedora IoT edition components

* Mon Aug 20 2018 Jun Aruga <jaruga@redhat.com> - 30-0.4
- Update dist macro to consider bootstrapping.

* Sat Aug 18 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 30-0.3
- Escape use of the distprefix macro, so it makes it into the macro
  file instead of being expanded in the spec.

* Wed Aug 15 2018 David Herrmann <dh.herrmann@gmail.com> - 30-0.2
- Enable dbus user units explicitly

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for rawhide being f30
