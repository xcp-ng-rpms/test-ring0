Name: test-ring0
Group: System Environment/Kernel
License: GPLv2
Version: 1.0.4
Release: 1%{?dist}
Summary: Ring0 Tests
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: bzip2, findutils, gzip, m4, perl, make >= 3.78
BuildRequires: gcc >= 2.96-98, binutils >= 2.12, redhat-rpm-config >= 8.0.32.1
BuildRequires: kernel-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: xen-dom0-libs-devel xen-libs-devel
Requires(post): /usr/sbin/depmod

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/test-ring0/archive?at=v1.0.4&format=tar.gz&prefix=test-ring0-1.0.4#/test-ring0-1.0.4.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/test-ring0/archive?at=v1.0.4&format=tar.gz&prefix=test-ring0-1.0.4#/test-ring0-1.0.4.tar.gz) = 31fd4ec7dd309d24870efe0f789ca5a35bf27a94


%description
Assorted tests for components that ring0 is responsible for.  The
tests may be installed by XenRT test cases as part of the Ring0 BST
(or similar). Includes test modules for exercising the functionality
and performance of various bits of the Linux kernel.

%prep
%autosetup -p1

%build
cd linux
%{__make} KDIR=/lib/modules/%{kernel_version}/build

%install
cd linux
%{__make} KDIR=/lib/modules/%{kernel_version}/build \
     INSTALL_MOD_PATH=%{buildroot} \
     DESTDIR=%{buildroot} \
     DEPMOD=/bin/true \
     install

%post
/usr/sbin/depmod %{kernel_version}

%files
/lib/modules/%{kernel_version}/extra/*
%{_bindir}/*
