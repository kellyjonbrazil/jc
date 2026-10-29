import os
import unittest
import json
from jc.exceptions import ParseError
import jc.parsers.ping_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat ping.out | jc --ping-s | jello -c > ping-streaming.json


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

    # output

    # centos
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-streaming-ignore-exceptions.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_streaming_ignore_exceptions_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-D-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_O_D_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-D-p-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_O_D_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-dup-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_ip_dup_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-dup-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping6_ip_dup_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-missing-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ping_missing_hostname_json = json.loads(f.read())

    # ubuntu 18.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-ip-O-D-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_ip_O_D_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-ip-O-D-p-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_ip_O_D_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping6-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ping6_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    # ubuntu 22.4
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-dest-unreachable-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_dest_unreachable_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-hostname-source-ip-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_hostname_I_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping-ip-source-ip-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping_ip_I_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-ip-source-ip-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_ip_I_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-22.04/ping6-hostname-source-ip-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_22_4_ping6_hostname_I_streaming_json = json.loads(f.read())

    # fedora
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-ip-O-D-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_ip_O_D_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-ip-O-D-p-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_ip_O_D_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-p-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/ping6-hostname-O-D-p-s-streaming.json'), 'r', encoding='utf-8') as f:
        fedora32_ping6_hostname_O_D_p_s_streaming_json = json.loads(f.read())

    # freebsd
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-p-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-s-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-p-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-s-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-ip-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-p-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-s-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-p-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-s-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping6-ip-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_ping6_ip_streaming_json = json.loads(f.read())

    # osx:
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-p-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-s-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-p-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-s-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-unreachable-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_unreachable_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-p-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-s-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-p-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_p_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-s-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_s_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-ip-dup-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping_ip_dup_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping6-ip-dup-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ping6_ip_dup_streaming_json = json.loads(f.read())

    # raspberry pi
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O-streaming.json'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/pi/ping-ip-O-D-streaming.json'), 'r', encoding='utf-8') as f:
        pi_ping_ip_O_D_streaming_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-long-digits.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_long_digits = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-long-digits-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_long_digits_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-error-resolved-sender.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_error_resolved_sender = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-error-resolved-sender-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_error_resolved_sender_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-bsd-error-bare-address.out'), 'r', encoding='utf-8') as f:
        generic_ping_bsd_error_bare_address = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-bsd-error-bare-address-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_bsd_error_bare_address_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-error-bare-address.out'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_error_bare_address = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-error-bare-address-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_error_bare_address_streaming_json = json.loads(f.read())
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-n-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_n_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-n-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_n_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-H-ip.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_H_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-H-ip-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_H_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-digit-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_digit_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-digit-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_digit_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-hostname-with-spaces.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_hostname_with_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-hostname-with-spaces-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_hostname_with_spaces_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-icmp-req.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_icmp_req = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-icmp-req-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_icmp_req_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-H-ip.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_H_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-H-ip-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_H_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-n-hostname.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_n_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-reply-n-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_reply_n_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-no-time.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_no_time = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-reply-no-time-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_reply_no_time_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-osx-icmp-errors.out'), 'r', encoding='utf-8') as f:
        generic_ping_osx_icmp_errors = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-osx-icmp-errors-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_osx_icmp_errors_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-ip.out'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_ip = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-ip-streaming.json'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_ip_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-hostname.out'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_hostname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/alpine-linux-3.13/ping-hostname-streaming.json'), 'r', encoding='utf-8') as f:
        alpine_linux_3_13_ping_hostname_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-hostname-from.out'), 'r', encoding='utf-8') as f:
        generic_ping_linux_hostname_from = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping-linux-hostname-from-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping_linux_hostname_from_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-hostname-from.out'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_hostname_from = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-linux-hostname-from-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping6_linux_hostname_from_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-icmp-errors.out'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_icmp_errors = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ping6-bsd-icmp-errors-streaming.json'), 'r', encoding='utf-8') as f:
        generic_ping6_bsd_icmp_errors_streaming_json = json.loads(f.read())

    def test_ping_s_nodata(self):
        """
        Test 'ping' with no data
        """
        self.assertEqual(list(jc.parsers.ping_s.parse([], quiet=True)), [])

    def test_ping_s_unparsable(self):
        data = 'unparsable data'
        g = jc.parsers.ping_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_ping_s_ignore_exceptions_success(self):
        """
        Test 'ping' with -qq (ignore_exceptions) option
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_ip_O.splitlines(), quiet=True, ignore_exceptions=True)), self.centos_7_7_ping_ip_O_streaming_ignore_exceptions_json)

    def test_ping_s_ignore_exceptions_error(self):
        """
        Test 'ping' with -qq (ignore_exceptions) option option and error
        """
        data_in = 'not ping'
        expected = json.loads('[{"_jc_meta":{"success":false,"error":"ParseError: Could not detect ping OS","line":"not ping"}}]')
        self.assertEqual(list(jc.parsers.ping_s.parse(data_in.splitlines(), quiet=True, ignore_exceptions=True)), expected)

    def test_ping_s_ip_O_centos_7_7(self):
        """
        Test 'ping <ip> -O' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_ip_O.splitlines(), quiet=True)), self.centos_7_7_ping_ip_O_streaming_json)

    def test_ping_s_ip_O_D_centos_7_7(self):
        """
        Test 'ping <ip> -O -D' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_ip_O_D.splitlines(), quiet=True)), self.centos_7_7_ping_ip_O_D_streaming_json)

    def test_ping_s_hostname_O_centos_7_7(self):
        """
        Test 'ping <hostname> -O' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_hostname_O.splitlines(), quiet=True)), self.centos_7_7_ping_hostname_O_streaming_json)

    def test_ping_s_hostname_O_p_centos_7_7(self):
        """
        Test 'ping <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_hostname_O_p.splitlines(), quiet=True)), self.centos_7_7_ping_hostname_O_p_streaming_json)

    def test_ping_s_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_hostname_O_D_p_s.splitlines(), quiet=True)), self.centos_7_7_ping_hostname_O_D_p_s_streaming_json)

    def test_ping6_s_ip_O_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -p' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping6_ip_O_p.splitlines(), quiet=True)), self.centos_7_7_ping6_ip_O_p_streaming_json)

    def test_ping6_s_ip_O_p_unparsable_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -p' with unparsable lines on Centos 7.7 (raises IndexError)
        """
        g = jc.parsers.ping_s.parse(self.centos_7_7_ping6_ip_O_p_unparsable.splitlines(), quiet=True)
        with self.assertRaises(IndexError):
            list(g)

    def test_ping6_s_ip_O_D_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -D -p' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping6_ip_O_D_p.splitlines(), quiet=True)), self.centos_7_7_ping6_ip_O_D_p_streaming_json)

    def test_ping6_s_hostname_O_p_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping6_hostname_O_p.splitlines(), quiet=True)), self.centos_7_7_ping6_hostname_O_p_streaming_json)

    def test_ping6_s_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping6_hostname_O_D_p_s.splitlines(), quiet=True)), self.centos_7_7_ping6_hostname_O_D_p_s_streaming_json)

    def test_ping_s_ip_dup_centos_7_7(self):
        """
        Test 'ping <ip>' to broadcast IP to get duplicate replies on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_ip_dup.splitlines(), quiet=True)), self.centos_7_7_ping_ip_dup_streaming_json)

    def test_ping6_s_ip_dup_centos_7_7(self):
        """
        Test 'ping6 <ip>' to broadcast IP to get duplicate replies on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping6_ip_dup.splitlines(), quiet=True)), self.centos_7_7_ping6_ip_dup_streaming_json)

    def test_ping_s_ip_O_unparsedlines_centos_7_7(self):
        """
        Test 'ping <ip> -O' on Centos 7.7 with unparsable lines and error messages
        """
        g = jc.parsers.ping_s.parse(self.centos_7_7_ping_ip_O_unparsedlines.splitlines(), quiet=True)
        with self.assertRaises(IndexError):
            list(g)

    def test_ping_s_ip_O_ubuntu_18_4(self):
        """
        Test 'ping <ip> -O' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping_ip_O.splitlines(), quiet=True)), self.ubuntu_18_4_ping_ip_O_streaming_json)

    def test_ping_s_ip_O_D_ubuntu_18_4(self):
        """
        Test 'ping <ip> -O -D' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping_ip_O_D.splitlines(), quiet=True)), self.ubuntu_18_4_ping_ip_O_D_streaming_json)

    def test_ping_s_hostname_O_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping_hostname_O.splitlines(), quiet=True)), self.ubuntu_18_4_ping_hostname_O_streaming_json)

    def test_ping_s_hostname_O_p_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping_hostname_O_p.splitlines(), quiet=True)), self.ubuntu_18_4_ping_hostname_O_p_streaming_json)

    def test_ping_s_hostname_O_D_p_s_ubuntu_18_4(self):
        """
        Test 'ping <hostname> -O -D -p -s' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping_hostname_O_D_p_s.splitlines(), quiet=True)), self.ubuntu_18_4_ping_hostname_O_D_p_s_streaming_json)

    def test_ping6_s_ip_O_p_ubuntu_18_4(self):
        """
        Test 'ping6 <ip> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping6_ip_O_p.splitlines(), quiet=True)), self.ubuntu_18_4_ping6_ip_O_p_streaming_json)

    def test_ping6_s_ip_O_D_p_ubuntu_18_4(self):
        """
        Test 'ping6 <ip> -O -D -p' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping6_ip_O_D_p.splitlines(), quiet=True)), self.ubuntu_18_4_ping6_ip_O_D_p_streaming_json)

    def test_ping6_s_hostname_O_p_ubuntu_18_4(self):
        """
        Test 'ping6 <hostname> -O -p' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping6_hostname_O_p.splitlines(), quiet=True)), self.ubuntu_18_4_ping6_hostname_O_p_streaming_json)

    def test_ping6_s_hostname_O_D_p_s_ubuntu_18_4(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_18_4_ping6_hostname_O_D_p_s.splitlines(), quiet=True)), self.ubuntu_18_4_ping6_hostname_O_D_p_s_streaming_json)

    def test_ping_s_dest_unreachable_ubuntu_22_4(self):
        """
        Test 'ping' on Ubuntu 22.4 with destination unreachable message
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_22_4_ping_dest_unreachable.splitlines(), quiet=True)), self.ubuntu_22_4_ping_dest_unreachable_streaming_json)


    def test_ping_s_hostname_I_ubuntu_22_4(self):
        """
        Test 'ping <hostname> -I' on ubuntu 22.04
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_22_4_ping_hostname_source_ip.splitlines(), quiet=True)), self.ubuntu_22_4_ping_hostname_I_streaming_json)

    def test_ping_s_ip_I_ubuntu_22_4(self):
        """
        Test 'ping <ip> -I' on ubuntu 22.04
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_22_4_ping_ip_source_ip.splitlines(), quiet=True)), self.ubuntu_22_4_ping_ip_I_streaming_json)

    def test_ping6_s_ip_I_ubuntu_22_4(self):
        """
        Test 'ping6 <ip> -I' on ubuntu 22.04
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_22_4_ping6_ip_source_ip.splitlines(), quiet=True)), self.ubuntu_22_4_ping6_ip_I_streaming_json)

    def test_ping6_s_hostname_I_ubuntu_22_4(self):
        """
        Test 'ping6 <hostname> -I' on ubuntu 22.04
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.ubuntu_22_4_ping6_hostname_source_ip.splitlines(), quiet=True)), self.ubuntu_22_4_ping6_hostname_I_streaming_json)


    def test_ping_s_ip_O_fedora32(self):
        """
        Test 'ping <ip> -O' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping_ip_O.splitlines(), quiet=True)), self.fedora32_ping_ip_O_streaming_json)

    def test_ping_s_ip_O_D_fedora32(self):
        """
        Test 'ping <ip> -O -D' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping_ip_O_D.splitlines(), quiet=True)), self.fedora32_ping_ip_O_D_streaming_json)

    def test_ping_s_hostname_O_fedora32(self):
        """
        Test 'ping <hostname> -O' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping_hostname_O.splitlines(), quiet=True)), self.fedora32_ping_hostname_O_streaming_json)

    def test_ping_s_hostname_O_p_fedora32(self):
        """
        Test 'ping <hostname> -O -p' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping_hostname_O_p.splitlines(), quiet=True)), self.fedora32_ping_hostname_O_p_streaming_json)

    def test_ping_s_hostname_O_D_p_s_fedora32(self):
        """
        Test 'ping <hostname> -O -D -p -s' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping_hostname_O_D_p_s.splitlines(), quiet=True)), self.fedora32_ping_hostname_O_D_p_s_streaming_json)

    def test_ping6_s_ip_O_p_fedora32(self):
        """
        Test 'ping6 <ip> -O -p' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping6_ip_O_p.splitlines(), quiet=True)), self.fedora32_ping6_ip_O_p_streaming_json)

    def test_ping6_s_ip_O_D_p_fedora32(self):
        """
        Test 'ping6 <ip> -O -D -p' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping6_ip_O_D_p.splitlines(), quiet=True)), self.fedora32_ping6_ip_O_D_p_streaming_json)

    def test_ping6_s_hostname_O_p_fedora32(self):
        """
        Test 'ping6 <hostname> -O -p' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping6_hostname_O_p.splitlines(), quiet=True)), self.fedora32_ping6_hostname_O_p_streaming_json)

    def test_ping6_s_hostname_O_D_p_s_fedora32(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on fedora32
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.fedora32_ping6_hostname_O_D_p_s.splitlines(), quiet=True)), self.fedora32_ping6_hostname_O_D_p_s_streaming_json)

    def test_ping_s_hostname_p_freebsd12(self):
        """
        Test 'ping <hostname> -p' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_hostname_p.splitlines(), quiet=True)), self.freebsd12_ping_hostname_p_streaming_json)

    def test_ping_s_hostname_s_freebsd12(self):
        """
        Test 'ping <hostname> -s' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_hostname_s.splitlines(), quiet=True)), self.freebsd12_ping_hostname_s_streaming_json)

    def test_ping_s_ping_hostname_freebsd12(self):
        """
        Test 'ping <hostname>' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_hostname.splitlines(), quiet=True)), self.freebsd12_ping_hostname_streaming_json)

    def test_ping_s_ip_p_freebsd12(self):
        """
        Test 'ping <ip> -p' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_ip_p.splitlines(), quiet=True)), self.freebsd12_ping_ip_p_streaming_json)

    def test_ping_s_ip_s_freebsd12(self):
        """
        Test 'ping <ip> -s' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_ip_s.splitlines(), quiet=True)), self.freebsd12_ping_ip_s_streaming_json)

    def test_ping_s_ip_freebsd12(self):
        """
        Test 'ping6 <ip>' on freebsd127
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping_ip.splitlines(), quiet=True)), self.freebsd12_ping_ip_streaming_json)

    def test_ping6_s_hostname_p_freebsd12(self):
        """
        Test 'ping6 <hostname> -p' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_hostname_p.splitlines(), quiet=True)), self.freebsd12_ping6_hostname_p_streaming_json)

    def test_ping6_s_hostname_s_freebsd12(self):
        """
        Test 'ping6 <hostname> -s' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_hostname_s.splitlines(), quiet=True)), self.freebsd12_ping6_hostname_s_streaming_json)

    def test_ping6_s_hostname_freebsd12(self):
        """
        Test 'ping6 <hostname>' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_hostname.splitlines(), quiet=True)), self.freebsd12_ping6_hostname_streaming_json)

    def test_ping6_s_ip_p_freebsd12(self):
        """
        Test 'ping6 <ip> -p' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_ip_p.splitlines(), quiet=True)), self.freebsd12_ping6_ip_p_streaming_json)

    def test_ping6_s_ip_s_freebsd12(self):
        """
        Test 'ping6 <ip> -s' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_ip_s.splitlines(), quiet=True)), self.freebsd12_ping6_ip_s_streaming_json)

    def test_ping6_s_ip_freebsd12(self):
        """
        Test 'ping6 <ip>' on freebsd12
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.freebsd12_ping6_ip.splitlines(), quiet=True)), self.freebsd12_ping6_ip_streaming_json)

    def test_ping6_s_ip_freebsd_new_header(self):
        """
        Test 'ping -6 <ip>' on FreeBSD 13+, which prints 'PING(' instead of 'PING6('
        """
        data = self.freebsd12_ping6_ip.replace('PING6(', 'PING(', 1)
        self.assertTrue(data.startswith('PING(56=40+8+8 bytes) '))
        self.assertEqual(list(jc.parsers.ping_s.parse(data.splitlines(), quiet=True)), self.freebsd12_ping6_ip_streaming_json)

    def test_ping_s_hostname_p_osx_10_14_6(self):
        """
        Test 'ping <hostname> -p' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_hostname_p.splitlines(), quiet=True)), self.osx_10_14_6_ping_hostname_p_streaming_json)

    def test_ping_s_hostname_s_osx_10_14_6(self):
        """
        Test 'ping <hostname> -s' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_hostname_s.splitlines(), quiet=True)), self.osx_10_14_6_ping_hostname_s_streaming_json)

    def test_ping_s_hostname_osx_10_14_6(self):
        """
        Test 'ping <hostname>' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_hostname.splitlines(), quiet=True)), self.osx_10_14_6_ping_hostname_streaming_json)

    def test_ping_s_ip_p_osx_10_14_6(self):
        """
        Test 'ping <ip> -p' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip_p.splitlines(), quiet=True)), self.osx_10_14_6_ping_ip_p_streaming_json)

    def test_ping_s_ip_s_osx_10_14_6(self):
        """
        Test 'ping <ip> -s' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip_s.splitlines(), quiet=True)), self.osx_10_14_6_ping_ip_s_streaming_json)

    def test_ping_s_ip_osx_10_14_6(self):
        """
        Test 'ping <ip>' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip.splitlines(), quiet=True)), self.osx_10_14_6_ping_ip_streaming_json)

    def test_ping_s_ip_unreachable_osx_10_14_6(self):
        """
        Test 'ping <ip>' with host unreachable error on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip_unreachable.splitlines(), quiet=True)), self.osx_10_14_6_ping_ip_unreachable_streaming_json)

    def test_ping_s_ip_unknown_errors_osx_10_14_6(self):
        """
        Test 'ping <ip>' with unknown/unparsable errors on osx 10.14.6
        """
        g = jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip_unknown_errors.splitlines(), quiet=True)
        with self.assertRaises(IndexError):
            list(g)

    def test_ping6_s_hostname_p_osx_10_14_6(self):
        """
        Test 'ping6 <hostname> -p' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_hostname_p.splitlines(), quiet=True)), self.osx_10_14_6_ping6_hostname_p_streaming_json)

    def test_ping6_s_hostname_s_osx_10_14_6(self):
        """
        Test 'ping6 <hostname> -s' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_hostname_s.splitlines(), quiet=True)), self.osx_10_14_6_ping6_hostname_s_streaming_json)

    def test_ping6_s_hostname_osx_10_14_6(self):
        """
        Test 'ping6 <hostname>' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_hostname.splitlines(), quiet=True)), self.osx_10_14_6_ping6_hostname_streaming_json)

    def test_ping6_s_ip_p_osx_10_14_6(self):
        """
        Test 'ping6 <ip> -p' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_ip_p.splitlines(), quiet=True)), self.osx_10_14_6_ping6_ip_p_streaming_json)

    def test_ping6_s_ip_s_osx_10_14_6(self):
        """
        Test 'ping6 <ip> -s' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_ip_s.splitlines(), quiet=True)), self.osx_10_14_6_ping6_ip_s_streaming_json)

    def test_ping6_s_ip_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_ip.splitlines(), quiet=True)), self.osx_10_14_6_ping6_ip_streaming_json)

    def test_ping6_s_ip_unparsable_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' with unparsable lines on osx 10.14.6
        """
        g = jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_ip_unparsable.splitlines(), quiet=True)
        with self.assertRaises(IndexError):
            list(g)

    def test_ping_s_ip_dup_osx_10_14_6(self):
        """
        Test 'ping <ip>' to broadcast IP to get duplicate replies on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping_ip_dup.splitlines(), quiet=True)), self.osx_10_14_6_ping_ip_dup_streaming_json)

    def test_ping6_s_ip_dup_osx_10_14_6(self):
        """
        Test 'ping6 <ip>' to broadcast IP to get duplicate replies on osx 10.14.6
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.osx_10_14_6_ping6_ip_dup.splitlines(), quiet=True)), self.osx_10_14_6_ping6_ip_dup_streaming_json)

    def test_ping_s_ip_O_pi(self):
        """
        Test 'ping6 <ip> -O' on raspberry pi
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.pi_ping_ip_O.splitlines(), quiet=True)), self.pi_ping_ip_O_streaming_json)

    def test_ping_s_ip_O_D_pi(self):
        """
        Test 'ping6 <ip> -O -D' on raspberry pi
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.pi_ping_ip_O_D.splitlines(), quiet=True)), self.pi_ping_ip_O_D_streaming_json)

    def test_ping_s_missing_hostname(self):
        """
        Test 'ping' with missing hostname on linux
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.centos_7_7_ping_missing_hostname.splitlines(), quiet=True)), self.centos_7_7_ping_missing_hostname_json)

    def test_ping_s_linux_long_digits(self):
        """
        Test 'ping' with a long run of digits in the statistics section
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_long_digits.splitlines(), quiet=True)), self.generic_ping_linux_long_digits_streaming_json)

    def test_ping_s_linux_error_resolved_sender(self):
        """
        Test 'ping' error lines where the sender was resolved to a name
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_error_resolved_sender.splitlines(), quiet=True)), self.generic_ping_linux_error_resolved_sender_streaming_json)

    def test_ping_s_bsd_error_bare_address(self):
        """
        Test 'ping' on macOS/BSD with error lines where the sender is a bare address
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_bsd_error_bare_address.splitlines(), quiet=True)), self.generic_ping_bsd_error_bare_address_streaming_json)

    def test_ping6_s_bsd_error_bare_address(self):
        """
        Test 'ping6' on macOS/BSD with error lines where the sender is a bare address
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping6_bsd_error_bare_address.splitlines(), quiet=True)), self.generic_ping6_bsd_error_bare_address_streaming_json)


    def test_ping_s_linux_reply_n_hostname(self):
        """
        Test 'ping -n <hostname>' on linux where replies show only the address
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_n_hostname.splitlines(), quiet=True)), self.generic_ping_linux_reply_n_hostname_streaming_json)

    def test_ping_s_linux_reply_H_ip(self):
        """
        Test 'ping -H <ip>' on linux where replies show a resolved name
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_H_ip.splitlines(), quiet=True)), self.generic_ping_linux_reply_H_ip_streaming_json)

    def test_ping_s_linux_reply_digit_hostname(self):
        """
        Test 'ping -D <hostname>' on linux with a host name that starts with a digit
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_digit_hostname.splitlines(), quiet=True)), self.generic_ping_linux_reply_digit_hostname_streaming_json)

    def test_ping_s_linux_reply_hostname_with_spaces(self):
        """
        Test 'ping <hostname>' on linux where the resolved name contains spaces
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_hostname_with_spaces.splitlines(), quiet=True)), self.generic_ping_linux_reply_hostname_with_spaces_streaming_json)

    def test_ping_s_linux_reply_icmp_req(self):
        """
        Test 'ping <hostname>' on linux with old iputils 'icmp_req' reply lines
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_icmp_req.splitlines(), quiet=True)), self.generic_ping_linux_reply_icmp_req_streaming_json)

    def test_ping6_s_linux_reply_H_ip(self):
        """
        Test 'ping6 -H <ip>' on linux where replies show a resolved name
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping6_linux_reply_H_ip.splitlines(), quiet=True)), self.generic_ping6_linux_reply_H_ip_streaming_json)

    def test_ping6_s_linux_reply_n_hostname(self):
        """
        Test 'ping6 -n -D <hostname>' on linux where replies show only the address
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping6_linux_reply_n_hostname.splitlines(), quiet=True)), self.generic_ping6_linux_reply_n_hostname_streaming_json)

    def test_ping_s_linux_reply_no_time(self):
        """
        Test 'ping -s 4 <ip>' on linux with reply lines that have no time field
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.generic_ping_linux_reply_no_time.splitlines(), quiet=True)), self.generic_ping_linux_reply_no_time_streaming_json)

    def test_ping_s_osx_icmp_errors(self):
        """
        Test 'ping' on macOS/BSD with ICMP error messages that look like replies
        """
        result = list(jc.parsers.ping_s.parse(self.generic_ping_osx_icmp_errors.splitlines(), quiet=True, ignore_exceptions=True))
        self.assertEqual(result, self.generic_ping_osx_icmp_errors_streaming_json)
        self.assertEqual(
            [r.get('type') for r in result],
            [
                'frag_needed_and_df_set',
                'redirect_type_of_service_and_host',
                'destination_host_unreachable_for_type_of_service',
                'communication_prohibited_by_filter',
                None,
                'reply',
                'summary'
            ]
        )
        self.assertFalse(result[4]['_jc_meta']['success'])
        self.assertEqual(result[0]['response_ip'], '10.0.0.1')

    def test_ping_s_osx_long_unknown_error(self):
        """
        Test 'ping' on macOS/BSD with an unknown error message as long as a reply line
        """
        data = [
            'PING 192.0.2.10 (192.0.2.10): 56 data bytes',
            '36 bytes from 10.0.0.1: an error message that is long enough to look like a reply'
        ]
        self.assertRaises(IndexError, list, jc.parsers.ping_s.parse(data, quiet=True))

    def test_ping_s_error_types(self):
        """
        Test 'ping' with error messages of iputils, FreeBSD and macOS
        """
        messages = [
            ('Frag needed and DF set (mtu = 1400)', 'frag_needed_and_df_set'),
            ('frag needed and DF set (MTU 1400)', 'frag_needed_and_df_set'),
            ('Destination Host Unreachable for Type of Service', 'destination_host_unreachable_for_type_of_service'),
            ('Destination Host Unreachable', 'destination_host_unreachable'),
            ('Redirect Type of Service and Host(New addr: 10.0.0.254)', 'redirect_type_of_service_and_host'),
            ('Source Quench', 'source_quench'),
            ('Parameter problem: pointer = 0x14', 'parameter_problem')
        ]
        for message, expected in messages:
            data = [
                'PING 192.0.2.10 (192.0.2.10): 56 data bytes',
                '92 bytes from 10.0.0.1: ' + message
            ]
            result = list(jc.parsers.ping_s.parse(data, quiet=True))
            self.assertEqual(result[0]['type'], expected, message)
            self.assertEqual(result[0]['response_ip'], '10.0.0.1')

    def test_ping6_s_linux_error_types(self):
        """
        Test 'ping6' on linux with the IPv6 error messages of iputils
        """
        messages = [
            ('Time exceeded: Defragmentation failure', 'time_exceeded_fragment_reassembly_time_exceeded'),
            ('Time exceeded: Hop limit', 'time_exceeded_hop_limit'),
            ('Destination unreachable: Address unreachable', 'destination_unreachable_address_unreachable'),
            ('Packet too big: mtu=1280', 'packet_too_big'),
            ('Parameter problem: Wrong header field 40', 'parameter_problem')
        ]
        for message, expected in messages:
            data = [
                'PING 2001:db8::1(2001:db8::1) 56 data bytes',
                'From 2001:db8::fe icmp_seq=1 ' + message
            ]
            result = list(jc.parsers.ping_s.parse(data, quiet=True))
            self.assertEqual(result[0]['type'], expected, message)
            self.assertEqual(result[0]['response_ip'], '2001:db8::fe')
            self.assertEqual(result[0]['icmp_seq'], 1)

    def test_ping_s_bsd_parameter_problem(self):
        """
        Test 'ping' on macOS/BSD with an IPv4 'Parameter problem' error message
        """
        data = [
            'PING 192.0.2.10 (192.0.2.10): 56 data bytes',
            '92 bytes from 10.0.0.1: Parameter problem: pointer = 0x14',
            '92 bytes from 10.0.0.1: Source Quench'
        ]
        expected = [
            {'type': 'parameter_problem', 'response_bytes': 92, 'destination_ip': '192.0.2.10', 'response_ip': '10.0.0.1'},
            {'type': 'source_quench', 'response_bytes': 92, 'destination_ip': '192.0.2.10', 'response_ip': '10.0.0.1'}
        ]
        self.assertEqual(list(jc.parsers.ping_s.parse(data, quiet=True)), expected)

    def test_ping_s_ip_alpine_linux(self):
        """
        Test 'ping <ip>' on alpine linux
        """
        result = list(jc.parsers.ping_s.parse(self.alpine_linux_3_13_ping_ip.splitlines(), quiet=True))
        self.assertEqual(result, self.alpine_linux_3_13_ping_ip_streaming_json)
        self.assertEqual(result[-1]['round_trip_ms_max'], 1.637)
        self.assertIsNone(result[-1]['round_trip_ms_stddev'])

    def test_ping_s_hostname_alpine_linux(self):
        """
        Test 'ping <hostname>' on alpine linux
        """
        self.assertEqual(list(jc.parsers.ping_s.parse(self.alpine_linux_3_13_ping_hostname.splitlines(), quiet=True)), self.alpine_linux_3_13_ping_hostname_streaming_json)

    def test_ping_s_osx_all_lost_summary(self):
        """
        Test 'ping' on macOS/BSD with 100% packet loss and no round-trip line
        """
        data = [
            'PING 192.0.2.1 (192.0.2.1): 56 data bytes',
            'Request timeout for icmp_seq 0',
            '',
            '--- 192.0.2.1 ping statistics ---',
            '2 packets transmitted, 0 packets received, 100.0% packet loss'
        ]
        expected = [
            {'type': 'timeout', 'destination_ip': '192.0.2.1', 'sent_bytes': 56, 'pattern': None, 'icmp_seq': 0},
            {'type': 'summary', 'destination_ip': '192.0.2.1', 'sent_bytes': 56, 'pattern': None, 'packets_transmitted': 2,
             'packets_received': 0, 'packet_loss_percent': 100.0, 'duplicates': 0, 'round_trip_ms_min': None,
             'round_trip_ms_avg': None, 'round_trip_ms_max': None, 'round_trip_ms_stddev': None}
        ]
        self.assertEqual(list(jc.parsers.ping_s.parse(data, quiet=True)), expected)

    def test_ping_s_linux_hostname_from(self):
        """
        Test 'ping <hostname>' on linux with 'from' in the host name
        """
        result = list(jc.parsers.ping_s.parse(self.generic_ping_linux_hostname_from.splitlines(), quiet=True))
        self.assertEqual(result, self.generic_ping_linux_hostname_from_streaming_json)
        self.assertEqual(result[0]['sent_bytes'], 56)

    def test_ping6_s_linux_hostname_from(self):
        """
        Test 'ping6 <hostname>' on linux with 'from' in the host name
        """
        result = list(jc.parsers.ping_s.parse(self.generic_ping6_linux_hostname_from.splitlines(), quiet=True))
        self.assertEqual(result, self.generic_ping6_linux_hostname_from_streaming_json)
        self.assertEqual(result[0]['destination_ip'], '2001:db8::1')

    def test_ping_s_linux_header_formats(self):
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
            data = [header, '64 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=0.040 ms']
            result = list(jc.parsers.ping_s.parse(data, quiet=True))
            self.assertEqual((result[0]['destination_ip'], result[0]['sent_bytes']), (dest, data_bytes), header)

    def test_ping_s_bsd_source_address_header(self):
        """
        Test 'ping -S <src>' on macOS/BSD where the header shows the source address
        """
        for header in ('PING 192.0.2.10 (192.0.2.10) from 192.168.1.221: 56 data bytes',
                       'PING host.example.com (192.0.2.10) from 192.168.1.221: 1472 data bytes'):
            data = [header, '64 bytes from 192.0.2.10: icmp_seq=0 ttl=56 time=12.345 ms']
            result = list(jc.parsers.ping_s.parse(data, quiet=True))
            self.assertEqual(result[0]['destination_ip'], '192.0.2.10', header)
            self.assertEqual(result[0]['sent_bytes'], int(header.split()[-3]), header)
            self.assertEqual(result[0]['response_ip'], '192.0.2.10', header)

    def test_ping6_s_bsd_icmp_errors(self):
        """
        Test 'ping6' on macOS/FreeBSD with the ICMPv6 error messages of BSD ping6
        """
        result = list(jc.parsers.ping_s.parse(self.generic_ping6_bsd_icmp_errors.splitlines(), quiet=True))
        self.assertEqual(result, self.generic_ping6_bsd_icmp_errors_streaming_json)
        self.assertEqual([r['type'] for r in result],
                         ['no_route_to_destination', 'destination_administratively_unreachable',
                          'destination_unreachable_beyond_scope', 'packet_too_big',
                          'destination_unreachable_bad_code', 'reply', 'summary'])
        self.assertEqual(result[1]['response_ip'], 'fe80::1%em0')
        self.assertEqual(result[3]['response_bytes'], 1280)

    def test_ping_s_error_tables_match_ping(self):
        """
        Test 'ping_s' and 'ping' with the same table of ICMP error messages
        """
        import jc.parsers.ping
        for message in ('No Route to Destination', 'Destination Administratively Unreachable',
                        'Destination Unreachable Beyond Scope', 'Packet too big mtu = 1280',
                        'Destination Unreachable, Bad Code: 7', 'Destination Host Unreachable',
                        'Communication prohibited by filter', 'Weird error message'):
            line = '56 bytes from 192.0.2.1: ' + message
            self.assertEqual(jc.parsers.ping_s._error_type_v4(line), jc.parsers.ping._error_type(line), message)


if __name__ == '__main__':
    unittest.main()
