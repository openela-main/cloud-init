Name:                 cloud-init
Version:              22.1
Release:              10.el9_2.0.2
Summary:              Cloud instance init scripts
License:              ASL 2.0 or GPLv3
URL:                  http://launchpad.net/cloud-init
Source0:              https://launchpad.net/cloud-init/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Source1:              cloud-init-tmpfiles.conf

Patch0001:            0001-Add-initial-redhat-changes.patch
Patch0002:            0002-Do-not-write-NM_CONTROLLED-no-in-generated-interface.patch
Patch0003:            0003-Adding-_netdev-to-the-default-mount-configuration.patch
Patch0004:            0004-Setting-highest-autoconnect-priority-for-network-scr.patch
Patch0005:            0005-limit-permissions-on-def_log_file.patch
Patch0006:            0006-rhel-cloud.cfg-remove-ssh_genkeytypes-in-settings.py.patch
# For bz#2056964 - [RHEL-9]Rebase cloud-init from Fedora so it can configure networking using NM keyfiles
Patch7:               ci-Add-native-NetworkManager-support-1224.patch
# For bz#2056964 - [RHEL-9]Rebase cloud-init from Fedora so it can configure networking using NM keyfiles
Patch8:               ci-Use-Network-Manager-and-Netplan-as-default-renderers.patch
# For bz#2056964 - [RHEL-9]Rebase cloud-init from Fedora so it can configure networking using NM keyfiles
Patch9:               ci-Revert-Setting-highest-autoconnect-priority-for-netw.patch
# For bz#2088448 - Align cloud.cfg file and systemd with cloud-init upstream .tmpl files
Patch10:              ci-Align-rhel-custom-files-with-upstream-1431.patch
# For bz#2088448 - Align cloud.cfg file and systemd with cloud-init upstream .tmpl files
Patch11:              ci-Remove-rhel-specific-files.patch
# For bz#2091640 - [cloud][init] Add support for reading tags from instance metadata
Patch12:              ci-Support-EC2-tags-in-instance-metadata-1309.patch
# For bz#1980403 - [RHV] RHEL 9 VM with cloud-init without hostname set doesn't result in the FQDN as hostname
Patch13:              ci-cc_set_hostname-do-not-write-localhost-when-no-hostn.patch
# For bz#2061604 - cloud-config will change /etc/locale.conf back to en_US.UTF-8 on rhel-guest-image-9.0
Patch14:              ci-Honor-system-locale-for-RHEL-1355.patch
# For bz#2096270 - Adjust udev/rules default path[rhel-9]
Patch15:              ci-setup.py-adjust-udev-rules-default-path-1513.patch
# For bz#2107463 - [RHEL-9.1] Cannot run sysconfig when changing the priority of network renderers
# For bz#2104389 - [RHEL-9.1]Failed to config static IP and IPv6 according to VMware Customization Config File
# For bz#2117532 - [RHEL9.1] Revert patch of configuring networking by NM keyfiles
# For bz#2098501 - [RHEL-9.1] IPv6 not workable when cloud-init configure network using NM keyfiles
Patch16:              ci-Revert-Add-native-NetworkManager-support-1224.patch
# For bz#2107463 - [RHEL-9.1] Cannot run sysconfig when changing the priority of network renderers
# For bz#2104389 - [RHEL-9.1]Failed to config static IP and IPv6 according to VMware Customization Config File
# For bz#2117532 - [RHEL9.1] Revert patch of configuring networking by NM keyfiles
# For bz#2098501 - [RHEL-9.1] IPv6 not workable when cloud-init configure network using NM keyfiles
Patch17:              ci-Revert-Use-Network-Manager-and-Netplan-as-default-re.patch
# For bz#2107463 - [RHEL-9.1] Cannot run sysconfig when changing the priority of network renderers
# For bz#2104389 - [RHEL-9.1]Failed to config static IP and IPv6 according to VMware Customization Config File
# For bz#2117532 - [RHEL9.1] Revert patch of configuring networking by NM keyfiles
# For bz#2098501 - [RHEL-9.1] IPv6 not workable when cloud-init configure network using NM keyfiles
Patch18:              ci-Revert-Revert-Setting-highest-autoconnect-priority-f.patch
# For bz#2115565 - cloud-init configures user "centos" or "rhel" instead of "cloud-user" with cloud-init-22.1
Patch19:              ci-cloud.cfg.tmpl-make-sure-centos-settings-are-identic.patch
# For bz#2152100 - [RHEL-9] Ensure network ready before cloud-init service runs on RHEL
Patch20:              ci-Ensure-network-ready-before-cloud-init-service-runs-.patch
# For bz#2140893 - systemd[1]: Failed to start Initial cloud-init job after reboot system via sysrq 'b'
Patch21:              ci-cc_set_hostname-ignore-var-lib-cloud-data-set-hostna.patch
# For bz#2166245 - Add support for resizing encrypted root volume
Patch22:              ci-Allow-growpart-to-resize-encrypted-partitions-1316.patch
Patch23:              future-backport.patch
Patch24:              0001-Remove-rh-subscription.patch

