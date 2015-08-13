
Name: gratia-xdmod
Summary: A converter script from a Gratia database into XDMoD
Version: 0.1
License: ASL 2.0
Release: 1%{?dist}
Group: System Environment/Libraries

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0: %{name}-%{version}.tar.gz

%description
%{summary}

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

# Ghost files for the RPM.

mkdir -p $RPM_BUILD_ROOT/%_localstatedir/lock/
touch $RPM_BUILD_ROOT/%_localstatedir/lock/gratia-xdmod.lock

%clean
rm -rf $RPM_BUILD_ROOT

%pre

getent group xdmod >/dev/null || groupadd -r xdmod
getent passwd xdmod >/dev/null || \
    useradd -r -g xdmod -d /var/lib/gratia-xdmod -s /sbin/nologin \
    -c "User for running xdmod" xdmod
exit 0

%files -f INSTALLED_FILES
%defattr(-,root,root)
%config(noreplace) %_sysconfdir/gratia-xdmod.cfg
%ghost %_localstatedir/lock/gratia-xdmod.lock

%changelog
* Thu Aug 06 2015 Mats Rynge <rynge@isi.edu> - 0.1-1
- Initial packaging 

