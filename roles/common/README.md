Common Role
------------

Common server bootstrap role

Requirements
------------

 - ansible >= 2.17
 - python >= 3.9

Tasks
--------------

| Number |     Task      |                Description                | Tests |
|:------:|:-------------:|:-----------------------------------------:|:-----:|
|   00   |    always     | Check OS and install ansible dependencies |  ---  |
|   01   |   hostname    |            Set server hostname            |       |
|   02   |     hosts     |             Manage /etc/hosts             |  ---  |
|   03   |   timezone    |            Set server timezone            |       |
|   04   | repositories  |    Add or enable/disable repositories     |       |
|   05   |   packages    |             Install packages              |       |


Role Variables
--------------

By default, role only run always tasks, other tasks skipped if no config in inventory

```yaml

# common
#   <--deep_merge-- common_defaults
#     <--deep_merge-- role.common.defaults
#       <--deep_merge-- node.common

# Role defaults for all or groups
role:
  common:
    defaults:

# Node role config
node:
  common:

    # 01 # Hostname
    # default: none
    hostname: "{{ inventory_hostname }}"

    # 02 # Hosts
    hosts:
      system:
        # default: "/etc/hosts"
        config: "/etc/hosts"
      # default merged only if
      #   role.common.defaults.hosts.data or
      #   node.common.hosts.data exist
      # default:
      #   - address: "127.0.0.1"
      #     domains: 'localhost'
      #   - address: '::1'
      #     domains:
      #      - 'ip6-localhost'
      #      - 'ip6-loopback'
      #   - address: 'fe00::0'
      #     domains: 'ip6-localnet'
      #   - address: 'ff00::0'
      #     domains: 'ip6-mcastprefix'
      #   - address: 'ff02::1'
      #     domains: 'ip6-allnodes'
      #   - address: 'ff02::2'
      #     domains: 'ip6-allrouters'
      #   - address: "127.0.0.1"
      #     domains: "{{ inventory_hostname }}"
      data:
        - address: "127.0.0.1"
          domains: "gw-1"
        - address: "192.168.0.1"
          domains:
            - "gw-1.example.com"

    # 03 # Timezone
    # default: none
    timezone: "Etc/UTC"

    # 04 # Repositories
    repositories:
      manager:
        # default: none
        apt:
          - option: "Acquire::http::proxy"
            value: "https://user:password@hostname:port"
          - option: "Acquire::https::proxy"
            value: "https://user:password@hostname:port"
          - option: "Acquire::::Proxy"
            value: "true"
          - option: "Acquire::ForceIPv4"
            value: "true"
        # default: none
        dnf:
          - option: "gpgcheck"
            value: "yes"
          - option: "installonly_limit"
            value: "3"
          - option: "clean_requirements_on_remove"
            value: "yes"
          - option: "skip_if_unavailable"
            value: "no"
      # default: none
      add:
        # Allowed keys | apt / dnf | al / co / ol / rh / rl / debian / ubuntu | al-8 / al-9 / ..
        apt:
          - name: "zabbix"
            url: "https://repo.zabbix.com/zabbix/6.4/ubuntu {{ os.codename }} main"
            gpg: "https://repo.zabbix.com/RPM-GPG-KEY-ZABBIX-08EFA7DD"
            # deb or deb-src | default deb | ignored on dnf / yum
            type: "deb"
            options:
              arch: "amd64"
        dnf:
          - name: "epel"
            url: "https://download.fedoraproject.org/pub/epel/$releasever/$basearch/"
            gpg: "https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ os.version }}"
            options:
              module_hotfixes: "1"
              skip_if_unavailable: "true"
          - name: "example"
            url: "https://example.com/...."
            options:
              gpgcheck: "0"
      # default: none
      enable:
        al-9:
          - "crb"
          - "highavailability"
          - "extras"
          - "plus"
      # default: none
      disable:
        al:
          - 'epel'

    # 05 # Packages
    packages:
      all:
        - "bind-utils"
        - "htop"
        - "mc"
        - "mlocate"
        - "nano"
        - "rsync"
        - "screen"
        - "strace"
        - "unzip"
        - "zsh"
      al:
        - "epel-release"
        - "openscap-scanner"
        - "scap-security-guide"
      co:
        - "epel-release"
      rl:
        - "epel-release"
      kvm:
        - "qemu-guest-agent"

```

Dependencies
------------

```shell
ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
```

License
-------

MIT
