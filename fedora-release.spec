%define release_version 5
%define release_name Bordeaux
%define builtin_release_version Rawhide
%define builtin_release_name Rawhide
%define real_release_version %{?release_version}%{!?release_version:%{builtin_release_version}}
%define real_release_name %{?release_name}%{!?release_name:%{builtin_release_name}}
Summary: Fedora Core release file
Name: fedora-release
Version: %{real_release_version}
Release: 2
License: GFDL
Group: System Environment/Base
Source: fedora-release-%{real_release_version}.tar.gz
Source1: fedora-release-notes-%{real_release_version}.tar.gz
Obsoletes: rawhide-release
Obsoletes: redhat-release
Obsoletes: indexhtml
Provides: redhat-release
Provides: indexhtml
BuildRoot: %{_tmppath}/fedora-release-root
BuildArchitectures: noarch
BuildRequires: xmlto
BuildRequires: desktop-file-utils

%description
Fedora Core release file

%prep
%setup -q -n fedora-release-%{version} -a 1

%build
MAINDIR=`pwd`
pushd release-notes
cp RELEASE-NOTES-en.txt $MAINDIR/RELEASE-NOTES
cp README-en.txt $MAINDIR/README
cp -af README-* $MAINDIR
cp -af RELEASE-NOTES-* $MAINDIR
cp -r *.css figs stylesheet-images ../
cp -r about ../
popd
rm -f */*.eps
make index.html

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
echo "Fedora Core release %{real_release_version} (%{real_release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
cp $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
mkdir -p $RPM_BUILD_ROOT/usr/share/eula $RPM_BUILD_ROOT/usr/share/firstboot/modules
cp -f eula.txt $RPM_BUILD_ROOT/usr/share/eula/eula.en_US
cp -f eula.py $RPM_BUILD_ROOT/usr/share/firstboot/modules/eula.py

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
	install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

mkdir -p -m 755 $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML
cp -ap figs *.css *.html img css stylesheet-images \
  $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML
install -m 644 index.html $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML/index.html

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/sysconfig/rhn
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 sources $RPM_BUILD_ROOT/etc/sysconfig/rhn/sources
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# about fedora stuff
mkdir -p $RPM_BUILD_ROOT%{_datadir}/omf/fedora-release
install -m 644 release-notes/about-fedora.omf $RPM_BUILD_ROOT%{_datadir}/omf/fedora-release
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications 
install -m 644 release-notes/about-fedora.desktop $RPM_BUILD_ROOT%{_datadir}/applications/about-fedora.desktop

%clean
rm -rf $RPM_BUILD_ROOT

# If this is the first time a package containing /etc/issue
# is installed, we want the new files there. Otherwise, we
# want %config(noreplace) to take precedence.
%triggerpostun  -- redhat-release < 7.1.93-1
if [ -f /etc/issue.rpmnew ] ; then
   mv -f /etc/issue /etc/issue.rpmsave
   mv -f /etc/issue.rpmnew /etc/issue
fi
if [ -f /etc/issue.net.rpmnew ] ; then
   mv -f /etc/issue.net /etc/issue.net.rpmsave
   mv -f /etc/issue.net.rpmnew /etc/issue.net
fi

%post
[ -x /usr/bin/scrollkeeper-update ] && /usr/bin/scrollkeeper-update
[ -x /usr/bin/update-desktop-database ] && /usr/bin/update-desktop-database
exit 0

%postun
[ -x /usr/bin/scrollkeeper-update ] && /usr/bin/scrollkeeper-update
[ -x /usr/bin/update-desktop-database ] && /usr/bin/update-desktop-database
exit 0

%files
%defattr(-,root,root)
%attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
%dir /etc/sysconfig/rhn
%dir /etc/yum.repos.d
%config(noreplace) /etc/sysconfig/rhn/sources
%config(noreplace) /etc/yum.repos.d/*
%doc R* stylesheet-images figs *.css
%doc eula.txt GPL autorun-template
%doc about
%config %attr(0644,root,root) /etc/issue
%config %attr(0644,root,root) /etc/issue.net
/usr/share/firstboot/modules/eula.py*
/usr/share/eula/eula.en_US
%{_defaultdocdir}/HTML
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
%{_datadir}/omf/fedora-release
%{_datadir}/applications/*.desktop
