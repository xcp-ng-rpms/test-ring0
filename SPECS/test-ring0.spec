%global package_speccommit 53ba8a919029ec3ce65eefdc1ef8e089672fa7e3
%global package_srccommit v2.0.1
Name: test-ring0
Group: System Environment/Kernel
License: GPLv2
Version: 2.0.1
Release: 8%{?xsrel}.1%{?dist}
Summary: Ring0 Tests
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, tar
BuildRequires: bzip2, findutils, gzip, m4, make >= 3.78
BuildRequires: gcc >= 2.96-98, binutils >= 2.12
BuildRequires: kernel-devel
BuildRequires: xen-libs-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: dwarves
%if ! 0%{?xcpng}
BuildRequires: xssign-macros
%endif
%{?_cov_buildrequires}
Requires(post): /usr/sbin/depmod
Source0: test-ring0-2.0.1.tar.gz

%description
Assorted tests for components that ring0 is responsible for.  The
tests may be installed by XenRT test cases as part of the Ring0 BST
(or similar). Includes test modules for exercising the functionality
and performance of various bits of the Linux kernel.

%prep
%autosetup -p1
%{?_cov_prepare}

%if ! 0%{?xcpng}
%global certdir "%{_builddir}/certs"

cp -r /etc/pki/xs-secureboot-dev-certs "%{certdir}"
%certutil -d "%{dev_certdir}" -L -n "LINUX_SIGN_KEY_XS9_DEV" -r > "%{certdir}/kernel-dev.cer"
pk12util -d sql:"%{certdir}" -W "" -n LINUX_SIGN_KEY_XS9_DEV -o "%{certdir}/key.p12"
openssl pkcs12 -in "%{certdir}/key.p12" -passin pass: -nocerts -nodes -out "%{certdir}/private_key.pem"
%endif

%build
cd linux
%{?_cov_wrap} %{__make} KDIR=/lib/modules/%{kernel_version}/build

%install
cd linux
%{?_cov_wrap} %{__make} KDIR=/lib/modules/%{kernel_version}/build \
     INSTALL_MOD_PATH=%{buildroot} \
     DESTDIR=%{buildroot} \
     DEPMOD=/bin/true \
     install
%{?_cov_install}

# The RPM build system blindly runs strip on all output files which also
# destroys the signature on signed kernel modules. There is no way to disable
# this behavior and upstream refused to add an exception for .ko files. The
# macros below is more or less how Fedora and RHEL hack around this issue.
# https://bugzilla.redhat.com/show_bug.cgi?id=1967291
%define __modsign_install_post                          \
  sign_file=%(find /usr/src/ -name sign-file | tail -1) \
  find %{buildroot} -name "*.ko" -type f -exec ${sign_file} sha256 "%{certdir}/private_key.pem" "%{certdir}/kernel-dev.cer" {} \\;

%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

%post
/usr/sbin/depmod %{kernel_version}

%files
/lib/modules/%{kernel_version}/updates/*
%{_bindir}/*

%{?_cov_results_package}

%changelog
* Mon Jun 08 2026 Yann Dirson <yann.dirson@vates.tech> - 2.0.1-8.1
- (temporarily) Disable module-signing infrastructure
- Remove unused BuildRequires: perl

* Wed Dec 03 2025 Kevin Lampis <kevin.lampis@citrix.com> - 2.0.1-8
- CA-411782: Rebuild against kernel 6.6.98-13

* Thu Nov 13 2025 Lin Liu <lin.liu01@cloud.com> -2.0.1-7
- CP-310158: Rebuild with kernel 6.6.98-12

* Mon Nov 03 2025 Deli Zhang <deli.zhang@citrix.com> - 2.0.1-6
- CP-310026: Bump release to 6, rebuild against kernel 6.6.98-9

* Thu Sep 25 2025 Chunjie Zhu <chunjie.zhu@citrix.com> - 2.0.1-5
- Bump release to 5, rebuild against kernel 6.6.98-5

* Fri Aug 1 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 2.0.1-4
- CP-308667: kernel upgrade, Bump release to 4

* Fri Apr 11 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.1-3
- CA-401825: Sign kernel module

* Wed Mar 12 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 2.0.1-2
- Update with NUMA enabled

* Wed Mar 05 2025 Frediano Ziglio <frediano.ziglio@cloud.com> - 2.0.1-1
- CP-53618: Use procfs instead of debugfs for Secure Boot

* Thu Feb 13 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 2.0.0-3
- Bump release to 3

* Sun Jan 26 2025 Chunjie Zhu <chunjie.zhu@cloud.com> - 2.0.0-2
- Update with kABI support

* Fri Dec 06 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.0-1
- Update to target the 6.6 kernel

* Thu Mar 17 2022 Deli Zhang <deli.zhang@citrix.com> - 1.0.7-3
* Bump release to 3

* Thu Mar 17 2022 Deli Zhang <deli.zhang@citrix.com> - 1.0.7-2
* CP-39193: Disable static analysis

* Sun Mar 13 2022 Deli Zhang <deli.zhang@citrix.com> - 1.0.7-1
- CP-39193: Add kernel livepatch test modules

* Mon Feb 21 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.6-2
- CP-38416: Enable static analysis

* Tue Mar 30 2021 Andrew Cooper <andrew.cooper3@citrix.com> - 1.0.6-1
- Remove dependences on unstable Xen libraries

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.5-1
- CA-346372: Add a PoC for XSA-331
