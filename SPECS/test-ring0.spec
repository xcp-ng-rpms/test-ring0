%global package_speccommit 2cc68c53415b27b76fdfd217ceabf995be2ca265
%global package_srccommit v1.0.7
Name: test-ring0
Group: System Environment/Kernel
License: GPLv2
Version: 1.0.7
Release: 3%{?xsrel}%{?dist}
Summary: Ring0 Tests
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: bzip2, findutils, gzip, m4, perl, make >= 3.78
BuildRequires: gcc >= 2.96-98, binutils >= 2.12, redhat-rpm-config >= 8.0.32.1
BuildRequires: kernel-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: xen-libs-devel
%{?_cov_buildrequires}
Requires(post): /usr/sbin/depmod
Source0: test-ring0-1.0.7.tar.gz

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
/lib/modules/%{kernel_version}/extra/*
%{_bindir}/*

%{?_cov_results_package}

%changelog
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
