%{!?license: %global license %%doc}

# The only reason we are archful is because dmidecode is ExclusiveArch
# https://bugzilla.redhat.com/show_bug.cgi?id=1067089
%global debug_package %{nil}

Name:                 cloud-init
Version:              23.1.1
Release:              10%{?dist}.0.1
Summary:              Cloud instance init scripts

Group:                System Environment/Base
License:              GPLv3
URL:                  http://launchpad.net/cloud-init
Source0:              https://launchpad.net/cloud-init/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Source1:              cloud-init-tmpfiles.conf

Patch0002:            0002-Do-not-write-NM_CONTROLLED-no-in-generated-interface.patch
Patch0003:            0003-limit-permissions-on-def_log_file.patch
Patch0004:            0004-include-NOZEROCONF-yes-in-etc-sysconfig-network.patch
Patch0005:            0005-Manual-revert-Use-Network-Manager-and-Netplan-as-def.patch
Patch0006:            0006-Revert-Add-native-NetworkManager-support-1224.patch
Patch0007:            0007-settings.py-update-settings-for-rhel.patch
# For bz#2182407 - cloud-init strips new line from "/etc/hostname" when processing "/var/lib/cloud/data/previous-hostname"
Patch8:               ci-rhel-make-sure-previous-hostname-file-ends-with-a-ne.patch
# For bz#2182947 - Request to backport "Don't change permissions of netrules target (#2076)"
Patch9:               ci-Don-t-change-permissions-of-netrules-target-2076.patch
# For bz#2190081 - CVE-2023-1786 cloud-init: sensitive data could be exposed in logs [rhel-8]
Patch10:              ci-Make-user-vendor-data-sensitive-and-remove-log-permi.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch11:              ci-Revert-Manual-revert-Use-Network-Manager-and-Netplan.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch12:              ci-Revert-Revert-Add-native-NetworkManager-support-1224.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch13:              ci-nm-generate-ipv6-stateful-dhcp-config-at-par-with-sy.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch14:              ci-network_manager-add-a-method-for-ipv6-static-IP-conf.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch15:              ci-net-sysconfig-enable-sysconfig-renderer-if-network-m.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch16:              ci-network-manager-Set-higher-autoconnect-priority-for-.patch
# For bz#2219528 - [RHEL8] Support configuring network by NM keyfiles
Patch17:              ci-Set-default-renderer-as-sysconfig-for-centos-rhel-41.patch
Patch19:              ci-tools-read-version-fix-the-tool-so-that-it-can-handl.patch
Patch20:              ci-test-fixes-remove-NM_CONTROLLED-no-from-tests.patch
Patch21:              ci-Enable-SUSE-based-distros-for-ca-handling-2036.patch
Patch22:              ci-Handle-non-existent-ca-cert-config-situation-2073.patch
Patch23:              ci-Revert-limit-permissions-on-def_log_file.patch
Patch24:              ci-test-fixes-changes-to-apply-RHEL-specific-config-set.patch
Patch25:              ci-cosmetic-fix-tox-formatting.patch
# For bz#2222501 - Don't change log permissions if they are already more restrictive [rhel-8]
Patch28:              ci-logging-keep-current-file-mode-of-log-file-if-its-st.patch
# For bz#2223810 - [cloud-init] [RHEL8.9]There are warning logs if dev has more than one IPV6 address on ESXi
Patch29:              ci-DS-VMware-modify-a-few-log-level-4284.patch
# For bz#2229460 - [rhel-8.9] [RFE] Configure "ipv6.addr-gen-mode=eui64' as default in NetworkManager
Patch30:              ci-NM-renderer-set-default-IPv6-addr-gen-mode-for-all-i.patch
Patch31:              0001-Ensure-cloud-user-is-applied-to-OpenELA.patch
Patch32:              0001-Remove-rh-subscription.patch

BuildArch:            noarch

BuildRequires:        pkgconfig(systemd)
BuildRequires:        python3-devel
BuildRequires:        python3-setuptools
BuildRequires:        systemd

# For tests
BuildRequires:        iproute
BuildRequires:        python3-configobj
# # https://bugzilla.redhat.com/show_bug.cgi?id=1417029
BuildRequires:        python3-httpretty >= 0.8.14-2
BuildRequires:        python3-jinja2
BuildRequires:        python3-jsonpatch
BuildRequires:        python3-jsonschema
BuildRequires:        python3-mock
BuildRequires:        python3-nose
BuildRequires:        python3-oauthlib
BuildRequires:        python3-prettytable
BuildRequires:        python3-pyserial
BuildRequires:        python3-PyYAML
BuildRequires:        python3-requests
BuildRequires:        python3-six
BuildRequires:        python3-unittest2
# dnf is needed to make cc_ntp unit tests work
# https://bugs.launchpad.net/cloud-init/+bug/1721573
BuildRequires:        /usr/bin/dnf

Requires:             e2fsprogs
Requires:             iproute
Requires:             libselinux-python3
Requires:             policycoreutils-python3
Requires:             procps
Requires:             python3-configobj
Requires:             python3-jinja2
Requires:             python3-jsonpatch
Requires:             python3-jsonschema
Requires:             python3-oauthlib
Requires:             python3-prettytable
Requires:             python3-pyserial
Requires:             python3-PyYAML
Requires:             python3-requests
Requires:             python3-six
Requires:             shadow-utils
Requires:             util-linux
Requires:             xfsprogs
Requires:             dhcp-client
# https://bugzilla.redhat.com/show_bug.cgi?id=2039697
Requires:             gdisk
Requires:             openssl
Requires:             python3-netifaces

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

