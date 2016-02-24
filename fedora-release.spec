%define release_name Rawhide
%define dist_version 25
%define bug_version rawhide

Summary:        Fedora release files
Name:           fedora-release
Version:        25
Release:        0.1
License:        MIT
Group:          System Environment/Base
URL:            http://fedoraproject.org
Source:         %{name}-%{version}.tar.bz2
Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})

# Kill off the fedora-release-nonproduct package
Provides:       fedora-release-nonproduct = %{version}
Obsoletes:      fedora-release-nonproduct <= 23-0.3
Provides:       fedora-release-standard = 22-0.8
Obsoletes:      fedora-release-standard < 22-0.8


Requires:       fedora-repos(%{version})
BuildArch:      noarch

%description
Fedora release files such as various /etc/ files that define the release.

%package cloud
Summary:        Base package for Fedora Cloud-specific default configurations
Provides:       system-release-cloud
Provides:       system-release-cloud(%{version})
Provides:       system-release-product
Requires:       fedora-release = %{version}-%{release}

%description cloud
Provides a base package for Fedora Cloud-specific configuration files to
depend on.

%package server
Summary:        Base package for Fedora Server-specific default configurations
Provides:       system-release-server
Provides:       system-release-server(%{version})
Provides:       system-release-product
Requires:       fedora-release = %{version}-%{release}
Requires:       systemd
Requires:       cockpit
Requires:       rolekit
Requires(post):	sed
Requires(post):	systemd

%description server
Provides a base package for Fedora Server-specific configuration files to
depend on.

%package workstation
Summary:        Base package for Fedora Workstation-specific default configurations
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Provides:       system-release-product
Requires:       fedora-release = %{version}-%{release}
# needed for captive portal support
Requires:       NetworkManager-config-connectivity-fedora
Requires(post): /usr/bin/glib-compile-schemas
Requires(postun): /usr/bin/glib-compile-schemas

%description workstation
Provides a base package for Fedora Workstation-specific configuration files to
depend on.

%prep
%setup -q
sed -i 's|@@VERSION@@|%{dist_version}|g' Fedora-Legal-README.txt

%build

%install
install -d $RPM_BUILD_ROOT/etc
echo "Fedora release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe

# Symlink the -release files
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>$RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora
NAME=Fedora
VERSION="%{dist_version} (%{release_name})"
ID=fedora
VERSION_ID=%{dist_version}
PRETTY_NAME="Fedora %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:fedoraproject:fedora:%{dist_version}"
HOME_URL="https://fedoraproject.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL=https://fedoraproject.org/wiki/Legal:PrivacyPolicy
EOF

# Create the common /etc/issue
echo "\S" > $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora

# Create /etc/issue.net
echo "\S" > $RPM_BUILD_ROOT/usr/lib/issue.net
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/issue.net
ln -s ../usr/lib/issue.net $RPM_BUILD_ROOT/etc/issue.net

# Create os-release and issue files for the different editions
# Cloud
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
echo "VARIANT=\"Cloud Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
echo "VARIANT_ID=cloud" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
sed -i -e "s|(%{release_name})|(Cloud Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud

# Server
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT=\"Server Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT_ID=server" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
sed -i -e "s|(%{release_name})|(Server Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server

cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo "Admin Console: https://\4:9090/ or https://[\6]:9090/" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server

# Workstation
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT=\"Workstation Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT_ID=workstation" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
sed -i -e "s|(%{release_name})|(Workstation Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation

# Create the symlink for /etc/os-release
# We don't create the /usr/lib/os-release symlink until %%post
# so that we can ensure that the right one is referenced.
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Create the symlink for /etc/issue
# We don't create the /usr/lib/os-release symlink until %%post
# so that we can ensure that the right one is referenced.
ln -s ../usr/lib/issue $RPM_BUILD_ROOT/etc/issue

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora                %{dist_version}
%%dist                .fc%{dist_version}
%%fc%{dist_version}                1
EOF

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
mkdir -p $RPM_BUILD_ROOT/usr/lib/os.release.d/presets

# Default system wide
install -m 0644 85-display-manager.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 80-server.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/
# Fedora Workstation
install -m 0644 80-workstation.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/

# Override the list of enabled gnome-shell extensions for Workstation
mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/
install -m 0644 org.gnome.shell.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/

# Copy the make_edition script to /usr/sbin
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/sbin/
install -m 0744 convert-to-edition $RPM_BUILD_ROOT/%{_prefix}/sbin/

%post
# On initial installation, we'll at least temporarily put the non-product
# symlinks in place. It will be overridden by fedora-release-$EDITION
# %%post sections because we don't write the /usr/lib/variant file until
# %%posttrans to avoid trumping the fedora-release-$EDITION packages.
# This is necessary to avoid breaking systemctl scripts since they rely on
# /usr/lib/os-release being valid. We can't wait until %%posttrans to default
# to os-release-fedora.
if [ $1 = 0 ]; then
    ln -sf ./os.release.d/os-release-fedora $RPM_BUILD_ROOT/usr/lib/os-release || :
    ln -sf ./os.release.d/issue-fedora $RPM_BUILD_ROOT/usr/lib/issue || :
fi

# We also want to forcibly set these paths on upgrade if we are explicitly
# set to "nonproduct"
if [ -e /usr/lib/variant ]; then
    . /usr/lib/variant || :
    if [ "x$VARIANT_ID" = "xnonproduct" ]; then
        # Run the convert-to-edition script.
        %{_prefix}/sbin/convert-to-edition -ie non-edition
    fi
