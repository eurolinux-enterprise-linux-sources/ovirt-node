%define product_family oVirt Node
%define beta Beta
%define mgmt_scripts_dir %{_sysconfdir}/node.d
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Summary:        The oVirt Node daemons/scripts
Name:           ovirt-node
Version:        1.9.3
Release:        999%{?dist}%{?extra_release}
Source0:        %{name}-%{version}.tar.gz
License:        GPLv2+
Group:          Applications/System

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://www.ovirt.org/
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
BuildRequires:  libvirt-devel >= 0.5.1
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       libvirt >= 0.6.3
Requires:       augeas >= 0.3.5
#Requires:       libvirt-qpid >= 0.2.14-3
Requires:       udev >= 147-2.34
Requires:       wget
Requires:       cyrus-sasl-gssapi cyrus-sasl >= 2.1.22
Requires:       iscsi-initiator-utils
Requires:       ntp
Requires:       nfs-utils
#Requires:       glusterfs-client >= 2.0.1
Requires:       krb5-workstation
Requires:       bash
Requires:       chkconfig
Requires:       bind-utils
# Stupid yum dep solver pulls in older 'qemu' to resolve
# /usr/bin/qemu-img dep. This forces it to pick the new
# qemu-img RPM.
Requires:       qemu-img
Requires:       nc
Requires:       grub
Requires:       /usr/sbin/crond
#Requires:       anyterm
Requires:       newt-python
Requires:       libuser-python >= 0.56.9
Requires:       dbus-python
#Requires:       python-IPy

ExclusiveArch:  x86_64

%define app_root %{_datadir}/%{name}

%description
Provides a series of daemons and support utilities for hypervisor distribution.

%package tools
Summary:        oVirt Node tools for building and running an oVirt Node image
Group:          Applications/System
BuildArch:      noarch
BuildRequires:  pykickstart  >= 1.54
Requires:       livecd-tools >= 020-2

%define tools_root %{_datadir}/ovirt-node-tools

%description tools
The oVirt-node-tools package provides recipe (ks files), client tools,
documentation for building and running an oVirt Node image. This package
is not to be installed on the oVirt-Node, however on a development machine
to help in deployment on the node.

%prep
%setup -q

%build
%configure
# workaround for repos.ks
# for RHEL based image builds, brew spin-livecd uses Brew repos
make

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}

# FIXME move all installs into makefile
%{__install} -d -m0755 %{buildroot}%{_initrddir}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/cron.hourly
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -d -m0755 %{buildroot}%{mgmt_scripts_dir}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/cron.d
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
# remove nodeadmin from el6 build
#%{__install} -d -m0755 %{buildroot}%{python_sitelib}/nodeadmin

%{__install} -p -m0755 scripts/node-config %{buildroot}%{_sysconfdir}/sysconfig

%{__install} -p -m0755 scripts/ovirt-awake %{buildroot}%{_initrddir}
%{__install} -p -m0755 scripts/ovirt-early %{buildroot}%{_initrddir}
%{__install} -p -m0755 scripts/ovirt %{buildroot}%{_initrddir}
%{__install} -p -m0755 scripts/ovirt-post %{buildroot}%{_initrddir}
%{__install} -p -m0755 scripts/ovirt-firstboot %{buildroot}%{_initrddir}

%{__install} -p -m0644 logrotate/ovirt-logrotate %{buildroot}%{_sysconfdir}/cron.d
%{__install} -p -m0644 logrotate/ovirt-logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ovirt-node

#dracut module for disk cleanup
%{__install} -d -m0755 %{buildroot}%{_datadir}/dracut/modules.d/91ovirtnode
%{__install} -p -m0755 dracut/check %{buildroot}%{_datadir}/dracut/modules.d/91ovirtnode
%{__install} -p -m0755 dracut/install %{buildroot}%{_datadir}/dracut/modules.d/91ovirtnode
%{__install} -p -m0755 scripts/ovirt-boot-functions %{buildroot}%{_datadir}/dracut/modules.d/91ovirtnode
%{__install} -p -m0755 dracut/ovirt-cleanup.sh %{buildroot}%{_datadir}/dracut/modules.d/91ovirtnode

mkdir -p %{buildroot}/%{_sysconfdir}/default
echo "# File where default configuration is kept" > %{buildroot}/%{_sysconfdir}/default/ovirt

# ovirt-config-boot post-install hooks
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/ovirt-config-boot.d
# default hook for local_boot_trigger
%{__install} -p -m0755 scripts/local_boot_trigger.sh %{buildroot}%{_sysconfdir}/ovirt-config-boot.d

