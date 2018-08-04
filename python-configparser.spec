#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (not needed for Python 3.5+)

Summary:	Updated configparser from Python 3.5 to Python 2
Summary(pl.UTF-8):	Uaktualniony configparser z Pythona 3.5 do Pythona 2
Name:		python-configparser
Version:	3.5.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/configparser/
Source0:	https://files.pythonhosted.org/packages/source/c/configparser/configparser-%{version}.tar.gz
# Source0-md5:	cfdd915a5b7a6c09917a64a573140538
URL:		https://pypi.python.org/pypi/configparser
%if %{with python2}
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-backports
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ancient ConfigParser module available in the standard library 2.x
has seen a major update in Python 3.2. This is a backport of those
changes so that they can be used directly in Python 2.6 - 3.5.

%description -l pl.UTF-8
Przestarzały moduł ConfigParser dostępny w bibliotece standardowej
Pythona 2.x został znacząco uaktualniony w Pythonie 3.2. Niniejszy
moduł zawiera backport tych zmian, aby można ich było używać
bezpośrednio w Pythonie 2.6 - 3.5.

%package -n python3-configparser
Summary:	Updated configparser from Python 3.5 to older Python 3
Summary(pl.UTF-8):	Uaktualniony configparser z Pythona 3.5 do starszego Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-configparser
The ancient ConfigParser module available in the standard library 2.x
has seen a major update in Python 3.2. This is a backport of those
changes so that they can be used directly in Python 2.6 - 3.5.

%description -n python3-configparser -l pl.UTF-8
Przestarzały moduł ConfigParser dostępny w bibliotece standardowej
Pythona 2.x został znacząco uaktualniony w Pythonie 3.2. Niniejszy
moduł zawiera backport tych zmian, aby można ich było używać
bezpośrednio w Pythonie 2.6 - 3.5.

%prep
%setup -q -n configparser-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst configparser.rst
%{py_sitescriptdir}/backports/configparser
%{py_sitescriptdir}/configparser.py[co]
%{py_sitescriptdir}/configparser-%{version}-py*-nspkg.pth
%{py_sitescriptdir}/configparser-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-configparser
%defattr(644,root,root,755)
%doc README.rst configparser.rst
# XXX: shared dir
%dir %{py3_sitescriptdir}/backports
%{py3_sitescriptdir}/backports/configparser
%{py3_sitescriptdir}/configparser-%{version}-py*-nspkg.pth
%{py3_sitescriptdir}/configparser-%{version}-py*.egg-info
%endif