%build
%py3_build


%install
%py3_install --

sed -i "s,@@PACKAGED_VERSION@@,%{version}-%{release}," $RPM_BUILD_ROOT/%{python3_sitelib}/cloudinit/version.py

mkdir -p $RPM_BUILD_ROOT/var/lib/cloud

# /run/cloud-init needs a tmpfiles.d entry
mkdir -p $RPM_BUILD_ROOT/run/cloud-init
mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d
cp -p tools/21-cloudinit.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d/21-cloudinit.conf

# Make installed NetworkManager hook name less generic
mv $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d/hook-network-manager \
   $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d/cloud-init-azure-hook

[ ! -d $RPM_BUILD_ROOT/usr/lib/systemd/system-generators ] && mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system-generators
python3 tools/render-cloudcfg --variant rhel systemd/cloud-init-generator.tmpl > $RPM_BUILD_ROOT/usr/lib/systemd/system-generators/cloud-init-generator
chmod 755 $RPM_BUILD_ROOT/usr/lib/systemd/system-generators/cloud-init-generator

# installing man pages
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
for man in cloud-id.1 cloud-init.1 cloud-init-per.1; do
    install -c -m 0644 doc/man/${man} ${RPM_BUILD_ROOT}%{_mandir}/man1/${man}
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
done

%clean
rm -rf $RPM_BUILD_ROOT


%post
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

    /bin/systemctl is-enabled cloud-final.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-final.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init-local.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init-local.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init.target >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init.target >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable cloud-config.service >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-final.service  >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init.service   >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init-local.service >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init.target     >/dev/null 2>&1 || :
    # One-shot services -> no need to stop
fi

%postun
%systemd_postun cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service

if [ -f /etc/ssh/sshd_config.d/50-cloud-init.conf ] ; then
    echo "/etc/ssh/sshd_config.d/50-cloud-init.conf not removed"
fi

if [ -f /etc/NetworkManager/conf.d/99-cloud-init.conf ] ; then
    echo "/etc/NetworkManager/conf.d/99-cloud-init.conf not removed"
fi

if [ -f /etc/NetworkManager/conf.d/30-cloud-init-ip6-addr-gen-mode.conf ] ; then
    echo "/etc/NetworkManager/conf.d/30-cloud-init-ip6-addr-gen-mode.conf not removed"