fi

%posttrans
# If we get to %%posttrans and nothing created /usr/lib/variant, set it to
# nonproduct
if [ \! -e /usr/lib/variant ]; then
    %{_prefix}/sbin/convert-to-edition -ipe non-edition
fi

%post cloud
# == Run every time ==
# Create the variant file if it does not already exist. This needs to be done
# on both installation and upgrade, to ensure that we upgrade from F23
# and earlier properly.
if [ \! -e /usr/lib/variant ]; then
    echo "VARIANT_ID=cloud" > /usr/lib/variant || :
fi

. /usr/lib/variant || :
if [ "x$VARIANT_ID" = "xcloud" ]; then
    if [ $1 -eq 1 ] ; then
        # (On initial installation only), fix up after %%systemd_post in packages
        # possibly installed before our preset file was added
        %{_prefix}/sbin/convert-to-edition -ipe cloud
    else
        # On upgrades, do not enable or disable presets to avoid surprising
        # the user
        %{_prefix}/sbin/convert-to-edition -ip cloud
    fi
fi

%preun cloud
# If we are uninstalling, we need to reset the variant file and force
# the os-release file back to os-release-fedora.
# We do this in %%preun so that we don't have any time where the os-release
# symlink is dangling (since in %%postun, the os-release-$EDITION file
# will have already been removed)
if [ $1 = 0 ]; then
    . /usr/lib/variant || :
    if [ "x$VARIANT_ID" = "xcloud" ]; then
        # Do not enable or disable presets when uninstalling
        %{_prefix}/sbin/convert-to-edition -ie non-edition
    fi
fi


%post server
# == Run every time ==
# Create the variant file if it does not already exist. This needs to be done
# on both installation and upgrade, to ensure that we upgrade from F23
# and earlier properly.
if [ \! -e /usr/lib/variant ]; then
    echo "VARIANT_ID=server" > /usr/lib/variant || :
fi

. /usr/lib/variant || :
if [ "x$VARIANT_ID" = "xserver" ]; then
    if [ $1 -eq 1 ] ; then
        # (On initial installation only), fix up after %%systemd_post in packages
        # possibly installed before our preset file was added
        %{_prefix}/sbin/convert-to-edition -ipe server
    else
        # On upgrades, do not enable or disable presets to avoid surprising
        # the user
        %{_prefix}/sbin/convert-to-edition -ie server
    fi
fi

%preun server
# If we are uninstalling, we need to delete the variant file and
# force the os-release file back to os-release-fedora.
# We do this in %%preun so that we don't have any time where the os-release
# symlink is dangling (since in %%postun, the os-release-$EDITION file
# will have already been removed)
if [ $1 = 0 ]; then
    . /usr/lib/variant || :
    if [ "x$VARIANT_ID" = "xserver" ]; then
        # Do not enable or disable presets when uninstalling
        %{_prefix}/sbin/convert-to-edition -ie non-edition
    fi
fi

%post workstation
# == Run every time ==
# Create the variant file if it does not already exist. This needs to be done
# on both installation and upgrade, to ensure that we upgrade from F23
# and earlier properly.
if [ \! -e /usr/lib/variant ]; then
    echo "VARIANT_ID=workstation" > /usr/lib/variant || :
fi

. /usr/lib/variant || :
if [ "x$VARIANT_ID" = "xworkstation" ]; then
    if [ $1 -eq 1 ] ; then
        # (On initial installation only), fix up after %%systemd_post in packages
        # possibly installed before our preset file was added
        %{_prefix}/sbin/convert-to-edition -ipe workstation
    else
        # On upgrades, do not enable or disable presets to avoid surprising
        # the user
        %{_prefix}/sbin/convert-to-edition -ip workstation
    fi
fi

%preun workstation
# If we are uninstalling, we need to delete the variant file and
# force the os-release file back to os-release-fedora.
# We do this in %%preun so that we don't have any time where the os-release
# symlink is dangling (since in %%postun, the os-release-$EDITION file
# will have already been removed)
if [ $1 = 0 ]; then
    . /usr/lib/variant || :
    if [ "x$VARIANT_ID" = "xworkstation" ]; then
        # Do not enable or disable presets when uninstalling
        %{_prefix}/sbin/convert-to-edition -ie non-edition
    fi
fi

%postun workstation
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans workstation
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE Fedora-Legal-README.txt
%ghost /usr/lib/variant
%dir /usr/lib/os.release.d
%dir /usr/lib/os.release.d/presets
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-fedora
%ghost /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-fedora
%ghost /usr/lib/issue
%config(noreplace) /etc/issue
%config %attr(0644,root,root) /usr/lib/issue.net
%config(noreplace) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir /usr/lib/systemd/user-preset/
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
/usr/sbin/convert-to-edition

%files cloud
%{!?_licensedir:%global license %%doc}
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-cloud


%files server
%{!?_licensedir:%global license %%doc}
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-server
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-server
%ghost %{_prefix}/lib/systemd/system-preset/80-server.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-server.preset

%files workstation
%{!?_licensedir:%global license %%doc}
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-workstation
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%ghost %{_prefix}/lib/systemd/system-preset/80-workstation.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-workstation.preset

%changelog
* Tue Feb 23 2016 Dennis Gilmore <dennis@ausil.us> - 25-0.1
- setup for rawhide being f25
