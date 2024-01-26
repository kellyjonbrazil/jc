# How to use `jc` with `snap`

## How to build `snap` package

- Install `snapd`. [One](https://snapcraft.io/docs/installing-snapd) or [two](https://github.com/don-rumata/ansible-role-install-snap).

- Install `snapcraft`:

```bash
$ sudo snap install snapcraft --classic
```

- Update snapd:

```bash
$ sudo snap refresh snapcraft --edge
```

- Clone the repo:

```bash
$ git clone https://github.com/kellyjonbrazil/jc
```

- Change the directory:

```bash
$ cd ./jc
```

- Select branch:

```bash
$ git checkout snap-support
```

- Initialize LXD:

```bash
$ lxd init --auto
```

- Build `.snap` file:

```bash
$ snapcraft
```

## How to install local snap file

```bash
$ snap install --dangerous ./jc_*_amd64.snap
```

## How to use `jc` with plugins

- Put your plugin in the `"$HOME/.local/share/jc"` directory.

- To connect the directory, run:

```bash
snap connect jc:dot-jc-plugins snapd
```

## Urls

- <https://snapcraft.io/docs/supported-interfaces>

- <https://snapcraft.io/docs/interface-management>

- <https://snapcraft.io/docs/personal-files-interface>

- <https://snapcraft.io/docs/python-apps>

- <https://documentation.ubuntu.com/lxd/en/latest/getting_started/>
