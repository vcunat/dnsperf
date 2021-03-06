Name:           dnsperf
Version:        2.2.0
Release:        1%{?dist}
Summary:        DNS Performance Testing Tool
Group:          Productivity/Networking/DNS/Utilities

License:        Apache-2.0
URL:            https://www.dns-oarc.net/tools/dnsperf
# Using same naming as to build debs, get the source (and rename it) at
# https://www.dns-oarc.net/tools/dnsperf and change %setup
Source0:        %{name}_%{version}.orig.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  bind-devel
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  libcap-devel
BuildRequires:  libxml2-devel
%if 0%{?suse_version} || 0%{?sle_version}
BuildRequires:  libjson-c-devel
%else
BuildRequires:  json-c-devel
%endif
BuildRequires:  GeoIP-devel

%description
dnsperf and resperf are free tools developed by Nominum/Akamai (2006-2018)
and DNS-OARC (since 2019) that make it simple to gather accurate latency and
throughput metrics for Domain Name Service (DNS). These tools are easy-to-use
and simulate typical Internet, so network operators can benchmark their naming
and addressing infrastructure and plan for upgrades. The latest version of
the dnsperf and resperf can be used with test files that include IPv6
queries.

dnsperf "self-paces" the DNS query load to simulate network conditions.

New features in dnsperf improve the precision of latency measurements and
allow for per packet per-query latency reporting is possible. dnsperf is
now multithreaded, multiple dnsperf clients can be supported in multicore
systems (each client requires two cores). The output of dnsperf has also
been improved so it is more concise and useful. Latency data can be used to
make detailed graphs, so it is simple for network operators to take advantage
of the data.


%package -n resperf
Summary:        DNS Resolution Performance Testing Tool
Group:          Productivity/Networking/DNS/Utilities


%description -n resperf
dnsperf and resperf are free tools developed by Nominum/Akamai (2006-2018)
and DNS-OARC (since 2019) that make it simple to gather accurate latency and
throughput metrics for Domain Name Service (DNS). These tools are easy-to-use
and simulate typical Internet, so network operators can benchmark their naming
and addressing infrastructure and plan for upgrades. The latest version of
the dnsperf and resperf can be used with test files that include IPv6
queries.

resperf systematically increases the query rate and monitors the response
rate to simulate caching DNS services.


%prep
%setup -q -n %{name}_%{version}


%build
sh autogen.sh
%configure
make %{?_smp_mflags}


%check
make test


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/dnsperf
%{_datadir}/doc/*
%{_mandir}/man1/dnsperf.*


%files -n resperf
%defattr(-,root,root)
%{_bindir}/resperf
%{_bindir}/resperf-report
%{_mandir}/man1/resperf.*


%changelog
* Mon Dec 03 2018 Jerry Lundström <lundstrom.jerry@gmail.com> 2.2.0-1
- Release 2.2.0
  * First release by DNS-OARC with a rework of the code to use autotools,
    semantic versioning 2.0 and bugfixes pulled from other's forks.
  * Bugfixes:
    - Fix infinite loop in argument parsing
    - Fix min/max latency summing for multithreaded runs
    - Fix calculation of per_thread socket counts
    - Fixes to queryparse
      - Mark correctly end of file
      - Support python3
      - Stop looping on end of file undefinitely
    - Fix compilation issues and work around missing `dns_fixedname_initname()`
    - Clang `scan-build` fixes
  * Other changes:
    - add "configure --with-bind" option
    - Handle bind library changes to HMAC (see #22) and other differences
      between versions
    - Workaround issue on FreeBSD (see #23)
    - Use `snprintf()` and OpenBSD's `strlcat()`
    - Add/update build dependencies for Debia, Ubuntu, CentOS, FreeBSD
      and OpenBSD
  * Commits:
    ae9bc91 Clang format
    b9bb085 CI, buildbot
    b84e41b Autotools, README, changelog
    a2e1732 License
    9dcb661 Remove $Id markers, Principal Author and Reviewed tags from the
            full source tree
    0677bf0 Use dns_fixedname_initname() where possible
    d8d4696 [master] add "configure --with-bind" option to dnsperf
    b71a280 Add deb based distros dependencies
    439c614 Replace custom isc_boolean_t with C standard bool type
    407ae7c Replace custom isc_u?intNN_t types with C99 u?intNN_t types
    c27afd4 Replace ISC_PRINT_QUADFORMAT with inttypes.h format constants
    6fdb2f7 Fix queryparse
    4909b78 README
    2782d50 README.md: Rectify link to software
    e31ddf4 fix calculation of per_thread socket counts
    3bd7fb4 Fix min/max latency summing for multithreaded runs
    2207e27 Fix infinite loop in argument parsing.
    3bfe97a Include the github URL; remove the bug reports section.
    0cee04a Add note about bug reports.
    62c4b32 add .gitignore
    c45f0be Initial import.
    149172b Initial commit
