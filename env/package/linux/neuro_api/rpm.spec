%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

%if 0%{?ci_build:1}
    %global _topdir %(pwd)/rpmbuild
    %global _builddir .
    %global _sourcedir %{_builddir}
%endif


# ci_build only
%global package_version__major 1.0
#
%global release_version__major 1.0


%{!?package_version: %global package_version %{nil}}

%if 0%{?ci_build:1}
    %if "%{package_version}" == ""
        %global package_version %{getenv:CI_BUILD_TAG}
    %endif
    %if "%{package_version}" == ""
        %global package_version %{package_version__major}.%{getenv:CI_BUILD_ID}
    %endif
%endif


Name:           acme-neuro-api
Version:        %{package_version}
Release:        %{release_version__major}%{?dist}
Summary:        ACME Neuro API

Group:          Development/Languages
License:        (c) Ilya Nadelyaev
URL:            https://github.com/ilyanadelyaev/acme
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       uwsgi
Requires:       uwsgi-logger-syslog
Requires:       uwsgi-plugin-python

Requires:       python-flask >= 0.10.1
Requires:       python-blinker

Requires:       python-pymongo >= 3.3.0

Requires:       python-requests = 2.10.0
Requires:       python-urllib3

Requires:       python-configure = 0.5
Requires:       python-validate_email = 1.3

# consul
Requires:       python-raven


%systemd_requires


%description

%{summary}


%prep

%if 0%{?ci_build:1}
    %{__mkdir_p} %{_topdir}/{RPMS,SRPMS}
%endif

%{__cp} env/package/egg/neuro_api/{MANIFEST.in,setup.py} .


%build

%{__python} setup.py build


%install

%{__python} setup.py install --skip-build --root %{buildroot}

%{__mkdir_p} %{buildroot}%{_localstatedir}/log/acme/neuro_api
%{__mkdir_p} %{buildroot}%{_sysconfdir}/acme/neuro_api
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_rundir}/acme/neuro_api

%{__install} -D env/package/linux/neuro_api/files/service %{buildroot}%{_unitdir}/acme-neuro-api.service
%{__install} -D env/package/linux/neuro_api/files/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/acme-neuro-api
%{__install} -D env/package/linux/neuro_api/files/tmpfiles %{buildroot}%{_sysconfdir}/tmpfiles.d/acme-neuro-api.conf

%{__install} -D env/config/neuro_api/config.yml %{buildroot}%{_sysconfdir}/acme/neuro_api/config.yml

%{__sed} 's|__PYTHON_SITE_LIB__|%{python_sitelib}|' \
    env/package/linux/neuro_api/files/sysconfig.in > \
    %{buildroot}%{_sysconfdir}/sysconfig/acme-neuro-api

%{__sed} 's|__PYTHON_SITE_LIB__|%{python_sitelib}|' \
    env/package/linux/neuro_api/files/uwsgi.ini.in > \
    %{buildroot}%{_sysconfdir}/acme/neuro_api/uwsgi.ini

%{__rm} -rf %{buildroot}/usr/local


%files

%defattr(644,root,root,755)

%{_sysconfdir}/sysconfig/acme-neuro-api
%{_sysconfdir}/acme/neuro_api/uwsgi.ini
%{_sysconfdir}/acme/neuro_api/config.yml

%{python_sitelib}/acme/*
%{python_sitelib}/acme_neuro_api*.egg-info
%{_unitdir}/acme-neuro-api.service

%{_sysconfdir}/logrotate.d/acme-neuro-api
%{_sysconfdir}/tmpfiles.d/acme-neuro-api.conf

%dir %{_localstatedir}/log/acme/neuro_api
%dir %{_rundir}/acme/neuro_api


%post

if [ "$1" = "1" ]; then
    # Post install
    # - create user
    getent passwd neuro-api >/dev/null || \
        useradd -r -M -c "ACME Neuro API" neuro-api || :
    # enable services
    systemctl enable --now acme-neuro-api.service
fi

%tmpfiles_create acme-neuro-api.conf

%{__chown} neuro-api:neuro-api %{_localstatedir}/log/acme/neuro_api
%{__chown} neuro-api:neuro-api %{_rundir}/acme/neuro_api
#
%{__chown} root:neuro-api %{_sysconfdir}/acme/neuro_api/config.yml

%systemd_post acme-neuro-api.service


%preun

%systemd_preun acme-neuro-api.service

if [ "$1" = "0" ]; then
    # Pre un-install
    # - delete user
    userdel neuro-api >/dev/null || :
fi


%postun

%systemd_postun_with_restart acme-neuro-api.service