# newt UI
%{__install} -d -m0755 %{buildroot}%{python_sitelib}/ovirt_config_setup
%{__install} -p -m0644 scripts/__init__.py %{buildroot}%{python_sitelib}/ovirt_config_setup
#%{__install} -p -m0644 scripts/collectd.py %{buildroot}%{python_sitelib}/ovirt_config_setup
%{__install} -p -m0644 scripts/rhevm.py %{buildroot}%{python_sitelib}/ovirt_config_setup
%{__install} -p -m0644 scripts/rhn.py %{buildroot}%{python_sitelib}/ovirt_config_setup
%{__install} -d -m0755 %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/__init__.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/storage.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/password.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/install.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/iscsi.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/kdump.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/logging.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/ovirtfunctions.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0644 scripts/network.py %{buildroot}%{python_sitelib}/ovirtnode
%{__install} -p -m0755 scripts/ovirt-config-installer.py %{buildroot}%{_libexecdir}/ovirt-config-installer
%{__install} -p -m0755 scripts/ovirt-config-setup.py %{buildroot}%{_libexecdir}/ovirt-config-setup
%{__install} -p -m0755 scripts/ovirt-admin-shell %{buildroot}%{_libexecdir}
# python-augeas is not in RHEL-6
%{__install} -p -m0644 scripts/augeas.py %{buildroot}%{python_sitelib}

# default ovirt-config-setup menu options
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/ovirt-config-setup.d
%{__ln_s} ../..%{_libexecdir}/ovirt-config-storage %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"00_Disk Partitioning"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-password %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"05_Administrator Password"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-hostname %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"10_Set Hostname"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-iscsi %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"12_iSCSI Initiator Setup"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-networking %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"15_Networking Setup"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-kdump %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"20_Kdump Configuration"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-rhn %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"25_Register Host to RHN"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-snmp %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"26_Enable SNMP Agent"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-logging %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"30_Logging Setup"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-view-logs %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"90_View logs"
%{__ln_s} ../..%{_libexecdir}/ovirt-config-boot-wrapper %{buildroot}%{_sysconfdir}/ovirt-config-setup.d/"98_Local install and reboot"

# ovirt-early vendor hook dir
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/ovirt-early.d

# ovirt-node-tools
%{__install} -d -m0755 %{buildroot}%{tools_root}
#%{__install} -p -m0644 recipe/*.ks %{buildroot}%{tools_root}
%{__install} -p -m0755 tools/create-ovirt-iso-nodes %{buildroot}%{_sbindir}
%{__install} -p -m0755 tools/edit-livecd %{buildroot}%{_sbindir}
%{__install} -p -m0755 tools/livecd-setauth %{buildroot}%{_sbindir}
%{__install} -p -m0755 tools/livecd-rpms %{buildroot}%{_sbindir}


%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add ovirt-awake
/sbin/chkconfig --add ovirt-early
/sbin/chkconfig --add ovirt-firstboot
/sbin/chkconfig --add ovirt
/sbin/chkconfig --add ovirt-post
# workaround for imgcreate/live.py __copy_efi_files
if [ ! -e /boot/grub/splash.xpm.gz ]; then
  cp /usr/share/ovirt-node/grub-splash.xpm.gz /boot/grub/splash.xpm.gz
fi

%preun
if [ $1 = 0 ] ; then
    /sbin/service ovirt-early stop >/dev/null 2>&1
    /sbin/service ovirt-firstboor stop >/dev/null 2>&1
    /sbin/service ovirt stop >/dev/null 2>&1
    /sbin/service ovirt-post stop >/dev/null 2>&1
    /sbin/chkconfig --del ovirt-awake
    /sbin/chkconfig --del ovirt-early
    /sbin/chkconfig --del ovirt-firstboot
    /sbin/chkconfig --del ovirt
    /sbin/chkconfig --del ovirt-post
fi


