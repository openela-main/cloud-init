%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           cloud-init
Version:        24.4
Release:        6%{?dist}
Summary:        Cloud instance init scripts
License:        Apache-2.0 OR GPL-3.0-only
URL:            https://github.com/canonical/cloud-init

Source0:        %{url}/archive/%{version}/%{version}.tar.gz
Source1:        cloud-init-tmpfiles.conf
Patch1: 0002-downstream-Setting-autoconnect-priority-setting-for-.patch
Patch2: 0003-downstream-cc_disk_setup-add-sgdisk-to-sfdisk-conver.patch
Patch3: 0004-downstream-Get-rid-of-gdisk-dependency.patch
Patch4: 0005-downstream-Revert-chore-eliminate-redundant-ordering.patch
Patch5: 0006-downstream-remove-single-process-optimization.patch
Patch6: 0007-fix-don-t-deadlock-when-starting-network-service-wit.patch
Patch7: 0001-downstream-Created-.distro-directory.patch
# For RHEL-73667 - Suggest to change some log messages from warning to info after rebase cloud-init-24.4 [rhel-10]
Patch8: ci-Use-log_with_downgradable_level-for-user-password-wa.patch
# For RHEL-79727 - [c10s] cloud-init remove 'NOZEROCONF=yes' from /etc/sysconfig/network
Patch9: ci-net-sysconfig-do-not-remove-all-existing-settings-of.patch
# For RHEL-81896 - DataSourceNoCloudNet network configuration is ineffective [rhel-10]
Patch10: ci-fix-NM-reload-and-bring-up-individual-network-conns-.patch
# For RHEL-88659 - cloudinit backport optimization features on Alibaba Cloud
Patch11: ci-feat-aliyun-datasource-support-crawl-metadata-at-onc.patch
# For RHEL-100617 - CVE-2024-6174 cloud-init: From CVEorg collector [rhel-10.1]
Patch12: ci-fix-Don-t-attempt-to-identify-non-x86-OpenStack-inst.patch
# For RHEL-100617 - CVE-2024-6174 cloud-init: From CVEorg collector [rhel-10.1]
Patch13: ci-fix-strict-disable-in-ds-identify-on-no-datasources-.patch

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(systemd)

%if %{with tests}
BuildRequires:  iproute
BuildRequires:  passwd
BuildRequires:  procps-ng
# dnf is needed to make cc_ntp unit tests work
# https://bugs.launchpad.net/cloud-init/+bug/1721573
BuildRequires:  /usr/bin/dnf
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(responses)
BuildRequires:  python3dist(passlib)
%endif

# ISC DHCP is no longer maintained and cloud-init 24.1 now supports
# dhcpcd. See commit 21b2b6e4423b0fec325 and the upstream PR
# https://github.com/canonical/cloud-init/pull/4746.
#
Requires:       dhcpcd

Requires:       hostname
Requires:       e2fsprogs
Requires:       iproute
Requires:       python3-libselinux
Requires:       policycoreutils-python3
Requires:       procps
Requires:       python3-configobj
Requires:       python3-jinja2
Requires:       python3-jsonpatch
Requires:       python3-oauthlib
Requires:       python3-pyserial
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       shadow-utils
Requires:       util-linux
Requires:       xfsprogs
# https://bugzilla.redhat.com/show_bug.cgi?id=1974262
Requires:       openssl

%{?systemd_requires}


%description
Cloud-init is a set of init scripts for cloud instances.  Cloud instances
need special scripts to run during initialization to retrieve and install
ssh keys and to let the user run various scripts.


%prep
%autosetup -p1

# Change shebangs
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/env python3|' \
       -e 's|#!/usr/bin/python|#!/usr/bin/python3|' tools/* cloudinit/ssh_util.py

# Removing shebang manually because of rpmlint, will update upstream later
sed -i -e 's|#!/usr/bin/python||' cloudinit/cmd/main.py

# Use unittest from the standard library. unittest2 is old and being
# retired in Fedora. See https://bugzilla.redhat.com/show_bug.cgi?id=1794222
find tests/ -type f | xargs sed -i s/unittest2/unittest/
find tests/ -type f | xargs sed -i s/assertItemsEqual/assertCountEqual/


