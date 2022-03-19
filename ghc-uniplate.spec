#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	uniplate
Summary:	Help writing simple, concise and fast generic operations
Summary(pl.UTF-8):	Pomoc przy pisaniu prostych, zwięzłych i szybkich ogólnych operacji
Name:		ghc-%{pkgname}
Version:	1.6.12
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/uniplate
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	8a1914109e6707c4bab211d44c39f6c4
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/uniplate
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.4
BuildRequires:	ghc-containers
BuildRequires:	ghc-hashable >= 1.1.2.3
BuildRequires:	ghc-syb
BuildRequires:	ghc-unordered-containers >= 0.2.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.4
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-hashable-prof >= 1.1.2.3
BuildRequires:	ghc-syb-prof
BuildRequires:	ghc-unordered-containers-prof >= 0.2.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.4
Requires:	ghc-containers
Requires:	ghc-hashable >= 1.1.2.3
Requires:	ghc-syb
Requires:	ghc-unordered-containers >= 0.2.1
Obsoletes:	ghc-uniplate-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Uniplate is library for writing simple and concise generic operations.
Uniplate has similar goals to the original Scrap Your Boilerplate
work, but is substantially simpler and faster.

%description -l pl.UTF-8
Uniplate to biblioteka do pisania prostych i zwięzłych ogólnych
operacji. Ma podobne cele, co oryginalna paraca Scrap Your
Boilerplate, ale jest znacząco prostsza i szybsza.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.4
Requires:	ghc-containers-prof
Requires:	ghc-hashable-prof >= 1.1.2.3
Requires:	ghc-syb-prof
Requires:	ghc-unordered-containers-prof >= 0.2.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc uniplate.htm %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSuniplate-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSuniplate-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSuniplate-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Internal/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSuniplate-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Uniplate/Internal/*.p_hi
%endif