# Source-git patches

BuildArch:            noarch

BuildRequires:        pkgconfig(systemd)
BuildRequires:        python3-devel
BuildRequires:        python3-setuptools
BuildRequires:        systemd

# For tests
BuildRequires:        iproute
BuildRequires:        python3-configobj
# https://bugzilla.redhat.com/show_bug.cgi?id=1695953
BuildRequires:        python3-distro
# https://bugzilla.redhat.com/show_bug.cgi?id=1417029
BuildRequires:        python3-httpretty >= 0.8.14-2
BuildRequires:        python3-jinja2
BuildRequires:        python3-jsonpatch
BuildRequires:        python3-oauthlib
BuildRequires:        python3-prettytable
BuildRequires:        python3-pyserial
BuildRequires:        python3-PyYAML
BuildRequires:        python3-requests
BuildRequires:        python3-six
# dnf is needed to make cc_ntp unit tests work
# https://bugs.launchpad.net/cloud-init/+bug/1721573
BuildRequires:        /usr/bin/dnf

Requires:             e2fsprogs
Requires:             iproute
Requires:             libselinux-python3
Requires:             policycoreutils-python3
Requires:             procps
Requires:             python3-configobj
# https://bugzilla.redhat.com/show_bug.cgi?id=1695953
Requires:             python3-distro
Requires:             python3-jinja2
Requires:             python3-jsonpatch
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
# https://bugzilla.redhat.com/show_bug.cgi?id=2032524
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

%if 0%{?fedora}
python3 tools/render-cloudcfg --variant fedora > $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg
%endif

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

[ ! -d $RPM_BUILD_ROOT%{_systemdgeneratordir} ] && mkdir -p $RPM_BUILD_ROOT%{_systemdgeneratordir}
python3 tools/render-cloudcfg --variant rhel systemd/cloud-init-generator.tmpl > $RPM_BUILD_ROOT%{_systemdgeneratordir}/cloud-init-generator
chmod 755 $RPM_BUILD_ROOT%{_systemdgeneratordir}/cloud-init-generator

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


%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
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
%{_systemdgeneratordir}/cloud-init-generator
%{_sysconfdir}/systemd/system/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf

%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf

%changelog
* Thu Jan 25 2024 Release Engineering <releng@openela.org> - 22.1.0.2
- Apply OpenELA fixes

* Tue Jun 27 2023 Camilla Conte <cconte@redhat.com> - 22.1-10.el9_2
- Resolves: bz#2217065