%generate_buildrequires
%pyproject_buildrequires


%build
%py3_build


%install
%py3_install -- --init-system=systemd

# Generate cloud-config file
python3 tools/render-template --variant %{?rhel:rhel}%{!?rhel:fedora} > $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg

sed -i "s,@@PACKAGED_VERSION@@,%{version}-%{release}," $RPM_BUILD_ROOT/%{python3_sitelib}/cloudinit/version.py

mkdir -p $RPM_BUILD_ROOT/var/lib/cloud

# /run/cloud-init needs a tmpfiles.d entry
mkdir -p $RPM_BUILD_ROOT/run/cloud-init
mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d
cp -p tools/21-cloudinit.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d/21-cloudinit.conf

# installing man pages
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
for man in cloud-id.1 cloud-init.1 cloud-init-per.1; do
    install -c -m 0644 doc/man/${man} ${RPM_BUILD_ROOT}%{_mandir}/man1/${man}
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
done


%check
%if %{with tests}
python3 -m pytest tests/unittests
%else
%py3_check_import cloudinit
%endif

%post
%systemd_post cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service

if [ $1 -eq 1 ] ; then
    # Initial installation
    # Enabled by default per "runs once then goes away" exception
    /bin/systemctl enable cloud-config.service     >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-final.service      >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init.service       >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init-local.service >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init.target        >/dev/null 2>&1 || :
elif [ $1 -eq 2 ]; then
    # Upgrade
    # RHBZ 2210012 - check for null ssh_genkeytypes value in cloud.cfg that
    # breaks ssh connectivity after upgrade to a newer version of cloud-init.
    if [ -f  %{_sysconfdir}/cloud/cloud.cfg.rpmnew ] && grep -q '^\s*ssh_genkeytypes:\s*~\s*$'  %{_sysconfdir}/cloud/cloud.cfg ; then
       echo "***********************************************"
       echo "*** WARNING!!!! ***"
       echo ""
       echo "ssh_genkeytypes set to null in /etc/cloud/cloud.cfg!"
       echo "SSH access might be broken after reboot. Please check the following KCS"
       echo "for more detailed information:"
       echo ""
       echo "https://access.redhat.com/solutions/6988034"
       echo ""
       echo "Please reconcile the differences between /etc/cloud/cloud.cfg and "
       echo "/etc/cloud/cloud.cfg.rpmnew and update ssh_genkeytypes configuration in "
       echo "/etc/cloud/cloud.cfg to a list of keytype values, something like:"
       echo "ssh_genkeytypes:  ['rsa', 'ecdsa', 'ed25519']"
       echo ""
       echo "************************************************"
    fi
    # If the upgrade is from a version older than 0.7.9-8,
    # there will be stale systemd config
    /bin/systemctl is-enabled cloud-config.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-config.service >/dev/null 2>&1 || :
fi
%preun
%systemd_preun cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service


%postun
%systemd_postun cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service

if [ $1 -eq 0 ] ; then
    # warn during package removal not upgrade
    if [ -f /etc/ssh/sshd_config.d/50-cloud-init.conf ] ; then
	echo "/etc/ssh/sshd_config.d/50-cloud-init.conf not removed"
    fi

    if [ -f /etc/NetworkManager/conf.d/99-cloud-init.conf ] ; then
	echo "/etc/NetworkManager/conf.d/99-cloud-init.conf not removed"
    fi

    if [ -f /etc/NetworkManager/conf.d/30-cloud-init-ip6-addr-gen-mode.conf ] ; then
	echo "/etc/NetworkManager/conf.d/30-cloud-init-ip6-addr-gen-mode.conf not removed"
    fi
fi