fi

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
%doc               %{_sysconfdir}/cloud/clean.d/README
%dir               %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%{_unitdir}/cloud-config.service
%{_unitdir}/cloud-config.target
%{_unitdir}/cloud-final.service
%{_unitdir}/cloud-init-hotplugd.service
%{_unitdir}/cloud-init-hotplugd.socket
%{_unitdir}/cloud-init-local.service
%{_unitdir}/cloud-init.service
%{_unitdir}/cloud-init.target
%{_tmpfilesdir}/%{name}.conf
%{python3_sitelib}/*
%{_libexecdir}/%{name}
%{_bindir}/cloud-init*
%doc %{_datadir}/doc/%{name}
%{_mandir}/man1/*
%dir %verify(not mode) /run/cloud-init
%dir /var/lib/cloud
/etc/NetworkManager/dispatcher.d/cloud-init-azure-hook
/etc/dhcp/dhclient-exit-hooks.d/hook-dhclient
%{_udevrulesdir}/66-azure-ephemeral.rules
%{_datadir}/bash-completion/completions/cloud-init
%{_bindir}/cloud-id
/usr/lib/systemd/system-generators/cloud-init-generator
%{_sysconfdir}/systemd/system/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf


%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf

%changelog
* Thu Jan 25 2024 Release Engineering <releng@openela.org> - 23.1.1.0.1
- Apply OpenELA fixes

* Fri Aug 25 2023 Camilla Conte <cconte@redhat.com> - 23.1.1-10
- Resolves: bz#2233047
  ([RHEL 8.9] Inform user when cloud-init generated config files are left during uninstalling)

* Wed Aug 09 2023 Jon Maloy <jmaloy@redhat.com> - 23.1.1-9
- ci-NM-renderer-set-default-IPv6-addr-gen-mode-for-all-i.patch [bz#2229460]
- Resolves: bz#2229460
  ([rhel-8.9] [RFE] Configure "ipv6.addr-gen-mode=eui64' as default in NetworkManager)

* Thu Jul 27 2023 Camilla Conte <cconte@redhat.com> - 23.1.1-8
- ci-DS-VMware-modify-a-few-log-level-4284.patch [bz#2223810]
- Resolves: bz#2223810
  ([cloud-init] [RHEL8.9]There are warning logs if dev has more than one IPV6 address on ESXi)

* Tue Jul 25 2023 Miroslav Rezanina <mrezanin@redhat.com> - 23.1.1-7
- ci-logging-keep-current-file-mode-of-log-file-if-its-st.patch [bz#2222501]
- Resolves: bz#2222501
  (Don't change log permissions if they are already more restrictive [rhel-8])

* Mon Jul 10 2023 Miroslav Rezanina <mrezanin@redhat.com> - 23.1.1-6
- ci-Revert-Manual-revert-Use-Network-Manager-and-Netplan.patch [bz#2219528]
- ci-Revert-Revert-Add-native-NetworkManager-support-1224.patch [bz#2219528]
- ci-nm-generate-ipv6-stateful-dhcp-config-at-par-with-sy.patch [bz#2219528]
- ci-network_manager-add-a-method-for-ipv6-static-IP-conf.patch [bz#2219528]
- ci-net-sysconfig-enable-sysconfig-renderer-if-network-m.patch [bz#2219528]
- ci-network-manager-Set-higher-autoconnect-priority-for-.patch [bz#2219528]
- ci-Set-default-renderer-as-sysconfig-for-centos-rhel-41.patch [bz#2219528]
- Resolves: bz#2219528
  ([RHEL8] Support configuring network by NM keyfiles)

* Tue Jul 4 2023 Camilla Conte <cconte@redhat.com> - 23.1.1-5
- ci-Add-warning-during-upgrade-from-an-old-version-with-.patch [bz#2210012]
- Resolves: bz#2210012
  ([cloud-init] System didn't generate ssh host keys and lost ssh connection after cloud-init removed them with updated cloud-init package.)

* Wed May 03 2023 Jon Maloy <jmaloy@redhat.com> - 23.1.1-3
- ci-Don-t-change-permissions-of-netrules-target-2076.patch [bz#2182947]
- ci-Make-user-vendor-data-sensitive-and-remove-log-permi.patch [bz#2190081]
- Resolves: bz#2182947
  (Request to backport "Don't change permissions of netrules target (#2076)")
- Resolves: bz#2190081
  (CVE-2023-1786 cloud-init: sensitive data could be exposed in logs [rhel-8])

* Tue Apr 25 2023 Jon Maloy <jmaloy@redhat.com> - 23.1.1-2
- ci-rhel-make-sure-previous-hostname-file-ends-with-a-ne.patch [bz#2182407]
- Resolves: bz#2182407
  (cloud-init strips new line from "/etc/hostname" when processing "/var/lib/cloud/data/previous-hostname")

* Fri Apr 21 2023 Jon Maloy <jmaloy@redhat.com> - 23.1.1-1
- limit-permissions-on-def_log_file.patch
- Resolves bz#1424612
- include-NOZEROCONF-yes-in-etc-sysconfig-network.patch
- Resolves bz#1653131
- Rebase to 23.1.1 [bz#2172821]
- Resolves: bz#2172821

* Mon Jan 30 2023 Camilla Conte <cconte@redhat.com> - 22.1-8
- ci-cc_set_hostname-ignore-var-lib-cloud-data-set-hostna.patch [bz#2162258]
- Resolves: bz#2162258
  (systemd[1]: Failed to start Initial cloud-init job after reboot system via sysrq 'b' [RHEL-8])

* Wed Dec 28 2022 Camilla Conte <cconte@redhat.com> - 22.1-7
- ci-Ensure-network-ready-before-cloud-init-service-runs-.patch [bz#2151861]
- Resolves: bz#2151861
  ([RHEL-8] Ensure network ready before cloud-init service runs on RHEL)

* Mon Oct 17 2022 Jon Maloy <jmaloy@redhat.com> - 22.1-6
- ci-cloud.cfg.tmpl-make-sure-centos-settings-are-identic.patch [bz#2115576]
- Resolves: bz#2115576
  (cloud-init configures user "centos" or "rhel" instead of "cloud-user" with cloud-init-22.1)

* Wed Aug 17 2022 Jon Maloy <jmaloy@redhat.com> - 22.1-5
- ci-Revert-Add-native-NetworkManager-support-1224.patch [bz#2107464 bz#2110066 bz#2117526 bz#2104393 bz#2098624]
- ci-Revert-Use-Network-Manager-and-Netplan-as-default-re.patch [bz#2107464 bz#2110066 bz#2117526 bz#2104393 bz#2098624]
- Resolves: bz#2107464
  ([RHEL-8.7] Cannot run sysconfig when changing the priority of network renderers)
- Resolves: bz#2110066
  (DNS integration with OpenStack/cloud-init/NetworkManager is not working)
- Resolves: bz#2117526
  ([RHEL8.7] Revert patch of configuring networking by NM keyfiles)
- Resolves: bz#2104393
  ([RHEL-8.7]Failed to config static IP and IPv6 according to VMware Customization Config File)
- Resolves: bz#2098624
  ([RHEL-8.7] IPv6 not workable when cloud-init configure network using NM keyfiles)

* Tue Jul 12 2022 Miroslav Rezanina <mrezanin@redhat.com> - 22.1-4
- ci-cloud-init.spec-adjust-path-for-66-azure-ephemeral.r.patch [bz#2096269]
- ci-setup.py-adjust-udev-rules-default-path-1513.patch [bz#2096269]
- Resolves: bz#2096269
  (Adjust udev/rules default path[RHEL-8])

* Thu Jun 23 2022 Jon Maloy <jmaloy@redhat.com> - 22.1-3
- ci-Support-EC2-tags-in-instance-metadata-1309.patch [bz#2082686]
- Resolves: bz#2082686
  ([cloud][init] Add support for reading tags from instance metadata)

* Tue May 31 2022 Jon Maloy <jmaloy@redhat.com> - 22.1-2
- ci-Add-native-NetworkManager-support-1224.patch [bz#2059872]
- ci-Use-Network-Manager-and-Netplan-as-default-renderers.patch [bz#2059872]
- ci-Align-rhel-custom-files-with-upstream-1431.patch [bz#2082071]
- ci-Remove-rhel-specific-files.patch [bz#2082071]
- Resolves: bz#2059872
  ([RHEL-8]Rebase cloud-init from Fedora so it can configure networking using NM keyfiles)
- Resolves: bz#2082071
  (Align cloud.cfg file and systemd with cloud-init upstream .tmpl files)

* Mon Apr 25 2022 Amy Chen <xiachen@redhat.com> - 22.1-1
- Rebaes to 22.1 [bz#2065544]
- Resolves: bz#2065544
  ([RHEL-8.7.0] cloud-init rebase to 22.1)

* Fri Apr 01 2022 Camilla Conte <cconte@redhat.com> - 21.1-15
- ci-Detect-a-Python-version-change-and-clear-the-cache-8.patch [bz#1935826]
- ci-Fix-MIME-policy-failure-on-python-version-upgrade-93.patch [bz#1935826]
- Resolves: bz#1935826
  ([rhel-8] Cloud-init init stage fails after upgrade from RHEL7 to RHEL8.)

* Fri Feb 25 2022 Jon Maloy <jmaloy@redhat.com> - 21.1-14
- ci-Fix-IPv6-netmask-format-for-sysconfig-1215.patch [bz#2046540]
- Resolves: bz#2046540
  (cloud-init writes route6-$DEVICE config with a HEX netmask. ip route does not like : Error: inet6 prefix is expected rather than "fd00:fd00:fd00::/ffff:ffff:ffff:ffff::".)

* Tue Jan 25 2022 Jon Maloy <jmaloy@redhat.com> - 21.1-13
- ci-Add-flexibility-to-IMDS-api-version-793.patch [bz#2023940]
- ci-Azure-helper-Ensure-Azure-http-handler-sleeps-betwee.patch [bz#2023940]
- ci-azure-Removing-ability-to-invoke-walinuxagent-799.patch [bz#2023940]
- ci-Azure-eject-the-provisioning-iso-before-reporting-re.patch [bz#2023940]
- ci-Azure-Retrieve-username-and-hostname-from-IMDS-865.patch [bz#2023940]
- ci-Azure-Retry-net-metadata-during-nic-attach-for-non-t.patch [bz#2023940]
- ci-Azure-adding-support-for-consuming-userdata-from-IMD.patch [bz#2023940]
- Resolves: bz#2023940
  ([RHEL-8] Support for provisioning Azure VM with userdata)

* Wed Jan 19 2022 Jon Maloy <jmaloy@redhat.com> - 21.1-12
- ci-Add-gdisk-and-openssl-as-deps-to-fix-UEFI-Azure-init.patch [bz#2039697]
- ci-Datasource-for-VMware-953.patch [bz#2026587]
- ci-Change-netifaces-dependency-to-0.10.4-965.patch [bz#2026587]
- ci-Update-dscheck_VMware-s-rpctool-check-970.patch [bz#2026587]
- ci-Revert-unnecesary-lcase-in-ds-identify-978.patch [bz#2026587]
- ci-Add-netifaces-package-as-a-Requires-in-cloud-init.sp.patch [bz#2026587]
- Resolves: bz#2039697
  ([RHEL8] [Azure] cloud-init fails to configure the system)
- Resolves: bz#2026587
  ([cloud-init][RHEL8] Support for cloud-init datasource 'cloud-init-vmware-guestinfo')

* Wed Dec 08 2021 Jon Maloy <jmaloy@redhat.com> - 21.1-11
- ci-cloudinit-net-handle-two-different-routes-for-the-sa.patch [bz#2028028]
- Resolves: bz#2028028
  ([RHEL-8] Above 19.2 of cloud-init fails to configure routes when configuring static and default routes to the same destination IP)

* Mon Dec 06 2021 Jon Maloy <jmaloy@redhat.com> - 21.1-10
- ci-fix-error-on-upgrade-caused-by-new-vendordata2-attri.patch [bz#2021538]
- Resolves: bz#2021538
  (cloud-init.service fails to start after package update)

* Mon Oct 25 2021 Jon Maloy <jmaloy@redhat.com> - 21.1-9
- ci-cc_ssh.py-fix-private-key-group-owner-and-permission.patch [bz#2013644]
- Resolves: bz#2013644
  (cloud-init fails to set host key permissions correctly)

* Thu Sep 23 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-8
- ci-ssh_utils.py-ignore-when-sshd_config-options-are-not.patch [bz#1862933]
- Resolves: bz#1862933
  (cloud-init fails with ValueError: need more than 1 value to unpack[rhel-8])

* Fri Aug 27 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-7
- ci-Fix-home-permissions-modified-by-ssh-module-SC-338-9.patch [bz#1995840]
- Resolves: bz#1995840
  ([cloudinit]  Fix home permissions modified by ssh module)

* Wed Aug 11 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-6
- ci-Stop-copying-ssh-system-keys-and-check-folder-permis.patch [bz#1862967]
- Resolves: bz#1862967
  ([cloud-init]Customize ssh AuthorizedKeysFile causes login failure)

* Fri Aug 06 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-5
- ci-Add-dhcp-client-as-a-dependency.patch [bz#1977385]
- Resolves: bz#1977385
  ([Azure][RHEL-8] cloud-init must require dhcp-client on Azure)

* Mon Jul 19 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-4
- ci-ssh-util-allow-cloudinit-to-merge-all-ssh-keys-into-.patch [bz#1862967]
- Resolves: bz#1862967
  ([cloud-init]Customize ssh AuthorizedKeysFile causes login failure)

* Mon Jul 12 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-3
- ci-write-passwords-only-to-serial-console-lock-down-clo.patch [bz#1945891]
- Resolves: bz#1945891
  (CVE-2021-3429 cloud-init: randomly generated passwords logged in clear-text to world-readable file [rhel-8])

* Fri Jun 11 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-2
- ci-rhel-cloud.cfg-remove-ssh_genkeytypes-in-settings.py.patch [bz#1957532]
- ci-cloud-init.spec.template-update-systemd_postun-param.patch [bz#1952089]
- Resolves: bz#1957532
  ([cloud-init] From RHEL 82+ cloud-init no longer displays sshd keys fingerprints from instance launched from a backup image)
- Resolves: bz#1952089
  (cloud-init brew build fails on Fedora 33)

* Thu May 27 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-1.el8
- Rebaes to 21.1 [bz#1958174]
- Resolves: bz#1958174
  ([RHEL-8.5.0] Rebase cloud-init to 21.1)

* Thu May 13 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-10.el8_4.3
- ci-get_interfaces-don-t-exclude-Open-vSwitch-bridge-bon.patch [bz#1957135]
- ci-net-exclude-OVS-internal-interfaces-in-get_interface.patch [bz#1957135]
- Resolves: bz#1957135
  (Intermittent failure to start cloud-init due to failure to detect macs [rhel-8.4.0.z])

* Tue Apr 06 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-10.el8_4.1
- ci-Fix-requiring-device-number-on-EC2-derivatives-836.patch [bz#1942699]
- Resolves: bz#1942699
  ([Aliyun][RHEL8.4][cloud-init] cloud-init service failed to start with Alibaba instance [rhel-8.4.0.z])

* Tue Feb 02 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-10.el8
- ci-fix-a-typo-in-man-page-cloud-init.1-752.patch [bz#1913127]
- Resolves: bz#1913127
  (A typo in cloud-init man page)

* Tue Jan 26 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-9.el8
- ci-DataSourceAzure-update-password-for-defuser-if-exist.patch [bz#1900892]
- ci-Revert-ssh_util-handle-non-default-AuthorizedKeysFil.patch [bz#1919972]
- Resolves: bz#1900892
  ([Azure] Update existing user password RHEL8x)
- Resolves: bz#1919972
  ([RHEL-8.4] ssh keys can be shared across users giving potential root access)

* Thu Jan 21 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-8.el8
- ci-Missing-IPV6_AUTOCONF-no-to-render-sysconfig-dhcp6-s.patch [bz#1859695]
- Resolves: bz#1859695
  ([Cloud-init] DHCPv6 assigned address is not added to VM's interface)

* Tue Jan 05 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-7.el8
- ci-Report-full-specific-version-with-cloud-init-version.patch [bz#1898949]
- Resolves: bz#1898949
  (cloud-init should report full specific full version with "cloud-init --version")

* Mon Dec 14 2020 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-6.el8
- ci-Installing-man-pages-in-the-correct-place-with-corre.patch [bz#1612573]
- ci-Adding-BOOTPROTO-dhcp-to-render-sysconfig-dhcp6-stat.patch [bz#1859695]
- ci-Fix-unit-failure-of-cloud-final.service-if-NetworkMa.patch [bz#1898943]
- ci-ssh_util-handle-non-default-AuthorizedKeysFile-confi.patch [bz#1862967]
- Resolves: bz#1612573
  (Man page scan results for cloud-init)
- Resolves: bz#1859695
  ([Cloud-init] DHCPv6 assigned address is not added to VM's interface)
- Resolves: bz#1898943
  ([rhel-8]cloud-final.service fails if NetworkManager not installed.)
- Resolves: bz#1862967
  ([cloud-init]Customize ssh AuthorizedKeysFile causes login failure)

* Fri Nov 27 2020 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-5.el8
- ci-network-Fix-type-and-respect-name-when-rendering-vla.patch [bz#1881462]
- Resolves: bz#1881462
  ([rhel8][cloud-init] ifup bond0.504 Error: Connection activation failed: No suitable device found for this connection)

* Tue Nov 24 2020 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-4.el8
- ci-Changing-permission-of-cloud-init-generator-to-755.patch [bz#1897528]
- Resolves: bz#1897528
  (Change permission on ./systemd/cloud-init-generator.tmpl to 755 instead of 771)

* Fri Nov 13 2020 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-3.el8
- ci--Removing-net-tools-dependency.patch [bz#1881871]
- ci--Adding-man-pages-to-Red-Hat-spec-file.patch [bz#1612573]
- Resolves: bz#1881871
  (Remove net-tools legacy dependency from spec file)
- Resolves: bz#1612573
  (Man page scan results for cloud-init)

* Tue Nov 03 2020 Miroslav Rezanina <mrezanin@redhat.com> - 20.3-2.el8
- ci-Explicit-set-IPV6_AUTOCONF-and-IPV6_FORCE_ACCEPT_RA-.patch [bz#1889635]
- ci-Add-config-modules-for-controlling-IBM-PowerVM-RMC.-.patch [bz#1886430]
- Resolves: bz#1886430
  (Support for cloud-init config modules for PowerVM Hypervisor in Red Hat cloud-init)
- Resolves: bz#1889635
  (Add support for ipv6_autoconf on cloud-init-20.3)

* Fri Oct 23 2020 Eduardo Otubo <otubo@redhat.com> - 20.3-1.el8
- Rebase to cloud-init 20.3 [bz#1885185]
- Resolves: bz#1885185
  ([RHEL-8.4.0] cloud-init rebase to 20.3)

* Wed Sep 02 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-11.el8
- ci-cc_mounts-fix-incorrect-format-specifiers-316.patch [bz#1794664]
- Resolves: bz#1794664
  ([RHEL8] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init)

* Mon Aug 31 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-10.el8
- ci-Changing-notation-of-subp-call.patch [bz#1839662]
- Resolves: bz#1839662
  ([ESXi][RHEL8.3][cloud-init]ERROR log in cloud-init.log after clone VM on ESXi platform)

* Mon Aug 24 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-9.el8
- ci-Do-not-use-fallocate-in-swap-file-creation-on-xfs.-7.patch [bz#1794664]
- ci-swap-file-size-being-used-before-checked-if-str-315.patch [bz#1794664]
- ci-Detect-kernel-version-before-swap-file-creation-428.patch [bz#1794664]
- Resolves: bz#1794664
  ([RHEL8] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init)

* Mon Aug 17 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-8.el8
- ci-When-tools.conf-does-not-exist-running-cmd-vmware-to.patch [bz#1839662]
- ci-ssh-exit-with-non-zero-status-on-disabled-user-472.patch [bz#1833874]
- Resolves: bz#1833874
  ([rhel-8.3]using root user error should cause a non-zero exit code)
- Resolves: bz#1839662
  ([ESXi][RHEL8.3][cloud-init]ERROR log in cloud-init.log after clone VM on ESXi platform)

* Fri Jun 26 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-7.el8
- Fixing cloud-init-generator permissions [bz#1834173]
- Resolves: bz#1834173
  ([rhel-8.3]Incorrect ds-identify check in cloud-init-generator)

* Thu Jun 25 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-6.el8
- ci-ec2-only-redact-token-request-headers-in-logs-avoid-.patch [bz#1822343]
- Resolves: bz#1822343
  ([RHEL8.3] Do not log IMDSv2 token values into cloud-init.log)

* Wed Jun 24 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-5.el8
- ci-ec2-Do-not-log-IMDSv2-token-values-instead-use-REDAC.patch [bz#1822343]
- ci-Render-the-generator-from-template-instead-of-cp.patch [bz#1834173]
- ci-Change-from-redhat-to-rhel-in-systemd-generator-tmpl.patch [bz#1834173]
- ci-cloud-init.service.tmpl-use-rhel-instead-of-redhat-4.patch [bz#1834173]
- Resolves: bz#1822343
  ([RHEL8.3] Do not log IMDSv2 token values into cloud-init.log)
- Resolves: bz#1834173
  ([rhel-8.3]Incorrect ds-identify check in cloud-init-generator)

* Tue Jun 09 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-4.el8
- ci-changing-ds-identify-patch-from-usr-lib-to-usr-libex.patch [bz#1834173]
- Resolves: bz#1834173
  ([rhel-8.3]Incorrect ds-identify check in cloud-init-generator)

* Mon Jun 01 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-3.el8
- ci-Make-cloud-init.service-execute-after-network-is-up.patch [bz#1803928]
- Resolves: bz#1803928
  ([RHEL8.3] Race condition of starting cloud-init and NetworkManager)

* Thu May 28 2020 Miroslav Rezanina <mrezanin@redhat.com> - 19.4-2.el8
- ci-cc_set_password-increase-random-pwlength-from-9-to-2.patch [bz#1812171]
- ci-utils-use-SystemRandom-when-generating-random-passwo.patch [bz#1812174]
- ci-Enable-ssh_deletekeys-by-default.patch [bz#1814152]
- ci-Remove-race-condition-between-cloud-init-and-Network.patch [bz#1840648]
- Resolves: bz#1812171
  (CVE-2020-8632 cloud-init: Too short random password length in cc_set_password in config/cc_set_passwords.py [rhel-8])
- Resolves: bz#1812174
  (CVE-2020-8631 cloud-init: Use of random.choice when generating random password [rhel-8])
- Resolves: bz#1814152
  (CVE-2018-10896 cloud-init: default configuration disabled deletion of SSH host keys [rhel-8])
- Resolves: bz#1840648
  ([cloud-init][RHEL-8.2.0] /etc/resolv.conf lose config after reboot (initial instance is ok))

* Mon Apr 20 2020 Miroslav Rezanina <mrezanin@redhat.coM> - 19.4-1.el8.1
- Rebase to cloud-init 19.4 [bz#1811912]
- Resolves: bz#1811912
  ([RHEL-8.2.1] cloud-init rebase to 19.4)

* Tue Mar 10 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-12.el8
- ci-Remove-race-condition-between-cloud-init-and-Network.patch [bz#1807797]
- Resolves: bz#1807797
  ([cloud-init][RHEL-8.2.0] /etc/resolv.conf lose config after reboot (initial instance is ok))

* Thu Feb 20 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-11.el8
- ci-azure-avoid-re-running-cloud-init-when-instance-id-i.patch [bz#1788684]
- ci-net-skip-bond-interfaces-in-get_interfaces.patch [bz#1768770]
- ci-net-add-is_master-check-for-filtering-device-list.patch [bz#1768770]
- Resolves: bz#1768770
  (cloud-init complaining about enslaved mac)
- Resolves: bz#1788684
  ([RHEL-8] cloud-init Azure byte swap (hyperV Gen2 Only))

* Thu Feb 13 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-10.el8
- ci-cmd-main.py-Fix-missing-modules-init-key-in-modes-di.patch [bz#1802140]
- Resolves: bz#1802140
  ([cloud-init][RHEL8.2]cloud-init cloud-final.service fail with KeyError: 'modules-init' after upgrade to version 18.2-1.el7_6.1 in RHV)

* Tue Jan 28 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-9.el8
- ci-Removing-cloud-user-from-wheel.patch [bz#1785648]
- Resolves: bz#1785648
  ([RHEL8]cloud-user added to wheel group and sudoers.d causes 'sudo -v' prompts for passphrase)

* Fri Nov 22 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-8.el8
- ci-Fix-for-network-configuration-not-persisting-after-r.patch [bz#1706482]
- ci-util-json.dumps-on-python-2.7-will-handle-UnicodeDec.patch [bz#1744718]
- Resolves: bz#1706482
  ([cloud-init][RHVM]cloud-init network configuration does not persist reboot [RHEL 8.2.0])
- Resolves: bz#1744718
  ([cloud-init][RHEL8][OpenStack] cloud-init can't persist instance-data.json)

* Mon Jul 15 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-7.el8
- Fixing TPS [bz#1729864]
- Resolves: bz#1729864
 (cloud-init tps fail)

* Thu Jul 04 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el8
- ci-Revert-azure-ensure-that-networkmanager-hook-script-.patch [bz#1692914]
- ci-Azure-Return-static-fallback-address-as-if-failed-to.patch [bz#1691986]
- Resolves: bz#1691986
  ([Azure] [RHEL 8.1] Cloud-init fixes to support fast provisioning for Azure)
- Resolves: bz#1692914
  ([8.1] [WALA][cloud] cloud-init dhclient-hook script has some unexpected side-effects on Azure)

* Mon Jun 03 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-4.el8
- ci-Azure-Ensure-platform-random_seed-is-always-serializ.patch [bz#1691986]
- ci-DatasourceAzure-add-additional-logging-for-azure-dat.patch [bz#1691986]
- ci-Azure-Changes-to-the-Hyper-V-KVP-Reporter.patch [bz#1691986]
- ci-DataSourceAzure-Adjust-timeout-for-polling-IMDS.patch [bz#1691986]
- ci-cc_mounts-check-if-mount-a-on-no-change-fstab-path.patch [bz#1691986]
- Resolves: bz#1691986
  ([Azure] [RHEL 8.1] Cloud-init fixes to support fast provisioning for Azure)

* Tue Apr 16 2019 Danilo Cesar Lemes de Paula <ddepaula@redhat.com> - 18.5-3.el8
- ci-Adding-gating-tests-for-Azure-ESXi-and-AWS.patch [bz#1682786]
- Resolves: bz#1682786
  (cloud-init changes blocked until gating tests are added)

* Wed Apr 10 2019 Danilo C. L. de Paula <ddepaula@redhat.com> - 18.5-2
- Adding gating.yaml file
- Resolves: rhbz#1682786
  (cloud-init changes blocked until gating tests are added)


* Wed Apr 10 2019 Danilo de Paula <ddepaula@redhat.com: - 18.5-1.el8
- Rebase to cloud-init 18.5
- Resolves: bz#1687563
  (cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 8.0.1])

* Wed Jan 23 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-6.el8
- ci-net-Make-sysconfig-renderer-compatible-with-Network-.patch [bz#1602784]
- Resolves: bz#1602784
  (cloud-init: Sometimes image boots fingerprints is configured, there's a network device present but it's not configured)

* Fri Jan 18 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-5.el8
- ci-Fix-string-missmatch-when-mounting-ntfs.patch [bz#1664227]
- Resolves: bz#1664227
  ([Azure]String missmatch causes the /dev/sdb1 mounting failed after stop&start VM)

* Thu Jan 10 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-4.el8
- ci-Enable-cloud-init-by-default-on-vmware.patch [bz#1644335]
- Resolves: bz#1644335
  ([ESXi][RHEL8.0]Enable cloud-init by default on VMware)

* Wed Nov 28 2018 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-3.el8
- ci-Adding-systemd-mount-options-to-wait-for-cloud-init.patch [bz#1615599]
- ci-Azure-Ignore-NTFS-mount-errors-when-checking-ephemer.patch [bz#1615599]
- ci-azure-Add-reported-ready-marker-file.patch [bz#1615599]
- ci-Adding-disk_setup-to-rhel-cloud.cfg.patch [bz#1615599]
- Resolves: bz#1615599
  ([Azure] cloud-init fails to mount /dev/sdb1 after stop(deallocate)&&start VM)

* Tue Nov 06 2018 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-2.el7
- Revert "remove 'tee' command from logging configuration" [bz#1626117]
- Resolves: rhbz#1626117]
  (cloud-init-0.7.9-9 doesn't feed cloud-init-output.log)

* Fri Jun 29 2018 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-1.el7
- Rebase to 18.2 [bz#1515909]
  Resolves: rhbz#1515909

* Tue Feb 13 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-24
- Set DHCP_HOSTNAME on Azure to allow for the hostname to be
  published correctly when bouncing the network.
  Resolves: rhbz#1434109

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-23
- Fix a bug tha caused cloud-init to fail as a result of trying
  to rename bonds.
  Resolves: rhbz#1512247

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-22
- Apply patch from -21
  Resolves: rhbz#1489270

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-21
- sysconfig: Fix a potential traceback introduced in the
  0.7.9-17 build
  Resolves: rhbz#1489270

* Sun Dec 17 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-20
- sysconfig: Correct rendering for dhcp on ipv6
  Resolves: rhbz#1519271

* Thu Nov 30 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-19
- sysconfig: Fix rendering of default gateway for ipv6
  Resolves: rhbz#1492726

* Fri Nov 24 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-18
- Start the cloud-init init local service after the dbus socket is created
  so that the hostnamectl command works.
  Resolves: rhbz#1450521

* Tue Nov 21 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-17
- Correctly render DNS and DOMAIN for sysconfig
  Resolves: rhbz#1489270

* Mon Nov 20 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-16
- Disable NetworkManager management of resolv.conf if nameservers
  are specified by configuration.
  Resolves: rhbz#1454491

* Mon Nov 13 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-15
- Fix a null reference error in the rh_subscription module
  Resolves: rhbz#1498974

* Mon Nov 13 2017 Ryan McCabe <rmccabe@redhat.com> 0-7.9-14
- Include gateway if it's included in subnet configration
  Resolves: rhbz#1492726

* Sun Nov 12 2017 Ryan McCabe <rmccabe@redhat.com> 0-7.9-13
- Do proper cleanup of systemd units when upgrading from versions
  0.7.9-3 through 0.7.9-8.
  Resolves: rhbz#1465730

* Thu Nov 09 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-12
- Prevent Azure NM and dhclient hooks from running when cloud-init is
  disabled (rhbz#1474226)

* Tue Oct 31 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-11
- Fix rendering of multiple static IPs per interface file
  Resolves: rhbz#bz1497954

* Tue Sep 26 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-10
- AliCloud: Add support for the Alibaba Cloud datasource (rhbz#1482547)

* Thu Jun 22 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-9
- RHEL/CentOS: Fix default routes for IPv4/IPv6 configuration. (rhbz#1438082)
- azure: ensure that networkmanager hook script runs (rhbz#1440831 rhbz#1460206)
- Fix ipv6 subnet detection (rhbz#1438082)

* Tue May 23 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-8
- Update patches

* Mon May 22 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-7
- Add missing sysconfig unit test data (rhbz#1438082)
- Fix dual stack IPv4/IPv6 configuration for RHEL (rhbz#1438082)
- sysconfig: Raise ValueError when multiple default gateways are present. (rhbz#1438082)
- Bounce network interface for Azure when using the built-in path. (rhbz#1434109)
- Do not write NM_CONTROLLED=no in generated interface config files (rhbz#1385172)

* Wed May 10 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-6
- add power-state-change module to cloud_final_modules (rhbz#1252477)
- remove 'tee' command from logging configuration (rhbz#1424612)
- limit permissions on def_log_file (rhbz#1424612)
- Bounce network interface for Azure when using the built-in path. (rhbz#1434109)
- OpenStack: add 'dvs' to the list of physical link types. (rhbz#1442783)

* Wed May 10 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-5
- systemd: replace generator with unit conditionals (rhbz#1440831)

* Thu Apr 13 2017 Charalampos Stratakis <cstratak@redhat.com> 0.7.9-4
- Import to RHEL 7
Resolves:             rhbz#1427280

* Tue Mar 07 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-3
- fixes for network config generation
- avoid dependency cycle at boot (rhbz#1420946)

* Tue Jan 17 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-2
- use timeout from datasource config in openstack get_data (rhbz#1408589)

* Thu Dec 01 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.9-1
- Rebased on upstream 0.7.9.
- Remove dependency on run-parts

* Wed Jan 06 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-8
- make rh_subscription plugin do nothing in the absence of a valid
  configuration [RH:1295953]
- move rh_subscription module to cloud_config stage

* Wed Jan 06 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-7
- correct permissions on /etc/ssh/sshd_config [RH:1296191]

* Thu Sep 03 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-6
- rebuild for ppc64le

* Tue Jul 07 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-5
- bump revision for new build

* Tue Jul 07 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-4
- ensure rh_subscription plugin is enabled by default

* Wed Apr 29 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-3
- added dependency on python-jinja2 [RH:1215913]
- added rhn_subscription plugin [RH:1227393]
- require pyserial to support smartos data source [RH:1226187]

* Fri Jan 16 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-2
- Rebased RHEL version to Fedora rawhide
- Backported fix for https://bugs.launchpad.net/cloud-init/+bug/1246485
- Backported fix for https://bugs.launchpad.net/cloud-init/+bug/1411829

* Fri Nov 14 2014 Colin Walters <walters@redhat.com> - 0.7.6-1
- New upstream version [RH:974327]
- Drop python-cheetah dependency (same as above bug)
