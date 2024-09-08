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

    # ubunutu 18.4
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


if __name__ == '__main__':
    unittest.main()
