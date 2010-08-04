%define release_name Finian
%define dist_version 15

Summary:	Fedora release files
Name:		fedora-release
Version:	15
Release:	0.2
License:	GPLv2
Group:		System Environment/Base
URL:		http://fedoraproject.org
Source:		%{name}-%{version}.tar.bz2
Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release = %{version}-%{release}
Requires:       fedora-release-rawhide = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
Fedora release files such as yum configs and various /etc/ files that
define the release.

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-release = %{version}-%{release}

%description rawhide
This package provides the rawhide repo definitions.


%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Fedora release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg

install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Install all the keys, link the primary keys to primary arch files
# and to compat generic location
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for arch in i386 x86_64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
for arch in sparc sparc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-SPARC RPM-GPG-KEY-fedora-$arch
done
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL 
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/rpm/macros.dist
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo


%changelog
* Thu Jul 29 2010 Jesse Keating <jkeating@redhat.com> - 15-0.1
- Build for Fedora 15

* Fri Jul 23 2010 Jesse Keating <jkeating@redhat.com> - 14-0.6
- Add the Fedora 14 key

* Thu May 06 2010 Dennis Gilmore <dennis@ausil.us> - 14-0.5
- link sparc key
- drop ppc ppc64 from primary arch list

* Tue Mar 02 2010 Jesse Keating <jkeating@redhat.com> - 14-0.4
- When in rawhide, require the -rawhide subpackage.

* Thu Feb 18 2010 Jesse Keating <jkeating@redhat.com> - 14-0.3
- Fix the key path in the updates-testing repo

* Thu Feb 18 2010 Jesse Keating <jkeating@redhat.com> - 14-0.2
- Fix the -rawhide requires
- Fix the -rawhide files
- Switch to bz2 source

* Mon Feb 15 2010 Jesse Keating <jkeating@redhat.com> - 14-0.1
- Update for Fedora 14
- Move the rawhide repo file to it's own subpackage

* Tue Jan 19 2010 Jesse Keating <jkeating@redhat.com> - 13-0.3
- Put the right key in the key file this time

* Tue Jan 19 2010 Jesse Keating <jkeating@redhat.com> - 13-0.2
- Add the key for Fedora 13

* Thu Aug 27 2009 Jesse Keating <jkeating@redhat.com> - 13-0.1
- Bump for Fedora 13's rawhide.
- Put the version at 13 from the start.

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-3
- Bump for new tarball

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-2
- Fix the gpg key file name

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-1
- Update for F12-Alpha
- Replace F11 key with F12
- Drop old keys and inactive secondary arch keys
- Fix metalink urls to be https
- Drop the compose stuff

* Mon Mar 30 2009 Jesse Keating <jkeating@redhat.com> - 11.90-1
- Build for F12 collection

* Mon Mar 09 2009 Jesse Keating <jkeating@redhat.com> - 10.92-1
- Bump for F11 Beta
- Add the (giant) F11 Test key