* Wed Feb 08 2023 Camilla Conte <cconte@redhat.com> - 22.1-9
- ci-Allow-growpart-to-resize-encrypted-partitions-1316.patch [bz#2166245]
- Resolves: bz#2166245
  (Add support for resizing encrypted root volume)

* Fri Jan 27 2023 Camilla Conte <cconte@redhat.com> - 22.1-8
- ci-cc_set_hostname-ignore-var-lib-cloud-data-set-hostna.patch [bz#2140893]
- Resolves: bz#2140893
(systemd[1]: Failed to start Initial cloud-init job after reboot system via sysrq 'b')

* Wed Dec 21 2022 Camilla Conte <cconte@redhat.com> - 22.1-7
- ci-Ensure-network-ready-before-cloud-init-service-runs-.patch [bz#2152100]
- Resolves: bz#2152100
  ([RHEL-9] Ensure network ready before cloud-init service runs on RHEL)

* Tue Sep 27 2022 Camilla Conte <cconte@redhat.com> - 22.1-6
- ci-cloud.cfg.tmpl-make-sure-centos-settings-are-identic.patch [bz#2115565]
- Resolves: bz#2115565
  (cloud-init configures user "centos" or "rhel" instead of "cloud-user" with cloud-init-22.1)

* Wed Aug 17 2022 Miroslav Rezanina <mrezanin@redhat.com> - 22.1-5
- ci-Revert-Add-native-NetworkManager-support-1224.patch [bz#2107463 bz#2104389 bz#2117532 bz#2098501]
- ci-Revert-Use-Network-Manager-and-Netplan-as-default-re.patch [bz#2107463 bz#2104389 bz#2117532 bz#2098501]
- ci-Revert-Revert-Setting-highest-autoconnect-priority-f.patch [bz#2107463 bz#2104389 bz#2117532 bz#2098501]
- Resolves: bz#2107463
  ([RHEL-9.1] Cannot run sysconfig when changing the priority of network renderers)
- Resolves: bz#2104389
  ([RHEL-9.1]Failed to config static IP and IPv6 according to VMware Customization Config File)
- Resolves: bz#2117532
  ([RHEL9.1] Revert patch of configuring networking by NM keyfiles)
- Resolves: bz#2098501
  ([RHEL-9.1] IPv6 not workable when cloud-init configure network using NM keyfiles)

* Thu Jun 23 2022 Jon Maloy <jmaloy@redhat.com> - 22.1-4
- ci-Honor-system-locale-for-RHEL-1355.patch [bz#2061604]
- ci-cloud-init.spec-adjust-path-for-66-azure-ephemeral.r.patch [bz#2096270]
- ci-setup.py-adjust-udev-rules-default-path-1513.patch [bz#2096270]
- Resolves: bz#2061604
  (cloud-config will change /etc/locale.conf back to en_US.UTF-8 on rhel-guest-image-9.0)
- Resolves: bz#2096270
  (Adjust udev/rules default path[rhel-9])

* Wed Jun 08 2022 Miroslav Rezanina <mrezanin@redhat.com> - 22.1-3
- ci-Support-EC2-tags-in-instance-metadata-1309.patch [bz#2091640]
- ci-cc_set_hostname-do-not-write-localhost-when-no-hostn.patch [bz#1980403]
- Resolves: bz#2091640
  ([cloud][init] Add support for reading tags from instance metadata)
- Resolves: bz#1980403
  ([RHV] RHEL 9 VM with cloud-init without hostname set doesn't result in the FQDN as hostname)

* Tue May 31 2022 Miroslav Rezanina <mrezanin@redhat.com> - 22.1-2
- ci-Add-native-NetworkManager-support-1224.patch [bz#2056964]
- ci-Use-Network-Manager-and-Netplan-as-default-renderers.patch [bz#2056964]
- ci-Revert-Setting-highest-autoconnect-priority-for-netw.patch [bz#2056964]
- ci-Align-rhel-custom-files-with-upstream-1431.patch [bz#2088448]
- ci-Remove-rhel-specific-files.patch [bz#2088448]
- Resolves: bz#2056964
  ([RHEL-9]Rebase cloud-init from Fedora so it can configure networking using NM keyfiles)
- Resolves: bz#2088448
  (Align cloud.cfg file and systemd with cloud-init upstream .tmpl files)

* Tue Apr 19 2022 Emanuele Giuseppe Esposito <eesposit@redhat.com> - 22.1-1
- Rebase to 22.1 [bz#2065548]
- Resolves: bz#2065548
  ([RHEL-9.1] cloud-init rebase to 22.1)

* Fri Feb 25 2022 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-19
- ci-Fix-IPv6-netmask-format-for-sysconfig-1215.patch [bz#2053546]
- ci-Adding-_netdev-to-the-default-mount-configuration.patch [bz#1998445]
- ci-Setting-highest-autoconnect-priority-for-network-scr.patch [bz#2036060]
- Resolves: bz#2053546
  (cloud-init writes route6-$DEVICE config with a HEX netmask. ip route does not like : Error: inet6 prefix is expected rather than "fd00:fd00:fd00::/ffff:ffff:ffff:ffff::".)
- Resolves: bz#1998445
  ([Azure][RHEL-9] ordering cycle exists after reboot)
- Resolves: bz#2036060
  ([cloud-init][ESXi][RHEL-9] Failed to config static IP according to VMware Customization Config File)

* Fri Feb 11 2022 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-18
- ci-Add-_netdev-option-to-mount-Azure-ephemeral-disk-121.patch [bz#1998445]
- Resolves: bz#1998445
  ([Azure][RHEL-9] ordering cycle exists after reboot)

* Mon Feb 07 2022 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-17
- ci-Add-flexibility-to-IMDS-api-version-793.patch [bz#2042351]
- ci-Azure-helper-Ensure-Azure-http-handler-sleeps-betwee.patch [bz#2042351]
- ci-azure-Removing-ability-to-invoke-walinuxagent-799.patch [bz#2042351]
- ci-Azure-eject-the-provisioning-iso-before-reporting-re.patch [bz#2042351]
- ci-Azure-Retrieve-username-and-hostname-from-IMDS-865.patch [bz#2042351]
- ci-Azure-Retry-net-metadata-during-nic-attach-for-non-t.patch [bz#2042351]
- ci-Azure-adding-support-for-consuming-userdata-from-IMD.patch [bz#2042351]
- Resolves: bz#2042351
  ([RHEL-9] Support for provisioning Azure VM with userdata)

* Fri Jan 21 2022 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-16
- ci-Datasource-for-VMware-953.patch [bz#2040090]
- ci-Change-netifaces-dependency-to-0.10.4-965.patch [bz#2040090]
- ci-Update-dscheck_VMware-s-rpctool-check-970.patch [bz#2040090]
- ci-Revert-unnecesary-lcase-in-ds-identify-978.patch [bz#2040090]
- ci-Add-netifaces-package-as-a-Requires-in-cloud-init.sp.patch [bz#2040090]
- Resolves: bz#2040090
  ([cloud-init][RHEL9] Support for cloud-init datasource 'cloud-init-vmware-guestinfo')

* Thu Jan 13 2022 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-15
- ci-Add-gdisk-and-openssl-as-deps-to-fix-UEFI-Azure-init.patch [bz#2032524]
- Resolves: bz#2032524
  ([RHEL9] [Azure] cloud-init fails to configure the system)

* Tue Dec 14 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-14
- ci-cloudinit-net-handle-two-different-routes-for-the-sa.patch [bz#2028031]
- Resolves: bz#2028031
  ([RHEL-9] Above 19.2 of cloud-init fails to configure routes when configuring static and default routes to the same destination IP)

* Mon Dec 06 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-13
- ci-fix-error-on-upgrade-caused-by-new-vendordata2-attri.patch [bz#2028381]
- Resolves: bz#2028381
  (cloud-init.service fails to start after package update)

* Mon Nov 01 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-12
- ci-remove-unnecessary-EOF-string-in-disable-sshd-keygen.patch [bz#2016305]
- Resolves: bz#2016305
  (disable-sshd-keygen-if-cloud-init-active.conf:8: Missing '=', ignoring line)

* Tue Oct 26 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-11
- ci-cc_ssh.py-fix-private-key-group-owner-and-permission.patch [bz#2015974]
- Resolves: bz#2015974
  (cloud-init fails to set host key permissions correctly)

* Mon Oct 18 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-10
- ci-Inhibit-sshd-keygen-.service-if-cloud-init-is-active.patch [bz#2002492]
- ci-add-the-drop-in-also-in-the-files-section-of-cloud-i.patch [bz#2002492]
- Resolves: bz#2002492
  (util.py[WARNING]: Failed generating key type rsa to file /etc/ssh/ssh_host_rsa_key)

* Fri Sep 10 2021 Miroslav Rezanina mrezanin@redhat.com - 21.1-9
- ci-ssh_utils.py-ignore-when-sshd_config-options-are-not.patch [bz#2002302]
- Resolves: bz#2002302
  (cloud-init fails with ValueError: need more than 1 value to unpack[rhel-9])

* Fri Sep 03 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-8
- ci-Fix-home-permissions-modified-by-ssh-module-SC-338-9.patch [bz#1995843]
- Resolves: bz#1995843
  ([cloudinit]  Fix home permissions modified by ssh module)

* Mon Aug 16 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-7
- ci-Stop-copying-ssh-system-keys-and-check-folder-permis.patch [bz#1979099]
- ci-Report-full-specific-version-with-cloud-init-version.patch [bz#1971002]
- Resolves: bz#1979099
  ([cloud-init]Customize ssh AuthorizedKeysFile causes login failure[RHEL-9.0])
- Resolves: bz#1971002
  (cloud-init should report full specific full version with "cloud-init --version" [rhel-9])

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 21.1-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Aug 06 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-5
- ci-Add-dhcp-client-as-a-dependency.patch [bz#1964900]
- Resolves: bz#1964900
  ([Azure][RHEL-9] cloud-init must require dhcp-client on Azure)

* Thu Jul 15 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-4
- ci-write-passwords-only-to-serial-console-lock-down-clo.patch [bz#1945892]
- ci-ssh-util-allow-cloudinit-to-merge-all-ssh-keys-into-.patch [bz#1979099]
- Resolves: bz#1945892
  (CVE-2021-3429 cloud-init: randomly generated passwords logged in clear-text to world-readable file [rhel-9.0])
- Resolves: bz#1979099
  ([cloud-init]Customize ssh AuthorizedKeysFile causes login failure[RHEL-9.0])

* Fri Jul 02 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-3
- ci-Fix-requiring-device-number-on-EC2-derivatives-836.patch [bz#1943511]
- Resolves: bz#1943511
  ([Aliyun][RHEL9.0][cloud-init] cloud-init service failed to start with Alibaba instance)

* Mon Jun 21 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-2
- ci-rhel-cloud.cfg-remove-ssh_genkeytypes-in-settings.py.patch [bz#1970909]
- ci-Use-_systemdgeneratordir-macro-for-cloud-init-genera.patch [bz#1971480]
- Resolves: bz#1970909
  ([cloud-init] From RHEL 82+ cloud-init no longer displays sshd keys fingerprints from instance launched from a backup image[rhel-9])
- Resolves: bz#1971480
  (Use systemdgenerators macro in spec file)

* Thu Jun 10 2021 Miroslav Rezanina <mrezanin@redhat.com> - 21.1-1
- Rebase to 21.1 [bz#1958209]
- Resolves: bz#1958209
  ([RHEL-9.0] Rebase cloud-init to 21.1)

* Wed Apr 21 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.4-5
- Removing python-mock dependency
- Resolves: bz#1922323

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 20.4-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Apr 07 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20.4-3.el9
- ci-Removing-python-nose-and-python-tox-as-dependency.patch [bz#1916777 bz#1918892]
- Resolves: bz#1916777
  (cloud-init requires python-nose)
- Resolves: bz#1918892
  (cloud-init requires tox)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 Eduardo Otubo <otubo@redhat.com> - 20.4-2
- Updated to 20.4 [bz#1902250]

* Mon Sep 07 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-7
- Fix execution fail with backtrace

* Mon Sep 07 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-6
- Adding missing patches to spec file

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 19.4-4
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-3
- Fix BZ#1798729 - CVE-2020-8632 cloud-init: Too short random password length
  in cc_set_password in config/cc_set_passwords.py
- Fix BZ#1798732 - CVE-2020-8631 cloud-init: Use of random.choice when
  generating random password

* Sun Feb 23 2020 Dusty Mabe <dusty@dustymabe.com> - 19.4-2
- Fix sed substitutions for unittest2 and assertItemsEqual
- Fix failing unittests by including `BuildRequires: passwd`
    - The unittests started failing because of upstream commit
      7c07af2 where cloud-init can now support using `usermod` to
      lock an account if `passwd` isn't installed. Since `passwd`
      wasn't installed in our mock buildroot it was choosing to
      use `usermod` and the unittests were failing. See:
      https://github.com/canonical/cloud-init/commit/7c07af2
- Add missing files to package
    - /usr/bin/cloud-id
    - /usr/share/bash-completion/completions/cloud-init

* Fri Feb 14 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-1
- Updated to 19.4
- Rebasing the Fedora specific patches but removing patches that don't apply anymore

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Miro Hrončok <mhroncok@redhat.com> - 17.1-14
- Drop unneeded build dependency on python3-unittest2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 17.1-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 17.1-12
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-10
- Add patch to replace platform.dist() [RH:1695953]
- Add (Build)Requires: python3-distro

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-9
- Fix %%systemd_postun macro [RH:1695953]
- Add patch to fix failing test for EPOCHREALTIME bash env [RH:1695953]

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 17.1-6
- Rebuilt for Python 3.7

* Sat Apr 21 2018 Lars Kellogg-Stedman <lars@redhat.com> - 17.1-5
- Enable dhcp on EC2 interfaces with only local ipv4 addresses [RH:1569321]
  (cherry pick upstream commit eb292c1)

* Mon Mar 26 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 17.1-4
- Make sure the patch does not add infinitely many entries

* Mon Mar 26 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 17.1-3
- Add patch to retain old values of /etc/sysconfig/network

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct  4 2017 Garrett Holmstrom <gholms@fedoraproject.org> - 17.1-1
- Updated to 17.1

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