%files
%license LICENSE LICENSE-Apache2.0 LICENSE-GPLv3
%doc ChangeLog
%doc doc/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
%dir               %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%dir               %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf
%{_udevrulesdir}/66-azure-ephemeral.rules
%{_unitdir}/cloud-config.service
%{_unitdir}/cloud-final.service
%{_unitdir}/cloud-init.service
%{_unitdir}/cloud-init-local.service
%{_unitdir}/cloud-config.target
%{_unitdir}/cloud-init.target
/usr/lib/systemd/system-generators/cloud-init-generator
%{_unitdir}/cloud-init-hotplugd.service
%{_unitdir}/cloud-init-hotplugd.socket
%{_unitdir}/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf
%{_tmpfilesdir}/%{name}.conf
%{python3_sitelib}/*
%{_libexecdir}/%{name}
%{_bindir}/cloud-init*
%{_bindir}/cloud-id
%dir %verify(not mode) /run/cloud-init
%dir /var/lib/cloud
%{_datadir}/bash-completion/completions/cloud-init


%changelog
* Fri Jul 04 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-6
- ci-fix-Don-t-attempt-to-identify-non-x86-OpenStack-inst.patch [RHEL-100617]
- ci-fix-strict-disable-in-ds-identify-on-no-datasources-.patch [RHEL-100617]
- Resolves: RHEL-100617
  (CVE-2024-6174 cloud-init: From CVEorg collector [rhel-10.1])

* Mon May 12 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-5
- ci-feat-aliyun-datasource-support-crawl-metadata-at-onc.patch [RHEL-88659]
- Resolves: RHEL-88659
  (cloudinit backport optimization features on Alibaba Cloud)

* Tue Mar 18 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-4
- ci-fix-NM-reload-and-bring-up-individual-network-conns-.patch [RHEL-81896]
- Resolves: RHEL-81896
  (DataSourceNoCloudNet network configuration is ineffective [rhel-10])

* Mon Feb 17 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-3
- ci-Use-log_with_downgradable_level-for-user-password-wa.patch [RHEL-73667]
- ci-net-sysconfig-do-not-remove-all-existing-settings-of.patch [RHEL-79727]
- Resolves: RHEL-73667
  (Suggest to change some log messages from warning to info after rebase cloud-init-24.4 [rhel-10])
- Resolves: RHEL-79727
  ([c10s] cloud-init remove 'NOZEROCONF=yes' from /etc/sysconfig/network)

* Wed Feb 05 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-2
- Fix config missed on rebase [RHEL-77206]
- Resolves: RHEL-77206
  (cloud-init has reacquired a dependency on python-jsonschema)

* Mon Jan 06 2025 Miroslav Rezanina <mrezanin@redhat.com> - 24.4-1
- Rebase to 24.4 [RHEL-66254]
- Resolves: RHEL-66254
  ([RHEL-10] Rebase cloud-init to 24.4 version)

* Mon Nov 18 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-21
- ci-Prevent-NM-from-handling-DNS-when-network-interfaces.patch [RHEL-65769]
- Resolves: RHEL-65769
  ([RHEL-10] Prevent NM from handling DNS when network interfaces have DNS config)

* Mon Nov 11 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-20
- ci-Remove-python3-jsonschema-dependency.patch [RHEL-65849]
- Resolves: RHEL-65849
  ([RHEL-10] Drop cloud-init dependency on python-jsonschema)

* Tue Nov 05 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-19
- ci-Fix-metric-setting-for-ifcfg-network-connections-for.patch [RHEL-65016]
- ci-fix-Render-bridges-correctly-for-v2-on-sysconfig-wit.patch [RHEL-65019]
- ci-fix-Render-v2-bridges-correctly-on-network-manager-w.patch [RHEL-65019]
- Resolves: RHEL-65016
  (Configuring metric for default gateway is not working [rhel-10])
- Resolves: RHEL-65019
  (NoCloud - network_config bridges incorrectly configured [rhel-10])

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 24.1.4-18
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Mon Aug 26 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-17
- ci-fix-Add-subnet-ipv4-ipv6-to-network-schema-5191.patch [RHEL-54688]
- Resolves: RHEL-54688
  ([RHEL 10.0] cloud-init schema validation fails.)

* Mon Aug 19 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-16
- ci-Revert-fix-vmware-Set-IPv6-to-dhcp-when-there-is-no-.patch [RHEL-54372]
- Resolves: RHEL-54372
  ([RHEL10]Revert "fix(vmware): Set IPv6 to dhcp when there is no IPv6 addr (#5471)")

* Mon Aug 12 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-15
- ci-cc_disk_setup-add-sgdisk-to-sfdisk-convertion-dictio.patch [RHEL-36093]
- ci-Get-rid-of-gdisk-dependency.patch [RHEL-36093]
- Resolves: RHEL-36093
  (Remove cloud-init dependency on obsolete gdisk)

* Wed Jul 24 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-14
- ci-fix-Clean-cache-if-no-datasource-fallback-5499.patch [RHEL-49740]
- ci-Support-setting-mirrorlist-in-yum-repository-config-.patch [RHEL-49739]
- Resolves: RHEL-49740
  ([Cloud-init] [RHEL-10] Password reset feature broken with CloudstackDataSource)
- Resolves: RHEL-49739
  (Support setting mirrorlist in yum repository config [rhel-10])

* Fri Jul 12 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-13
- ci-fix-add-schema-rules-for-baseurl-and-metalink-in-yum.patch [RHEL-46874]
- Resolves: RHEL-46874
  (Suggest to update schema to support metalink [rhel-10])

* Mon Jul 08 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-12
- ci-Support-metalink-in-yum-repository-config-5444.patch [RHEL-44918]
- ci-fix-vmware-Set-IPv6-to-dhcp-when-there-is-no-IPv6-ad.patch [RHEL-35562]
- Resolves: RHEL-44918
  ([RFE] Support metalink in yum repository config [rhel-10])
- Resolves: RHEL-35562
  ([RHEL-10] It leaves the ipv6 networking config as blank in NM keyfile when config dhcp ipv6 with customization spec)

* Mon Jul 01 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-11
- ci-Deprecate-the-users-ssh-authorized-keys-property-516.patch [RHEL-45263]
- ci-docs-Add-deprecated-system_info-to-schema-5168.patch [RHEL-45263]
- ci-fix-schema-permit-deprecated-hyphenated-keys-under-u.patch [RHEL-45263]
- Resolves: RHEL-45263
  (Deprecate the users ssh-authorized-keys property and permit deprecated hyphenated keys under users key [rhel-10])

* Wed Jun 26 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-10
- ci-feat-sysconfig-Add-DNS-from-interface-config-to-reso.patch [RHEL-44334]
- ci-fix-jsonschema-Add-missing-sudo-definition-5418.patch [RHEL-44338]
- ci-doc-update-examples-to-reflect-alternative-ways-to-p.patch [RHEL-44338]
- ci-Update-pylint-version-to-support-python-3.12-5338.patch [RHEL-44599]
- Resolves: RHEL-44334
  ([RHEL-10] cloud-init fails to configure DNS search domains)
- Resolves: RHEL-44338
  ([RHEL-10] fix `SUDO` configuration schema for users and groups)
- Resolves: RHEL-44599
  ([rhel-10] fix pylint error and support python 3.12)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 24.1.4-9
- Bump release for June 2024 mass rebuild

* Thu Jun 20 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-8
- ci-.distro-spec-add-missing-dependencies-for-cloud-init.patch [RHEL-41010]
- Resolves: RHEL-41010
  ([RHEL-10] Add missing Requires dependency in cloud-init)

* Wed Jun 12 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-7
- ci-Add-back-dependency-on-python3-configobj.patch [RHEL-39347]
- Resolves: RHEL-39347
  ([RHEL-10] Requires dependency python3-configobj)

* Tue Jun 04 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-6
- ci-.distro-spec-remove-dependency-on-net-tools.patch [RHEL-39345]
- Resolves: RHEL-39345
  ([RHEL-10] Remove dependency on net-tools)

* Mon May 27 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-5
- ci-feat-Set-RH-ssh-key-permissions-when-no-ssh_keys-gro.patch [RHEL-36456]
- Resolves: RHEL-36456
  ([RHEL-10] Group ssh_keys is missing and ssh host key permission is changed in rhel-10)

* Mon May 06 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-4
- ci-Report-full-specific-version-with-cloud-init-version.patch [RHEL-34764]
- Resolves: RHEL-34764
  ([RHEL-10] cloud-init should report full version with "cloud-init --version" )

* Mon Apr 29 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-3
- ci-Fix-spec-file-post-install-script.patch [RHEL-33954]
- ci-refactor-remove-dependency-on-netifaces-4634.patch [RHEL-34518]
- ci-DS-VMware-Fix-ipv6-addr-converter-from-netinfo-to-ne.patch [RHEL-34518]
- Resolves: RHEL-33954
  ([RHEL-10] There is error message during cloud-init installation)
- Resolves: RHEL-34518
  (Remove dependency to netifcaces)

* Tue Apr 23 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-2
- ci-Remove-dependency-on-dhcp-client-ISC-DHCP-and-use-dh.patch [RHEL-26304]
- ci-fix-Fall-back-to-cached-local-ds-if-no-valid-ds-foun.patch [RHEL-32854]
- Resolves: RHEL-26304
  ([RFE][rhel-10] Suggest to remove dependency on dhcp-client in cloud-init)
- Resolves: RHEL-32854
  ([cloud-init][ESXi]VMware datasource resets on every boot causing it to lose network configuration [rhel-10.0])

* Mon Apr 22 2024 Miroslav Rezanina <mrezanin@redhat.com> - 24.1.4-1
- Rebase to 24.1.4 [RHEL-33439]
- Resolves: RHEL-33439
  (Update cloud-init on 24.1.4 for RHEL 10)

* Thu Feb 01 2024 Major Hayden <major@redhat.com> - 23.4.1-5
- Switch back to dhcp-client temporarily

* Tue Jan 30 2024 Major Hayden <major@redhat.com> - 23.4.1-4
- Replace dhcp-client with udhcpc

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 František Zatloukal <fzatlouk@redhat.com> - 23.4.1-1
- Update to 23.4.1

* Fri Aug 11 2023 Miroslav Suchý <msuchy@redhat.com> - 23.2.1-2
- correct SPDX formula

* Thu Jul 20 2023 Major Hayden <major@redhat.com> - 23.2.1-1
- Update to 23.2.1

* Thu Jul 20 2023 Major Hayden <major@redhat.com> - 23.2-4
- Add packit config

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 23.2-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Major Hayden <major@redhat.com> - 23.2-1
- Update to 23.2 rhbz#2196523

* Wed May 17 2023 Major Hayden <major@redhat.com> - 23.1.2-10
- Migrate to pyproject-rpm-macros for build requirements

* Tue May 16 2023 Major Hayden <major@redhat.com> - 23.1.2-9
- ec2: Do not enable DHCPv6 on EC2

* Tue May 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 23.1.2-8
- Disable tests by default in RHEL builds

* Thu May 11 2023 Major Hayden <major@redhat.com> - 23.1.2-7
- Update changelog for rhbz#2068529

* Thu May 11 2023 Major Hayden <major@redhat.com> - 23.1.2-6
- Allow > 3 nameservers to be used rhbz#2068529

* Sun Apr 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.1.2-5
- Use the correct SourceURL format for the upstream sources
- Switch to SPDX identifiers for the license field

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-4
- Switch to GitHub for upstream source

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-3
- Revert "Use forge source"

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-2
- Use forge source

* Thu Apr 27 2023 Major Hayden <major@redhat.com> - 23.1.2-1
- Update to 23.1.2

* Thu Mar 23 2023 František Zatloukal <fzatlouk@redhat.com> - 23.1.1-1
- Rebase to 23.1.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 22.2-3
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.2-2
- Add dhcp-client dependency for Azure and OCI network bootstrap

* Thu May 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.2-1
- Rebase to 22.2

* Thu Mar 10 2022 Dusty Mabe <dusty@dustymabe.com> - 22.1-3
- Don't require NetworkManager-config-server

* Tue Feb 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.1-2
- Drop extra tests search in prep

* Tue Feb 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.1-1
- Rebase to 22.1
- Backport cloud-init PR to add proper NetworkManager support
- Add patch to prefer NetworkManager

* Wed Feb 16 2022 Charalampos Stratakis <cstratak@redhat.com> - 21.3-6
- Remove redundant dependencies on nose and mock
