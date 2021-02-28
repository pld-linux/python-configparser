#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (not needed for Python 3.7+)

Summary:	Updated configparser from Python 3.7 to Python 2
Summary(pl.UTF-8):	Uaktualniony configparser z Pythona 3.7 do Pythona 2
Name:		python-configparser
Version:	4.0.2
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/configparser/
Source0:	https://files.pythonhosted.org/packages/source/c/configparser/configparser-%{version}.tar.gz
# Source0-md5:	35926cc4b9133f1f9ca70a1fd2fdf237
URL:		https://pypi.org/project/configparser/
%if %{with python2}
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with additional_tests}
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-black-multipy
BuildRequires:	python-pytest-checkdocs >= 1.2
BuildRequires:	python-pytest-flake8
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with additional_tests}
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
BuildRequires:	python3-pytest-checkdocs >= 1.2
BuildRequires:	python3-pytest-flake8
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 3.2
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-backports
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ancient ConfigParser module available in the standard library 2.x
has seen a major update in Python 3.2. This is a backport of those
changes so that they can be used directly in Python 2.6 - 3.6.

%description -l pl.UTF-8
Przestarzały moduł ConfigParser dostępny w bibliotece standardowej
Pythona 2.x został znacząco uaktualniony w Pythonie 3.2. Niniejszy
moduł zawiera backport tych zmian, aby można ich było używać
bezpośrednio w Pythonie 2.6 - 3.6.

%package -n python3-configparser
Summary:	Updated configparser from Python 3.7 to older Python 3
Summary(pl.UTF-8):	Uaktualniony configparser z Pythona 3.7 do starszego Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-configparser
The ancient ConfigParser module available in the standard library 2.x
has seen a major update in Python 3.2. This is a backport of those
changes so that they can be used directly in Python 2.6 - 3.6.

%description -n python3-configparser -l pl.UTF-8
Przestarzały moduł ConfigParser dostępny w bibliotece standardowej
Pythona 2.x został znacząco uaktualniony w Pythonie 3.2. Niniejszy
moduł zawiera backport tych zmian, aby można ich było używać
bezpośrednio w Pythonie 2.6 - 3.6.

%package apidocs
Summary:	API documentation for Python configparser module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona configparser
Group:		Documentation

%description apidocs
API documentation for Python configparser module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona configparser.

%prep
%setup -q -n configparser-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -s src
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s src
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

# https://bitbucket.org/ambv/configparser/issues/21/configparser-should-not-declare-a
# hack for: import configparser and from backports import configparser to work
ln -s ../../configparser.pyc $RPM_BUILD_ROOT%{py_sitescriptdir}/backports/configparser/
ln -s ../../configparser.pyo $RPM_BUILD_ROOT%{py_sitescriptdir}/backports/configparser/

# belongs to python-backports.spec
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/backports/__init__.py*
%endif

%if %{with python3}
%py3_install

# belongs to python-backports.spec
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/backports/__init__.py*
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/backports/__pycache__
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst configparser.rst
%{py_sitescriptdir}/backports/configparser
%{py_sitescriptdir}/configparser.py[co]
%{py_sitescriptdir}/configparser-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-configparser
%defattr(644,root,root,755)
%doc README.rst configparser.rst
%{py3_sitescriptdir}/backports/configparser
%{py3_sitescriptdir}/configparser.py
%{py3_sitescriptdir}/__pycache__/configparser.cpython-*.py[co]
%{py3_sitescriptdir}/configparser-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
