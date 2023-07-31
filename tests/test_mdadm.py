import os
import unittest
import json
import jc.parsers.mdadm

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid0-offline.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid0_offline = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid0-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid0_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-0-90-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_0_90_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-checking.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_checking = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-failfast.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_failfast = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-faulty1.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_faulty1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-faulty2.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_faulty2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-moreflags.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_moreflags = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-replacing.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_replacing = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-resync.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_resync = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-spare.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_spare = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-syncing.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_syncing = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine.out'), 'r', encoding='utf-8') as f:
        mdadm_examine = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-detail.out'), 'r', encoding='utf-8') as f:
        mdadm_query_detail = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid0-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid0_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-failed-and-flags.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_failed_and_flags = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty-and-removed.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty_and_removed = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty-with-spare.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty_with_spare = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-0-9.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_0_9 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-failfast.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_failfast = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-spare.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_spare = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-rebuild-failfast.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_rebuild_failfast = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-spare-writem-rebuild.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_spare_writem_rebuild = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-syncing.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_syncing = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container1.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_container1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container2-dev1.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_container2_dev1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container2-dev2.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_container2_dev2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-homehost.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_homehost = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-meta09.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_meta09 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_ok = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container1-member.out'), 'r', encoding='utf-8') as f:
        mdadm_query_container1_member = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container1-root.out'), 'r', encoding='utf-8') as f:
        mdadm_query_container1_root = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container2-member.out'), 'r', encoding='utf-8') as f:
        mdadm_query_container2_member = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container2-root.out'), 'r', encoding='utf-8') as f:
        mdadm_query_container2_root = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-homehost.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_homehost = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-meta09.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_meta09 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-ok.out'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_ok = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid0-offline.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid0_offline_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid0-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid0_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-0-90-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_0_90_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-checking.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_checking_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-failfast.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_failfast_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-faulty1.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_faulty1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-faulty2.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_faulty2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-moreflags.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_moreflags_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-replacing.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_replacing_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-resync.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_resync_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-spare.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_spare_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid1-syncing.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid1_syncing_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-detail.json'), 'r', encoding='utf-8') as f:
        mdadm_query_detail_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid0-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid0_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-failed-and-flags.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_failed_and_flags_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty-and-removed.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty_and_removed_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty-with-spare.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty_with_spare_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-faulty.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_faulty_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-0-9.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_0_9_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-failfast.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_failfast_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok-spare.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_spare_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-rebuild-failfast.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_rebuild_failfast_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-spare-writem-rebuild.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_spare_writem_rebuild_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid1-syncing.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid1_syncing_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container1.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_container1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container2-dev1.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_container2_dev1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-container2-dev2.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_container2_dev2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-homehost.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_homehost_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-meta09.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_meta09_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-examine-raid5-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_examine_raid5_ok_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container1-member.json'), 'r', encoding='utf-8') as f:
        mdadm_query_container1_member_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container1-root.json'), 'r', encoding='utf-8') as f:
        mdadm_query_container1_root_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container2-member.json'), 'r', encoding='utf-8') as f:
        mdadm_query_container2_member_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-container2-root.json'), 'r', encoding='utf-8') as f:
        mdadm_query_container2_root_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-homehost.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_homehost_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-meta09.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_meta09_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mdadm-query-raid5-ok.json'), 'r', encoding='utf-8') as f:
        mdadm_query_raid5_ok_json = json.loads(f.read())


    def test_mdadm_nodata(self):
        """
        Test 'mdadm' with no data
        """
        self.assertEqual(jc.parsers.mdadm.parse('', quiet=True), {})


    def test_mdadm_examine_raid0_offline(self):
        """
        Test 'mdadm --examine' with offline RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid0_offline, quiet=True), self.mdadm_examine_raid0_offline_json)


    def test_mdadm_examine_raid0_ok(self):
        """
        Test 'mdadm --examine' with ok RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid0_ok, quiet=True), self.mdadm_examine_raid0_ok_json)


    def test_mdadm_examine_raid1_0_90_ok(self):
        """
        Test 'mdadm --examine' with ok RAID array v0.90
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_0_90_ok, quiet=True), self.mdadm_examine_raid1_0_90_ok_json)


    def test_mdadm_examine_raid1_checking(self):
        """
        Test 'mdadm --examine' with checking RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_checking, quiet=True), self.mdadm_examine_raid1_checking_json)


    def test_mdadm_examine_raid1_failfast(self):
        """
        Test 'mdadm --examine' with failfast RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_failfast, quiet=True), self.mdadm_examine_raid1_failfast_json)


    def test_mdadm_examine_raid1_faulty1(self):
        """
        Test 'mdadm --examine' with faulty RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_faulty1, quiet=True), self.mdadm_examine_raid1_faulty1_json)


    def test_mdadm_examine_raid1_faulty2(self):
        """
        Test 'mdadm --examine' with faulty RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_faulty2, quiet=True), self.mdadm_examine_raid1_faulty2_json)


    def test_mdadm_examine_raid1_moreflags(self):
        """
        Test 'mdadm --examine' with RAID array with several flags
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_moreflags, quiet=True), self.mdadm_examine_raid1_moreflags_json)


    def test_mdadm_examine_raid1_ok(self):
        """
        Test 'mdadm --examine' with ok RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_ok, quiet=True), self.mdadm_examine_raid1_ok_json)


    def test_mdadm_examine_raid1_replacing(self):
        """
        Test 'mdadm --examine' with replacing RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_replacing, quiet=True), self.mdadm_examine_raid1_replacing_json)


    def test_mdadm_examine_raid1_resync(self):
        """
        Test 'mdadm --examine' with resyncing RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_resync, quiet=True), self.mdadm_examine_raid1_resync_json)


    def test_mdadm_examine_raid1_spare(self):
        """
        Test 'mdadm --examine' with spare in RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_spare, quiet=True), self.mdadm_examine_raid1_spare_json)


    def test_mdadm_examine_raid1_syncing(self):
        """
        Test 'mdadm --examine' with syncing RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid1_syncing, quiet=True), self.mdadm_examine_raid1_syncing_json)


    def test_mdadm_examine(self):
        """
        Test 'mdadm --examine'
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine, quiet=True), self.mdadm_examine_json)


    def test_mdadm_query_detail(self):
        """
        Test 'mdadm --query --detail'
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_detail, quiet=True), self.mdadm_query_detail_json)


    def test_mdadm_query_raid0_ok(self):
        """
        Test 'mdadm --query' on ok RAID array
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid0_ok, quiet=True), self.mdadm_query_raid0_ok_json)


    def test_mdadm_query_raid1_failed_and_flags(self):
        """
        Test 'mdadm --query' on failed RAID array with flags
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_failed_and_flags, quiet=True), self.mdadm_query_raid1_failed_and_flags_json)


    def test_mdadm_query_raid1_faulty_and_removed(self):
        """
        Test 'mdadm --query' on faulty RAID array with removed disk
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_faulty_and_removed, quiet=True), self.mdadm_query_raid1_faulty_and_removed_json)


    def test_mdadm_query_raid1_faulty_with_spare(self):
        """
        Test 'mdadm --query' on faulty RAID array with spare disk
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_faulty_with_spare, quiet=True), self.mdadm_query_raid1_faulty_with_spare_json)


    def test_mdadm_query_raid1_faulty(self):
        """
        Test 'mdadm --query' on faulty RAID
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_faulty, quiet=True), self.mdadm_query_raid1_faulty_json)


    def test_mdadm_query_raid1_ok_0_9(self):
        """
        Test 'mdadm --query' on ok RAID on v0.9
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_ok_0_9, quiet=True), self.mdadm_query_raid1_ok_0_9_json)


    def test_mdadm_query_raid1_ok_failfast(self):
        """
        Test 'mdadm --query' on ok RAID with failfast
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_ok_failfast, quiet=True), self.mdadm_query_raid1_ok_failfast_json)


    def test_mdadm_query_raid1_ok_spare(self):
        """
        Test 'mdadm --query' on ok RAID with spare
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_ok_spare, quiet=True), self.mdadm_query_raid1_ok_spare_json)


    def test_mdadm_query_raid1_ok(self):
        """
        Test 'mdadm --query' on ok RAID
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_ok, quiet=True), self.mdadm_query_raid1_ok_json)


    def test_mdadm_query_raid1_rebuild_failfast(self):
        """
        Test 'mdadm --query' on rebuilding RAID with failfast
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_rebuild_failfast, quiet=True), self.mdadm_query_raid1_rebuild_failfast_json)


    def test_mdadm_query_raid1_spare_writem_rebuild(self):
        """
        Test 'mdadm --query' on rebuilding RAID with spare
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_spare_writem_rebuild, quiet=True), self.mdadm_query_raid1_spare_writem_rebuild_json)


    def test_mdadm_query_raid1_syncing(self):
        """
        Test 'mdadm --query' on syncing RAID
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid1_syncing, quiet=True), self.mdadm_query_raid1_syncing_json)


    def test_mdadm_examine_container1(self):
        """
        Test 'mdadm --examine' on container 1
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_container1, quiet=True), self.mdadm_examine_container1_json)


    def test_mdadm_examine_container2_dev1(self):
        """
        Test 'mdadm --examine' on container 1 dev 1
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_container2_dev1, quiet=True), self.mdadm_examine_container2_dev1_json)


    def test_mdadm_examine_container2_dev2(self):
        """
        Test 'mdadm --examine' on container 1 dev 2
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_container2_dev2, quiet=True), self.mdadm_examine_container2_dev2_json)


    def test_mdadm_examine_raid5_homehost(self):
        """
        Test 'mdadm --examine' on RAID5 homehost
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid5_homehost, quiet=True), self.mdadm_examine_raid5_homehost_json)


    def test_mdadm_examine_raid5_meta09(self):
        """
        Test 'mdadm --examine' on RAID5 on v0.9
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid5_meta09, quiet=True), self.mdadm_examine_raid5_meta09_json)


    def test_mdadm_examine_raid5_ok(self):
        """
        Test 'mdadm --examine' on ok RAID5
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_examine_raid5_ok, quiet=True), self.mdadm_examine_raid5_ok_json)


    def test_mdadm_query_container1_member(self):
        """
        Test 'mdadm --query' container1 member
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_container1_member, quiet=True), self.mdadm_query_container1_member_json)


    def test_mdadm_query_container1_root(self):
        """
        Test 'mdadm --query' container1 root
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_container1_root, quiet=True), self.mdadm_query_container1_root_json)


    def test_mdadm_query_container2_member(self):
        """
        Test 'mdadm --query' container2 member
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_container2_member, quiet=True), self.mdadm_query_container2_member_json)


    def test_mdadm_query_container2_root(self):
        """
        Test 'mdadm --query' container2 root
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_container2_root, quiet=True), self.mdadm_query_container2_root_json)


    def test_mdadm_query_raid5_homehost(self):
        """
        Test 'mdadm --query' RAID5 with homehost
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid5_homehost, quiet=True), self.mdadm_query_raid5_homehost_json)


    def test_mdadm_query_raid5_meta09(self):
        """
        Test 'mdadm --query' RAID5 on v0.9
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid5_meta09, quiet=True), self.mdadm_query_raid5_meta09_json)


    def test_mdadm_query_raid5_ok(self):
        """
        Test 'mdadm --query' on ok RAID5
        """
        self.assertEqual(jc.parsers.mdadm.parse(self.mdadm_query_raid5_ok, quiet=True), self.mdadm_query_raid5_ok_json)


if __name__ == '__main__':
    unittest.main()