* Thu Mar 05 2009 Jesse Keating <jkeating@redhat.com> - 10.91-4
- Drop req on fedora-release-notes (#483018)

* Tue Mar 03 2009 Jesse Keating <jkeating@redhat.com> - 10.91-3
- Move metalink urls to mirrorlist for helping anaconda

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Jesse Keating <jkeating@redhat.com> - 10.91-1
- Use the correct CPE name (#481287)

* Wed Jan 21 2009 Jesse Keating <jkeating@redhat.com> - 10.91-1
- Update for Fedora 11 Alpha
- Use metalink urls to get mirror information

* Wed Oct 01 2008 Jesse Keating <jkeating@redhat.com> - 10.90-1
- Initial build for Fedora 11.

* Mon Sep 15 2008 Jesse Keating <jkeating@redhat.com> - 9.91-1
- Update for Fedora 10 beta
- Add the new keys for F10
- Remove F8/9 keys
- Update compose configs
- Clarify rawhide repo definition

* Wed Jun 11 2008 Jesse Keating <jkeating@redhat.com> - 9.90-2
- Package up the ia64 key as the first secondary arch
- Mark config files correctly
- Stop using download.fedora.redhat.com and use download.fedoraproject.org instead

* Mon Mar 31 2008 Jesse Keating <jkeating@redhat.com> - 9.90-1
- Update for Fedora 10 rawhide.

* Thu Mar 13 2008 Jesse Keating <jkeating@redhat.com> - 8.92-1
- Update for 9 Beta
- Update the compose files for 9 Beta
- Add system-release-cpe (from Mark Cox)
- Add terminal to issue (#436387)
- Rename development to rawhide where appropriate.

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 8.90-3
- Bump for cvs oopsie

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 8.90-2
- Add the gpg info to the devel repo

* Wed Oct 03 2007 Jesse Keating <jkeating@redhat.com> - 8.90-1
- First build for Fedora 9 development.

* Fri Sep 28 2007 Jesse Keating <jkeating@redhat.com> - 7.92-1
- Bump for F8 Test2.
- Package up the compose kickstart files

* Fri Sep 14 2007 Jesse Keating <jkeating@redhat.com> - 7.91-2
- Use failovermethod=priority in yum configs (243698)

* Thu Aug 30 2007 Jesse Keating <jkeating@redhat.com> - 7.91-1
- Provide system-release, useful for spinoffs.
- Also link system-release to fedora-release for file level checks
- Bump for F8 Test2
- Fix license tag

* Thu Jul 27 2007 Jesse Keating <jkeating@redhat.com> - 7.90-1
- Bump for F8 Test1

* Thu Jun 28 2007 Jesse Keating <jkeating@redhat.com> - 7.89-3
- Cleanups from review
- Don't (noreplace) the dist tag macro file

* Tue Jun 19 2007 Jesse Keating <jkeating@redhat.com> - 7.89-2
- Define the dist macros in this package since we define everyting else here

* Wed May 30 2007 Jesse Keating <jkeating@redhat.com> - 7.89-1
- And we're back to rawhide.  Re-enable devel repos

* Thu May 24 2007 Jesse Keating <jkeating@redhat.com> - 7-3
- We have a name!
- Require the newer release notes

* Mon May 21 2007 Jesse Keating <jkeating@redhat.com> - 7-2
- Use Everything in the non-mirror URL to the release tree

* Mon May 21 2007 Jesse Keating <jkeating@redhat.com> - 7-1
- First build for Fedora 7
- Remove Extras repos (YAY!)
- Remove references to "core" in repo files.
- Adjust repo files for new mirror structure
- Remove Legacy repo

* Fri Apr 20 2007 Jesse Keating <jkeating@redhat.com> - 6.93-1
- Bump for Test 4

* Mon Mar 19 2007 Jesse Keating <jkeating@redhat.com> - 6.92-1
- Bump for Test 3
- No more eula in fedora-release, moved to firstboot

* Fri Feb 23 2007 Jesse Keating <jkeating@redhat.com> - 6.91-1
- Bump for Test 2

* Tue Feb 13 2007 Jesse Keating <jkeating@redhat.com> - 6.90-4
- Specfile cleanups

* Mon Feb 05 2007 Jesse Keating <jkeating@redhat.com> - 6.90-3
- Drop the legacy repo file.

* Fri Jan 26 2007 Jesse Keating <jkeating@redhat.com> - 6.90-2
- Core?  What Core?

* Wed Jan 24 2007 Jeremy Katz <katzj@redhat.com> - 6.90-1
- Bump to 6.90.  Keep working with older release notes

* Mon Oct 16 2006 Jesse Keating <jkeating@redhat.com> - 6-89
- Keep version 6, bump release.  Saves from having to rebuild
  release notes all the time

* Sun Oct 15 2006 Jesse Keating <jkeating@redhat.com> - 6.89-1
- Rebuild for rawhide

* Thu Oct 12 2006 Jesse Keating <jkeating@redhat.com> - 6-3
- version has to stay the same, safe to use.

* Thu Oct  5 2006 Jesse Keating <jkeating@redhat.com> - 6-2
- replace old mirror files with new mirrorlist cgi system

* Thu Oct  5 2006 Jesse Keating <jkeating@redhat.com> - 6-1
- Rebuild for Fedora Core 6 release

* Tue Sep  5 2006 Jesse Keating <jkeating@redhat.com> - 5.92-1
- Bump for FC6 Test3

* Thu Jul 27 2006 Jesse Keating <jkeating@redhat.com> - 5.91.1-1
- Convert deprecated gtk calls. (#200242)
- Fix some of the versioning

* Sun Jul 23 2006 Jesse Keating <jkeating@redhat.com> - 5.91-4
- Bump for FC6 Test2
- Remove release-notes content, now standalone package
- Don't replace issue and issue.net if the end user has modified it
- Require fedora-release-notes
- Cleanups

* Mon Jun 19 2006 Jesse Keating <jkeating@redhat.com> - 5.90-3
- Cleanups

* Thu Jun 15 2006 Jesse Keating <jkeating@redhat.com> - 5.90-1
- Update for 5.90

* Wed May 24 2006 Jesse Keating <jkeating@redhat.com> - 5.89-rawhide.2
- Update to get new devel repo file
- merge minor changes from external cvs .spec file

* Wed Apr 19 2006 Jesse Keating <jkeating@redhat.com> - 5.89-rawhide.1
- Look, a changelog!
- Removed duplicate html/css content from doc dir.
- Add lynx as a buildreq

