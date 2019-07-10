# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define COMPONENT lcm
%define RPM_NAME caas-%{COMPONENT}
%define RPM_MAJOR_VERSION 1.0.0
%define RPM_MINOR_VERSION 7
%define IMAGE_TAG %{RPM_MAJOR_VERSION}-%{RPM_MINOR_VERSION}
%define DEPLOY_PATH %{_lcm_path}/deploy
%define SU_PATH %{_lcm_path}/su

Name:           %{RPM_NAME}
Version:        %{RPM_MAJOR_VERSION}
Release:        %{RPM_MINOR_VERSION}%{?dist}
Summary:        Containers as a Service Life Cycle Managemnet workflows
License:        %{_platform_license}
BuildArch:      x86_64
Vendor:         %{_platform_vendor}
Source0:        %{name}-%{version}.tar.gz

Requires: rsync >= 3.1.0

%description
This RPM contains Life Cycle Managemnet workflows for the CaaS subsystem.

%prep
%autosetup

%build

%install
mkdir -p %{buildroot}/%{SU_PATH}/
rsync -av su/* %{buildroot}/%{SU_PATH}/

mkdir -p %{buildroot}/%{DEPLOY_PATH}/
rsync -av deploy/* %{buildroot}/%{DEPLOY_PATH}/

mkdir -p %{buildroot}/%{_playbooks_path}/
rsync -av ansible/playbooks/pre_config_lcm.yaml %{buildroot}/%{_playbooks_path}/

mkdir -p %{buildroot}/%{_roles_path}/
rsync -av ansible/roles/pre_config_lcm %{buildroot}/%{_roles_path}/

# ------- set lcm path inside deploy
sed -i 's|{{ lcm_path }}|%{_lcm_path}|g' %{buildroot}/%{DEPLOY_PATH}/roles/bm_onboard/tasks/main.yml
sed -i 's|{{ lcm_path }}|%{_lcm_path}|g' %{buildroot}/%{DEPLOY_PATH}/roles/list_application_deployments/tasks/main.yml
sed -i 's|{{ lcm_path }}|%{_lcm_path}|g' %{buildroot}/%{DEPLOY_PATH}/roles/list_application_packages/tasks/main.yml
sed -i 's|{{ lcm_path }}|%{_lcm_path}|g' %{buildroot}/%{DEPLOY_PATH}/roles/list_docker_images/tasks/main.yml
sed -i 's|{{ caas_manifest_path }}|%{_caas_manifest_path}|g' %{buildroot}/%{DEPLOY_PATH}/group_vars/controller-1.caas_master/params.yml
# ------- set lcm path inside roles
sed -i 's|{{ lcm_path }}|%{_lcm_path}|g' %{buildroot}/%{_roles_path}/pre_config_lcm/tasks/main.yml
# -------

%files
%{SU_PATH}
%{DEPLOY_PATH}
%{_playbooks_path}/pre_config_lcm.yaml
%{_roles_path}/pre_config_lcm

%preun

%post
mkdir -p %{_postconfig_path}/
ln -sf %{_playbooks_path}/pre_config_lcm.yaml %{_postconfig_path}/

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_postconfig_path}/pre_config_lcm.yaml
fi

%clean
rm -rf ${buildroot}

