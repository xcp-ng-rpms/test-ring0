%global package_speccommit 53ba8a919029ec3ce65eefdc1ef8e089672fa7e3
%global package_srccommit v2.0.1
Name: test-ring0
Group: System Environment/Kernel
License: GPLv2
Version: 2.0.1
Release: 8%{?xsrel}.1~testring0.5%{?dist}
Summary: Ring0 Tests
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, tar
BuildRequires: bzip2, findutils, gzip, m4, make >= 3.78
BuildRequires: gcc >= 2.96-98, binutils >= 2.12
BuildRequires: kernel-devel
BuildRequires: xen-libs-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: dwarves
%{?_cov_buildrequires}
Requires(post): /usr/sbin/depmod
Source0: test-ring0-2.0.1.tar.gz
Patch0: fix-pte-set-clear.patch
Patch1: fix-set-memory-uc.patch

%description
Assorted tests for components that ring0 is responsible for.  The
tests may be installed by XenRT test cases as part of the Ring0 BST
(or similar). Includes test modules for exercising the functionality
and performance of various bits of the Linux kernel.

%prep
%autosetup -p1
%{?_cov_prepare}

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

%post
/usr/sbin/depmod %{kernel_version}

%files
/lib/modules/%{kernel_version}/updates/*
%{_bindir}/*

%{?_cov_results_package}

%changelog
* Mon Oct 12 2026 Baptiste Le Duc <baptiste.le-duc@vates.tech> - 2.0.1-8.1
- Remove unused BuildRequires: perl (Yann Dirson)
- Add BuildRequires: dwarves (Corentin Oparowski)
- Remove module signing: drop BuildRequires: xssign-macros
- Support XCP-ng 9: fix two regressions from the 2.0.1 update:
    - pte-set-clear-flags: use vmalloc() result as the VA, not a vm_struct
    - set-memory-uc: keep the test result when restoring WB

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
