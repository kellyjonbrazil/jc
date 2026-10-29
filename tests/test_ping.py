import os
import unittest
import json
import jc.parsers.ping

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input

    # centos
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-D.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_D = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_D_p_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p-unparsable.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_p_unparsable = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-D-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_D_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_D_p_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-dup.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_dup = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-dup.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_dup = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-unparsedlines.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_unparsedlines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-missing-hostname.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_missing_hostname = f.read()

    # ubuntu 18.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O-D.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O_D = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_D_p_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-D-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_D_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_D_p_s = f.read()

    # ubuntu 22.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-dest-unreachable.out'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_dest_unreachable = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-ip-source-ip.out'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_ip_source_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-hostname-source-ip.out'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_hostname_source_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-ip-source-ip.out'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_ip_source_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-hostname-source-ip.out'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_hostname_source_ip = f.read()

    # fedora
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O.out'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O-D.out'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O_D = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O.out'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_D_p_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-p.out'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-D-p.out'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_D_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-p.out'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_D_p_s = f.read()

    # freebsd
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-p.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-s.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-p.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-s.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-p.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-s.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-p.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-s.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip.out'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip = f.read()

    # osx
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-p.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-s.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-p.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-s.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-unreachable.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_unreachable = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-unknown-errors.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_unknown_errors = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-p.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-s.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-p.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-s.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_s = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-unparsable.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_unparsable = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-dup.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_dup = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-dup.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_dup = f.read()

    # raspberry pi
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O.out'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O-D.out'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O_D = f.read()

    # alpine-linux
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-ip.out'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-hostname.out'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_hostname = f.read()

    # output

    # centos
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-D.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_D_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_D_p_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p-unparsable.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_p_unparsable_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-D-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_D_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_D_p_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-dup.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_dup_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-dup.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_dup_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-unparsedlines.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_unparsedlines_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-missing-hostname.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_missing_hostname_json = json.loads(f.read())

    # ubuntu 18.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O-D.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O_D_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_D_p_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-D-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_D_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_D_p_s_json = json.loads(f.read())

    # ubuntu 22.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-dest-unreachable.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_dest_unreachable_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-ip-source-ip.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_ip_source_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-hostname-source-ip.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_hostname_source_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-ip-source-ip.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_ip_source_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-hostname-source-ip.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_hostname_source_ip_json = json.loads(f.read())

    # fedora
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O-D.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O_D_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_D_p_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-p.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-D-p.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_D_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-p.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_D_p_s_json = json.loads(f.read())

    # freebsd
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-p.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-s.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-p.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-s.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-p.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-s.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-p.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-s.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_json = json.loads(f.read())

    # osx:
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-p.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-s.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-p.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-s.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-unreachable.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_unreachable_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-unknown-errors.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_unknown_errors_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-p.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-s.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-p.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-s.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_s_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-unparsable.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_unparsable_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-dup.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_dup_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-dup.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_dup_json = json.loads(f.read())

    # raspberry pi
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O.json'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O-D.json'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O_D_json = json.loads(f.read())

    # alpine-linux
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-ip.json'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-hostname.json'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_hostname_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-long-digits.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_long_digits = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-long-digits.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_long_digits_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-bsd-error-bare-address.out'), 'r', encoding='utf-8') as f:
        generic_ping_bsd_error_bare_address = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-bsd-error-bare-address.json'), 'r', encoding='utf-8') as f:
        generic_ping_bsd_error_bare_address_json = json.loads(f.read())
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-n-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_n_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-n-hostname.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_n_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-H-ip.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_H_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-H-ip.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_H_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-digit-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_digit_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-digit-hostname.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_digit_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-hostname-with-spaces.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_hostname_with_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-hostname-with-spaces.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_hostname_with_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-icmp-req.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_icmp_req = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-icmp-req.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_icmp_req_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-H-ip.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_H_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-H-ip.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_H_ip_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-n-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_n_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-n-hostname.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_n_hostname_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-no-time.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_no_time = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-osx-icmp-errors.out'), 'r', encoding='utf-8') as f:
        generic_ping_osx_icmp_errors = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-osx-icmp-errors.json'), 'r', encoding='utf-8') as f:
        generic_ping_osx_icmp_errors_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-hostname-from.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_hostname_from = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-hostname-from.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_hostname_from_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-hostname-from.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_hostname_from = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-hostname-from.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_hostname_from_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-icmp-errors.out'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_icmp_errors = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-icmp-errors.json'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_icmp_errors_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-error-resolved-sender.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_error_resolved_sender = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-error-resolved-sender.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_error_resolved_sender_json = json.loads(f.read())

    def test_ping_nodata(self):
        """
        Test 'ping' with no data
        """
        self.assertEqual(jc.parsers.ping.parse('', quiet=True), {})

    def test_ping_ip_O_centos_7_7(self):
        """
        Test 'ping <ip> -O' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_O, quiet=True), self.centos_7_7_ping_ip_O_json)

    def test_ping_ip_O_D_centos_7_7(self):
        """
        Test 'ping <ip> -O -D' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_O_D, quiet=True), self.centos_7_7_ping_ip_O_D_json)

    def test_ping_hostname_O_centos_7_7(self):
        """
        Test 'ping <hostname> -O' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O, quiet=True), self.centos_7_7_ping_hostname_O_json)

    def test_ping_hostname_O_p_centos_7_7(self):
        """
        Test 'ping <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O_p, quiet=True), self.centos_7_7_ping_hostname_O_p_json)

    def test_ping_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O_D_p_s, quiet=True), self.centos_7_7_ping_hostname_O_D_p_s_json)

    def test_ping6_ip_O_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_O_p, quiet=True), self.centos_7_7_ping6_ip_O_p_json)

    def test_ping6_ip_O_p_unparsable_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -p' with unparsable lines on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_O_p_unparsable, quiet=True), self.centos_7_7_ping6_ip_O_p_unparsable_json)

    def test_ping6_ip_O_D_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -D -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_O_D_p, quiet=True), self.centos_7_7_ping6_ip_O_D_p_json)

    def test_ping6_hostname_O_p_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_hostname_O_p, quiet=True), self.centos_7_7_ping6_hostname_O_p_json)

    def test_ping6_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_hostname_O_D_p_s, quiet=True), self.centos_7_7_ping6_hostname_O_D_p_s_json)

    def test_ping_ip_dup_centos_7_7(self):
        """
        Test 'ping <ip>' to broadcast IP to get duplicate replies on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_dup, quiet=True), self.centos_7_7_ping_ip_dup_json)

    def test_ping6_ip_dup_centos_7_7(self):
        """
        Test 'ping6 <ip>' to broadcast IP to get duplicate replies on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_dup, quiet=True), self.centos_7_7_ping6_ip_dup_json)

    def test_ping_ip_O_unparsedlines_centos_7_7(self):
        """
        Test 'ping <ip> -O' on Centos 7.7 with unparsable lines and error messages
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_O_unparsedlines, quiet=True), self.centos_7_7_ping_ip_O_unparsedlines_json)

    def test_ping_ip_O_ubuntu_18_4(self):
        """
        Test 'ping <ip> -O' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping_ip_O, quiet=True), self.ubuntu_18_4_ping_ip_O_json)

    def test_ping_ip_O_D_ubuntu_18_4(self):
        """
        Test 'ping <ip> -O -D' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping_ip_O_D, quiet=True), self.ubuntu_18_4_ping_ip_O_D_json)

    def test_ping_hostname_O_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping_hostname_O, quiet=True), self.ubuntu_18_4_ping_hostname_O_json)

    def test_ping_hostname_O_p_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping_hostname_O_p, quiet=True), self.ubuntu_18_4_ping_hostname_O_p_json)

    def test_ping_hostname_O_D_p_s_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O -D -p -s' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping_hostname_O_D_p_s, quiet=True), self.ubuntu_18_4_ping_hostname_O_D_p_s_json)

    def test_ping6_ip_O_p_ubuntu_18_4(self):
        """
        Test 'ping6 <ip> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping6_ip_O_p, quiet=True), self.ubuntu_18_4_ping6_ip_O_p_json)

    def test_ping6_ip_O_D_p_ubuntu_18_4(self):
        """
        Test 'ping6 <ip> -O -D -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping6_ip_O_D_p, quiet=True), self.ubuntu_18_4_ping6_ip_O_D_p_json)

    def test_ping6_hostname_O_p_ubuntu_18_4(self):
        """
        Test 'ping6 <hostname> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping6_hostname_O_p, quiet=True), self.ubuntu_18_4_ping6_hostname_O_p_json)

    def test_ping6_hostname_O_D_p_s_ubuntu_18_4(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping6_hostname_O_D_p_s, quiet=True), self.ubuntu_18_4_ping6_hostname_O_D_p_s_json)

    def test_ping_dest_unreachable_ubuntu_22_4(self):
        """
        Test 'ping' on Ubuntu 22.4 with destination unreachable message
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_22_4_ping_dest_unreachable, quiet=True), self.ubuntu_22_4_ping_dest_unreachable_json)

    def test_ping_ip_source_ip_ubuntu_22_4(self):
        """
        Test 'ping -I <source_ip> <ip>' on Ubuntu 22.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_22_4_ping_ip_source_ip, quiet=True), self.ubuntu_22_4_ping_ip_source_ip_json)

    def test_ping_hostname_source_ip_ubuntu_22_4(self):
        """
        Test 'ping -I <source_ip> <hostname>' on Ubuntu 22.4
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_22_4_ping_hostname_source_ip, quiet=True), self.ubuntu_22_4_ping_hostname_source_ip_json)

    def test_ping6_ip_source_ip_ubuntu_22_4(self):
        """
        Test 'ping6 -I <source_ip> <ip>' on Ubuntu 22.4 with source IP address
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_22_4_ping6_ip_source_ip, quiet=True), self.ubuntu_22_4_ping6_ip_source_ip_json)

    def test_ping6_hostname_source_ip_ubuntu_22_4(self):
        """
        Test 'ping6 -I <source_ip> <hostname>' on Ubuntu 22.4 with source IP address
        """
        self.assertEqual(jc.parsers.ping.parse(self.ubuntu_22_4_ping6_hostname_source_ip, quiet=True), self.ubuntu_22_4_ping6_hostname_source_ip_json)

    def test_ping_ip_O_fedora32(self):
        """
        Test 'ping <ip> -O' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping_ip_O, quiet=True), self.fedora32_ping_ip_O_json)

    def test_ping_ip_O_D_fedora32(self):
        """
        Test 'ping <ip> -O -D' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping_ip_O_D, quiet=True), self.fedora32_ping_ip_O_D_json)

    def test_ping_hostname_O_fedora32(self):
        """
        Test 'ping <hostname> -O' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping_hostname_O, quiet=True), self.fedora32_ping_hostname_O_json)

    def test_ping_hostname_O_p_fedora32(self):
        """
        Test 'ping <hostname> -O -p' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping_hostname_O_p, quiet=True), self.fedora32_ping_hostname_O_p_json)

    def test_ping_hostname_O_D_p_s_fedora32(self):
        """
        Test 'ping <hostname> -O -D -p -s' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping_hostname_O_D_p_s, quiet=True), self.fedora32_ping_hostname_O_D_p_s_json)

    def test_ping6_ip_O_p_fedora32(self):
        """
        Test 'ping6 <ip> -O -p' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping6_ip_O_p, quiet=True), self.fedora32_ping6_ip_O_p_json)

    def test_ping6_ip_O_D_p_fedora32(self):
        """
        Test 'ping6 <ip> -O -D -p' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping6_ip_O_D_p, quiet=True), self.fedora32_ping6_ip_O_D_p_json)

    def test_ping6_hostname_O_p_fedora32(self):
        """
        Test 'ping6 <hostname> -O -p' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping6_hostname_O_p, quiet=True), self.fedora32_ping6_hostname_O_p_json)

    def test_ping6_hostname_O_D_p_s_fedora32(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on fedora32
        """
        self.assertEqual(jc.parsers.ping.parse(self.fedora32_ping6_hostname_O_D_p_s, quiet=True), self.fedora32_ping6_hostname_O_D_p_s_json)

    def test_ping_hostname_p_freebsd12(self):
        """
        Test 'ping <hostname> -p' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_hostname_p, quiet=True), self.freebsd12_ping_hostname_p_json)

    def test_ping_hostname_s_freebsd12(self):
        """
        Test 'ping <hostname> -s' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_hostname_s, quiet=True), self.freebsd12_ping_hostname_s_json)

    def test_ping_ping_hostname_freebsd12(self):
        """
        Test 'ping <hostname>' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_hostname, quiet=True), self.freebsd12_ping_hostname_json)

    def test_ping_ip_p_freebsd12(self):
        """
        Test 'ping <ip> -p' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_ip_p, quiet=True), self.freebsd12_ping_ip_p_json)

    def test_ping_ip_s_freebsd12(self):
        """
        Test 'ping <ip> -s' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_ip_s, quiet=True), self.freebsd12_ping_ip_s_json)

    def test_ping_ip_freebsd12(self):
        """
        Test 'ping6 <ip>' on freebsd127
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping_ip, quiet=True), self.freebsd12_ping_ip_json)

    def test_ping6_hostname_p_freebsd12(self):
        """
        Test 'ping6 <hostname> -p' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_hostname_p, quiet=True), self.freebsd12_ping6_hostname_p_json)

    def test_ping6_hostname_s_freebsd12(self):
        """
        Test 'ping6 <hostname> -s' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_hostname_s, quiet=True), self.freebsd12_ping6_hostname_s_json)

    def test_ping6_hostname_freebsd12(self):
        """
        Test 'ping6 <hostname>' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_hostname, quiet=True), self.freebsd12_ping6_hostname_json)

    def test_ping6_ip_p_freebsd12(self):
        """
        Test 'ping6 <ip> -p' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_ip_p, quiet=True), self.freebsd12_ping6_ip_p_json)

    def test_ping6_ip_s_freebsd12(self):
        """
        Test 'ping6 <ip> -s' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_ip_s, quiet=True), self.freebsd12_ping6_ip_s_json)

    def test_ping6_ip_freebsd12(self):
        """
        Test 'ping6 <ip>' on freebsd12
        """
        self.assertEqual(jc.parsers.ping.parse(self.freebsd12_ping6_ip, quiet=True), self.freebsd12_ping6_ip_json)

    def test_ping6_ip_freebsd_new_header(self):
        """
        Test 'ping -6 <ip>' on FreeBSD 13+, which prints 'PING(' instead of 'PING6('
        """
        data = self.freebsd12_ping6_ip.replace('PING6(', 'PING(', 1)
        self.assertTrue(data.startswith('PING(56=40+8+8 bytes) '))
        self.assertEqual(jc.parsers.ping.parse(data, quiet=True), self.freebsd12_ping6_ip_json)

    def test_ping_hostname_p_osx_10_14_6(self):
        """
        Test 'ping <hostname> -p' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_hostname_p, quiet=True), self.osx_10_14_6_ping_hostname_p_json)

    def test_ping_hostname_s_osx_10_14_6(self):
        """
        Test 'ping <hostname> -s' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_hostname_s, quiet=True), self.osx_10_14_6_ping_hostname_s_json)

    def test_ping_ping_hostname_osx_10_14_6(self):
        """
        Test 'ping <hostname>' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_hostname, quiet=True), self.osx_10_14_6_ping_hostname_json)

    def test_ping_ip_p_osx_10_14_6(self):
        """
        Test 'ping <ip> -p' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip_p, quiet=True), self.osx_10_14_6_ping_ip_p_json)

    def test_ping_ip_s_osx_10_14_6(self):
        """
        Test 'ping <ip> -s' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip_s, quiet=True), self.osx_10_14_6_ping_ip_s_json)

    def test_ping_ip_osx_10_14_6(self):
        """
        Test 'ping <ip>' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip, quiet=True), self.osx_10_14_6_ping_ip_json)

    def test_ping_ip_unreachable_osx_10_14_6(self):
        """
        Test 'ping <ip>' with host unreachable error on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip_unreachable, quiet=True), self.osx_10_14_6_ping_ip_unreachable_json)

    def test_ping_ip_unknown_errors_osx_10_14_6(self):
        """
        Test 'ping <ip>' with unknown/unparsable errors on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip_unknown_errors, quiet=True), self.osx_10_14_6_ping_ip_unknown_errors_json)

    def test_ping6_hostname_p_osx_10_14_6(self):
        """
        Test 'ping6 <hostname> -p' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_hostname_p, quiet=True), self.osx_10_14_6_ping6_hostname_p_json)

    def test_ping6_hostname_s_osx_10_14_6(self):
        """
        Test 'ping6 <hostname> -s' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_hostname_s, quiet=True), self.osx_10_14_6_ping6_hostname_s_json)

    def test_ping6_hostname_osx_10_14_6(self):
        """
        Test 'ping6 <hostname>' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_hostname, quiet=True), self.osx_10_14_6_ping6_hostname_json)

    def test_ping6_ip_p_osx_10_14_6(self):
        """
        Test 'ping6 <ip> -p' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_ip_p, quiet=True), self.osx_10_14_6_ping6_ip_p_json)

    def test_ping6_ip_s_osx_10_14_6(self):
        """
        Test 'ping6 <ip> -s' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_ip_s, quiet=True), self.osx_10_14_6_ping6_ip_s_json)

    def test_ping6_ip_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_ip, quiet=True), self.osx_10_14_6_ping6_ip_json)

    def test_ping6_ip_unparsable_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' with unparsable lines on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_ip_unparsable, quiet=True), self.osx_10_14_6_ping6_ip_unparsable_json)

    def test_ping_ip_dup_osx_10_14_6(self):
        """
        Test 'ping <ip>' to broadcast IP to get duplicate replies on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_ip_dup, quiet=True), self.osx_10_14_6_ping_ip_dup_json)

    def test_ping6_ip_dup_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' to broadcast IP to get duplicate replies on osx 10.14.6
        """
        self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping6_ip_dup, quiet=True), self.osx_10_14_6_ping6_ip_dup_json)

    def test_ping_ip_O_pi(self):
        """
        Test 'ping6 <ip> -O' on raspberry pi
        """
        self.assertEqual(jc.parsers.ping.parse(self.pi_ping_ip_O, quiet=True), self.pi_ping_ip_O_json)

    def test_ping_ip_O_D_pi(self):
        """
        Test 'ping6 <ip> -O -D' on raspberry pi
        """
        self.assertEqual(jc.parsers.ping.parse(self.pi_ping_ip_O_D, quiet=True), self.pi_ping_ip_O_D_json)

    def test_ping_ip_alpine_linux(self):
        """
        Test 'ping <ip> -O' on alpine linux
        """
        self.assertEqual(jc.parsers.ping.parse(self.alpine_linux_3_13_ping_ip, quiet=True), self.alpine_linux_3_13_ping_ip_json)

    def test_ping_hostname_alpine_linux(self):
        """
        Test 'ping <hostname>' on alpine linux
        """
        self.assertEqual(jc.parsers.ping.parse(self.alpine_linux_3_13_ping_hostname, quiet=True), self.alpine_linux_3_13_ping_hostname_json)

    def test_ping_missing_hostname(self):
        """
        Test 'ping' with missing hostname on linux
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_missing_hostname, quiet=True), self.centos_7_7_ping_missing_hostname_json)

    def test_ping_linux_long_digits(self):
        """
        Test 'ping' with a long run of digits in the statistics section
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_long_digits, quiet=True), self.generic_ping_linux_long_digits_json)

    def test_ping_bsd_error_bare_address(self):
        """
        Test 'ping' on macOS/BSD with error lines where the sender is a bare address
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_bsd_error_bare_address, quiet=True), self.generic_ping_bsd_error_bare_address_json)


    def test_ping_linux_reply_n_hostname(self):
        """
        Test 'ping -n <hostname>' on linux where replies show only the address
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_reply_n_hostname, quiet=True), self.generic_ping_linux_reply_n_hostname_json)

    def test_ping_linux_reply_H_ip(self):
        """
        Test 'ping -H <ip>' on linux where replies show a resolved name
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_reply_H_ip, quiet=True), self.generic_ping_linux_reply_H_ip_json)

    def test_ping_linux_reply_digit_hostname(self):
        """
        Test 'ping -D <hostname>' on linux with a host name that starts with a digit
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_reply_digit_hostname, quiet=True), self.generic_ping_linux_reply_digit_hostname_json)

    def test_ping_linux_reply_hostname_with_spaces(self):
        """
        Test 'ping <hostname>' on linux where the resolved name contains spaces
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_reply_hostname_with_spaces, quiet=True), self.generic_ping_linux_reply_hostname_with_spaces_json)

    def test_ping_linux_reply_icmp_req(self):
        """
        Test 'ping <hostname>' on linux with old iputils 'icmp_req' reply lines
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping_linux_reply_icmp_req, quiet=True), self.generic_ping_linux_reply_icmp_req_json)

    def test_ping6_linux_reply_H_ip(self):
        """
        Test 'ping6 -H <ip>' on linux where replies show a resolved name
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping6_linux_reply_H_ip, quiet=True), self.generic_ping6_linux_reply_H_ip_json)

    def test_ping6_linux_reply_n_hostname(self):
        """
        Test 'ping6 -n -D <hostname>' on linux where replies show only the address
        """
        self.assertEqual(jc.parsers.ping.parse(self.generic_ping6_linux_reply_n_hostname, quiet=True), self.generic_ping6_linux_reply_n_hostname_json)

    def test_ping_osx_icmp_errors(self):
        """
        Test 'ping' on macOS/BSD with ICMP error messages that look like replies
        """
        result = jc.parsers.ping.parse(self.generic_ping_osx_icmp_errors, quiet=True)
        self.assertEqual(result, self.generic_ping_osx_icmp_errors_json)
        self.assertEqual(
            [(r['type'], r.get('response_ip')) for r in result['responses']],
            [
                ('frag_needed_and_df_set', '10.0.0.1'),
                ('redirect_type_of_service_and_host', '10.0.0.1'),
                ('destination_host_unreachable_for_type_of_service', '10.0.0.1'),
                ('communication_prohibited_by_filter', '10.0.0.1'),
                ('unparsable_line', None),
                ('reply', '192.0.2.10')
            ]
        )
        self.assertEqual(result['responses'][0]['len'], 1500)

    def test_ping_bsd_error_types(self):
        """
        Test 'ping' on macOS/BSD with the error messages of iputils, FreeBSD and macOS
        """
        messages = [
            ('Frag needed and DF set (mtu = 1400)', 'frag_needed_and_df_set'),
            ('frag needed and DF set (MTU 1400)', 'frag_needed_and_df_set'),
            ('Destination Net Unreachable for Type of Service', 'destination_net_unreachable_for_type_of_service'),
            ('Destination Net Unreachable', 'destination_net_unreachable'),
            ('Redirect Host(New addr: 10.0.0.254)', 'redirect_host'),
            ('Redirect Type of Service and Network(New addr: 10.0.0.254)', 'redirect_type_of_service_and_network'),
            ('Source Quench', 'source_quench'),
            ('Parameter problem: pointer = 0x14', 'parameter_problem'),
            ('Frag reassembly time exceeded', 'frag_reassembly_time_exceeded')
        ]
        for message, expected in messages:
            data = ('PING 192.0.2.10 (192.0.2.10): 56 data bytes\n'
                    '92 bytes from 10.0.0.1: ' + message + '\n'
                    'Vr HL TOS  Len   ID Flg  off TTL Pro  cks      Src      Dst\n'
                    ' 4  5  00 5400 567b   0 0000  3f  01 a024 192.168.1.221  192.0.2.10 \n'
                    '\n'
                    '--- 192.0.2.10 ping statistics ---\n'
                    '1 packets transmitted, 0 packets received, 100.0% packet loss\n')
            result = jc.parsers.ping.parse(data, quiet=True)
            self.assertEqual(result['responses'][0]['type'], expected, message)
            self.assertEqual(result['responses'][0]['response_ip'], '10.0.0.1')
            self.assertEqual(result['responses'][0]['id'], 22139)

    def test_ping6_bsd_error_not_reply(self):
        """
        Test 'ping6' on macOS/BSD with an error line that is not a reply
        """
        data = ('PING6(56=40+8+8 bytes) 2001:db8::5 --> 2001:db8::9\n'
                '72 bytes from 2001:db8::1: Destination unreachable: Address unreachable\n'
                '16 bytes from 2001:db8::9, icmp_seq=3 hlim=64 time=0.412 ms\n'
                '\n'
                '--- 2001:db8::9 ping6 statistics ---\n'
                '4 packets transmitted, 1 packets received, 75.0% packet loss\n'
                'round-trip min/avg/max/std-dev = 0.412/0.412/0.412/0.000 ms\n')
        expected = [
            {'type': 'unparsable_line', 'unparsed_line': '72 bytes from 2001:db8::1: Destination unreachable: Address unreachable'},
            {'type': 'reply', 'bytes': 16, 'response_ip': '2001:db8::9', 'icmp_seq': 3, 'ttl': 64, 'time_ms': 0.412, 'duplicate': False}
        ]
        self.assertEqual(jc.parsers.ping.parse(data, quiet=True)['responses'], expected)

    def test_ping_ip_O_pi_trailing_blank_lines(self):
        """
        Test 'ping <ip> -O' on raspberry pi (100% packet loss) with any number of trailing blank lines
        """
        for ending in ('', '\n', '\n\n', '\n\n\n\n', '\n \n'):
            result = jc.parsers.ping.parse(self.pi_ping_ip_O.rstrip() + ending, quiet=True)
            self.assertEqual(result, self.pi_ping_ip_O_json, repr(ending))
            self.assertEqual(result['packet_loss_percent'], 100.0)
            self.assertEqual(result['data_bytes'], 56)

    def test_ping_linux_reply_no_time_no_trailing_blank_line(self):
        """
        Test 'ping' on linux with replies and no rtt or trailing blank line
        """
        result = jc.parsers.ping.parse(self.generic_ping_linux_reply_no_time, quiet=True)
        self.assertEqual(result['data_bytes'], 4)
        self.assertEqual(result['duplicates'], 1)
        self.assertEqual(result['packet_loss_percent'], 0.0)
        self.assertEqual(result['time_ms'], 1001.0)
        self.assertEqual(
            result['responses'][2],
            {'type': 'reply', 'timestamp': None, 'bytes': 12, 'response_ip': '127.0.0.1', 'icmp_seq': 2, 'ttl': 64, 'time_ms': None, 'duplicate': True}
        )

    def test_ping_short_input(self):
        """
        Test 'ping' with fewer than three lines of input
        """
        self.assertEqual(jc.parsers.ping.parse('PING 192.0.2.1 (192.0.2.1): 56 data bytes\n', quiet=True),
                         {'destination_ip': '192.0.2.1', 'data_bytes': 56, 'pattern': None, 'responses': []})
        self.assertEqual(jc.parsers.ping.parse('foo', quiet=True), {'responses': []})

    def test_ping_linux_hostname_from(self):
        """
        Test 'ping <hostname>' on linux with 'from' in the host name
        """
        result = jc.parsers.ping.parse(self.generic_ping_linux_hostname_from, quiet=True)
        self.assertEqual(result, self.generic_ping_linux_hostname_from_json)
        self.assertEqual(result['data_bytes'], 56)

    def test_ping6_linux_hostname_from(self):
        """
        Test 'ping6 <hostname>' on linux with 'from' in the host name
        """
        result = jc.parsers.ping.parse(self.generic_ping6_linux_hostname_from, quiet=True)
        self.assertEqual(result, self.generic_ping6_linux_hostname_from_json)
        self.assertEqual(result['destination_ip'], '2001:db8::1')

    def test_ping_linux_header_formats(self):
        """
        Test 'ping' and 'ping6' on linux with the header line formats of old and new iputils
        """
        headers = [
            ('PING fromage.example.com (198.51.100.7) from 10.0.0.2 eth0: 56(84) bytes of data.', '198.51.100.7', 56),
            ('PING 2001:db8:53::(2001:db8:53::) 56 data bytes', '2001:db8:53::', 56),
            ('PING 2001:db8::1(2001:db8::1) from 2001:db8::2 : 56 data bytes', '2001:db8::1', 56),
            ('PING example.com(example.com (2001:db8::1)) , flow 0x00001, 56 data bytes', '2001:db8::1', 56),
            ('PING example.com (2001:db8::1) 1400 data bytes', '2001:db8::1', 1400),
            ('PING 2001:db8::1 (2001:db8::1) from 2001:db8::2 eth0: 56 data bytes', '2001:db8::1', 56)
        ]
        for header, dest, data_bytes in headers:
            data = header + '\n\n--- x ping statistics ---\n1 packets transmitted, 0 received, 100% packet loss, time 0ms\n'
            result = jc.parsers.ping.parse(data, quiet=True)
            self.assertEqual((result['destination_ip'], result['data_bytes']), (dest, data_bytes), header)

    def test_ping_bsd_source_address_header(self):
        """
        Test 'ping -S <src>' on macOS/BSD where the header shows the source address
        """
        for header in ('PING 192.0.2.10 (192.0.2.10) from 192.168.1.221: 56 data bytes',
                       'PING host.example.com (192.0.2.10) from 192.168.1.221: 1472 data bytes'):
            data = header + '\n64 bytes from 192.0.2.10: icmp_seq=0 ttl=56 time=12.345 ms\n\n--- 192.0.2.10 ping statistics ---\n1 packets transmitted, 1 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 12.345/12.345/12.345/0.000 ms\n'
            result = jc.parsers.ping.parse(data, quiet=True)
            self.assertEqual(result['destination_ip'], '192.0.2.10', header)
            self.assertEqual(result['data_bytes'], int(header.split()[-3]), header)
            self.assertEqual(result['responses'][0]['response_ip'], '192.0.2.10', header)

    def test_ping6_bsd_icmp_errors(self):
        """
        Test 'ping6' on macOS/FreeBSD with the ICMPv6 error messages of BSD ping6
        """
        result = jc.parsers.ping.parse(self.generic_ping6_bsd_icmp_errors, quiet=True)
        self.assertEqual(result, self.generic_ping6_bsd_icmp_errors_json)
        self.assertEqual([r['type'] for r in result['responses']],
                         ['no_route_to_destination', 'destination_administratively_unreachable',
                          'destination_unreachable_beyond_scope', 'packet_too_big',
                          'destination_unreachable_bad_code', 'reply'])
        self.assertEqual(result['responses'][1]['response_ip'], 'fe80::1%em0')
        self.assertEqual(result['responses'][3]['bytes'], 1280)

    def test_ping_linux_error_resolved_sender(self):
        """
        Test 'ping' on linux with error lines from a sender shown as '<name> (<ip>)' and as '<ip>'
        """
        result = jc.parsers.ping.parse(self.generic_ping_linux_error_resolved_sender, quiet=True)
        self.assertEqual(result, self.generic_ping_linux_error_resolved_sender_json)
        self.assertEqual(result['responses'][0], {'type': 'destination_host_unreachable', 'response_ip': '203.0.113.5', 'icmp_seq': 1, 'timestamp': None})
        self.assertEqual(result['responses'][2]['type'], 'reply')
        self.assertEqual(result['responses'][3]['icmp_seq'], 4)

    def test_ping_linux_error_lines(self):
        """
        Test 'ping' and 'ping6' on linux with error lines, with and without -D timestamps
        """
        footer = '\n--- x ping statistics ---\n1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms\n'
        tests = [
            ('PING 10.0.3.22 (10.0.3.22) 56(84) bytes of data.\n[1700000000.123456] From 10.0.0.1 icmp_seq=7 Destination Host Unreachable\n',
             {'type': 'destination_host_unreachable', 'response_ip': '10.0.0.1', 'icmp_seq': 7, 'timestamp': 1700000000.123456}),
            ('PING 10.0.3.22 (10.0.3.22) 56(84) bytes of data.\nFrom 10.0.0.1 icmp_seq=2 Frag needed and DF set (mtu = 1400)\n',
             {'type': 'frag_needed_and_df_set', 'response_ip': '10.0.0.1', 'icmp_seq': 2, 'timestamp': None}),
            ('PING 2001:db8::9(2001:db8::9) 56 data bytes\nFrom 2001:db8::1 icmp_seq=3 Destination unreachable: Address unreachable\n',
             {'type': 'destination_unreachable_address_unreachable', 'response_ip': '2001:db8::1', 'icmp_seq': 3, 'timestamp': None})
        ]
        for data, expected in tests:
            result = jc.parsers.ping.parse(data + footer, quiet=True)
            self.assertEqual(result['responses'], [expected], data)

    def test_ping_linux_header_only(self):
        """
        Test 'ping' and 'ping6' on linux when only the header line was printed (stopped at once)
        """
        tests = [
            ('PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.\n', '10.0.0.1', 56, []),
            ('PING ::1(::1) 56 data bytes\n', '::1', 56, []),
            ('PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.\n64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=0.040 ms\n', '10.0.0.1', 56,
             [{'type': 'reply', 'timestamp': None, 'bytes': 64, 'response_ip': '10.0.0.1', 'icmp_seq': 1, 'ttl': 64, 'time_ms': 0.04, 'duplicate': False}])
        ]
        for data, dest, data_bytes, responses in tests:
            result = jc.parsers.ping.parse(data, quiet=True)
            self.assertEqual(result, {'destination_ip': dest, 'data_bytes': data_bytes, 'pattern': None, 'responses': responses}, data)

    def test_ping_line_separators_in_line(self):
        """
        Test 'ping' with form feed and Unicode line separator characters inside a line
        """
        data = ('PING host.example.com (10.0.0.1) 56(84) bytes of data.\n'
                '64 bytes from host name (10.0.0.1): icmp_seq=1 ttl=64 time=0.040 ms\n'
                '64 bytes from host\x0cname (10.0.0.1): icmp_seq=2 ttl=64 time=0.050 ms\n'
                '\n--- host.example.com ping statistics ---\n'
                '2 packets transmitted, 2 received, 0% packet loss, time 1001ms\n'
                'rtt min/avg/max/mdev = 0.040/0.045/0.050/0.005 ms\n')
        result = jc.parsers.ping.parse(data, quiet=True)
        self.assertEqual(result['responses'], [
            {'type': 'reply', 'timestamp': None, 'bytes': 64, 'response_ip': '10.0.0.1', 'icmp_seq': 1, 'ttl': 64, 'time_ms': 0.04, 'duplicate': False},
            {'type': 'reply', 'timestamp': None, 'bytes': 64, 'response_ip': '10.0.0.1', 'icmp_seq': 2, 'ttl': 64, 'time_ms': 0.05, 'duplicate': False}
        ])
        self.assertEqual(result['packets_received'], 2)

    def test_ping_bsd_unparsable_line_text(self):
        """
        Test 'ping' and 'ping6' on macOS/BSD where unparsable lines keep their original text
        """
        tests = [
            ('PING 192.0.2.1 (192.0.2.1): 56 data bytes\n', '64 bytes from 192.0.2.1: icmp_seq=1 odd=yes: message'),
            ('PING6(56=40+8+8 bytes) 2001:db8::5 --> 2001:db8::9\n', '16 bytes from 2001:db8::9, icmp_seq=1, odd=yes')
        ]
        for header, line in tests:
            data = header + line + '\n\n--- x ping statistics ---\n1 packets transmitted, 0 packets received, 100.0% packet loss\n'
            result = jc.parsers.ping.parse(data, quiet=True)
            self.assertEqual(result['responses'], [{'type': 'unparsable_line', 'unparsed_line': line}], line)
            self.assertEqual(result['packets_transmitted'], 1)


if __name__ == '__main__':
    unittest.main()