%files tools
%defattr(0644,root,root,0755)
%doc README COPYING
%{tools_root}/*.ks
%defattr(0755,root,root,0755)
%{_sbindir}/node-creator
%{_sbindir}/create-ovirt-iso-nodes
%{_sbindir}/edit-livecd
%{_sbindir}/livecd-setauth
%{_sbindir}/livecd-rpms


%files
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/default/ovirt

%config(noreplace) %{_sysconfdir}/logrotate.d/ovirt-node
%config(noreplace) %{_sysconfdir}/cron.d/ovirt-logrotate

%{mgmt_scripts_dir}
%{_sysconfdir}/ovirt-config-boot.d
%{_sysconfdir}/ovirt-config-setup.d
%config(noreplace) %{_sysconfdir}/sysconfig/node-config

%doc COPYING
# should be ifarch i386
%{app_root}/grub-splash.xpm.gz
# end i386 bits
%{app_root}/syslinux-vesa-splash.jpg

%{_datadir}/dracut/modules.d/91ovirtnode/check
%{_datadir}/dracut/modules.d/91ovirtnode/install
%{_datadir}/dracut/modules.d/91ovirtnode/ovirt-boot-functions
%{_datadir}/dracut/modules.d/91ovirtnode/ovirt-cleanup.sh
%{_libexecdir}/ovirt-config-boot
%{_libexecdir}/ovirt-config-boot-wrapper
%{_libexecdir}/ovirt-config-hostname
%{_libexecdir}/ovirt-config-iscsi
%{_libexecdir}/ovirt-config-kdump
%{_libexecdir}/ovirt-config-logging
%{_libexecdir}/ovirt-config-networking
%{_libexecdir}/ovirt-config-password
%{_libexecdir}/ovirt-config-rhn
%{_libexecdir}/ovirt-config-setup
%{_libexecdir}/ovirt-config-setup-old
%{_libexecdir}/ovirt-config-snmp
%{_libexecdir}/ovirt-config-storage
%{_libexecdir}/ovirt-config-uninstall
%{_libexecdir}/ovirt-config-view-logs
%{_libexecdir}/ovirt-functions
%{_libexecdir}/ovirt-boot-functions
%{_libexecdir}/ovirt-install-node-stateless
%{_libexecdir}/ovirt-process-config
%{_libexecdir}/ovirt-rpmquery
%{_libexecdir}/ovirt-config-installer
%{_libexecdir}/ovirt-admin-shell
%{_sbindir}/gptsync
%{_sbindir}/showpart
%{_sbindir}/persist
%{_sbindir}/unpersist
%{python_sitelib}/ovirt_config_setup
%{python_sitelib}/ovirtnode
%{python_sitelib}/augeas*

%{_initrddir}/ovirt-awake
%{_initrddir}/ovirt-early
%{_initrddir}/ovirt-firstboot
%{_initrddir}/ovirt
%{_initrddir}/ovirt-post
%{_sysconfdir}/ovirt-early.d

%changelog
* Tue Apr 04 2010 Darryl L. Pierce <dpierce@redhat.com> - 1.9.2-1
- Updated autoconf environment.
- Allow persistence of empty configuration files.

* Wed Mar 24 2010 Darryl L. Pierce <dpierce@redhat.com> - 1.9.1-1
- Update ovirt-process-config to fail configs that are missing the field name or value.
- Updated build system will use Fedora 13 as the rawhide repo.
- Fixed ovirt-config-networking to not report success when network start fails.
- Reboot hangs on /etc [FIXED].
- Multipath translation performance improvements.
- Cleanup ROOTDRIVE when partitioning.
- Fix hang when cleaning dirty storage.
- The order of the oVirt SysVInit scripts has been changed.
-   ovirt-early -> ovirt-awake -> ovirt -> ovirt-post
- Fixes to the SysVINit scripts to name lifecycle methods propery.
- Added psmisc package.
- Added default KEYTAB_FILE name to /etc/sysconfig/node-config.
- Fixes to the persist and unpersist commands to handle already persisted files and directories.
- Duplicate NTP/DNS entries are rejected during network setup.

* Wed Oct 07 2009 David Huff <dhuff@redhat.com> - 1.0.3-4
- Added ovirt-node-tools subpackage

* Thu Jun 23 2009 David Huff <dhuff@redhat.com> - 1.0.3
- Clean up spec for inclusion in Fedora
- Removed subpackages, stateful, stateless, logos, and selinux

* Thu Dec 11 2008 Perry Myers <pmyers@redhat.com> - 0.96
- Subpackage stateful/stateless to separate out functionality for
  embedded Node and Node running as part of already installed OS
- ovirt-config-* setup scripts for standalone mode

* Thu Sep 11 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.7
- Add the ovirt-install- and ovirt-uninstall-node scripts, and refactor
  post to accomodate

* Mon Sep  8 2008 Jim Meyering <meyering@redhat.com> - 0.92 0.6
- Update ovirt-identify-node's build rule.

* Fri Aug 22 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.5
- Add the ovirt-listen-awake daemon to the RPM

* Fri Aug 22 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.4
- Re-arrange the directory layout, in preparation for ovirt-listen-awake

* Tue Jul 29 2008 Perry Myers <pmyers@redhat.com> - 0.92 0.2
- Added /etc/ovirt-release and merged ovirt-setup into spec file

* Wed Jul 02 2008 Darryl Pierce <dpierce@redhat.com> - 0.92 0.2
- Added log rotation to limit file system writes.

* Mon Jun 30 2008 Perry Myers <pmyers@redhat.com> - 0.92 0.1
- Add in sections of kickstart post, general cleanup
