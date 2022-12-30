"""jc - JSON Convert `/proc/net/netstat` file parser

Usage (cli):

    $ cat /proc/net/netstat | jc --proc

or

    $ jc /proc/net/netstat

or

    $ cat /proc/net/netstat | jc --proc-net-netstat

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_netstat_file)

or

    import jc
    result = jc.parse('proc_net_netstat', proc_net_netstat_file)

Schema:

All values except "type" are integers

    [
      {
        "type":                     string,
        "<key>":                    integer
      }
    ]

Examples:

    $ cat /proc/net/netstat | jc --proc -p
    [
      {
        "SyncookiesSent": 0,
        "SyncookiesRecv": 0,
        "SyncookiesFailed": 0,
        "EmbryonicRsts": 0,
        "PruneCalled": 0,
        "RcvPruned": 0,
        "OfoPruned": 0,
        "OutOfWindowIcmps": 0,
        "LockDroppedIcmps": 0,
        "ArpFilter": 0,
        "TW": 3,
        "TWRecycled": 0,
        "TWKilled": 0,
        "PAWSActive": 0,
        "PAWSEstab": 0,
        "DelayedACKs": 10,
        "DelayedACKLocked": 53,
        "DelayedACKLost": 0,
        "ListenOverflows": 0,
        "ListenDrops": 0,
        "TCPHPHits": 2387,
        "TCPPureAcks": 12711,
        "TCPHPAcks": 53535,
        "TCPRenoRecovery": 0,
        "TCPSackRecovery": 0,
        "TCPSACKReneging": 0,
        "TCPSACKReorder": 0,
        "TCPRenoReorder": 0,
        "TCPTSReorder": 0,
        "TCPFullUndo": 0,
        "TCPPartialUndo": 0,
        "TCPDSACKUndo": 0,
        "TCPLossUndo": 0,
        "TCPLostRetransmit": 0,
        "TCPRenoFailures": 0,
        "TCPSackFailures": 0,
        "TCPLossFailures": 0,
        "TCPFastRetrans": 0,
        "TCPSlowStartRetrans": 0,
        "TCPTimeouts": 0,
        "TCPLossProbes": 0,
        "TCPLossProbeRecovery": 0,
        "TCPRenoRecoveryFail": 0,
        "TCPSackRecoveryFail": 0,
        "TCPRcvCollapsed": 0,
        "TCPBacklogCoalesce": 2883,
        "TCPDSACKOldSent": 0,
        "TCPDSACKOfoSent": 0,
        "TCPDSACKRecv": 0,
        "TCPDSACKOfoRecv": 0,
        "TCPAbortOnData": 0,
        "TCPAbortOnClose": 1,
        "TCPAbortOnMemory": 0,
        "TCPAbortOnTimeout": 0,
        "TCPAbortOnLinger": 0,
        "TCPAbortFailed": 0,
        "TCPMemoryPressures": 0,
        "TCPMemoryPressuresChrono": 0,
        "TCPSACKDiscard": 0,
        "TCPDSACKIgnoredOld": 0,
        "TCPDSACKIgnoredNoUndo": 0,
        "TCPSpuriousRTOs": 0,
        "TCPMD5NotFound": 0,
        "TCPMD5Unexpected": 0,
        "TCPMD5Failure": 0,
        "TCPSackShifted": 0,
        "TCPSackMerged": 0,
        "TCPSackShiftFallback": 0,
        "TCPBacklogDrop": 0,
        "PFMemallocDrop": 0,
        "TCPMinTTLDrop": 0,
        "TCPDeferAcceptDrop": 0,
        "IPReversePathFilter": 0,
        "TCPTimeWaitOverflow": 0,
        "TCPReqQFullDoCookies": 0,
        "TCPReqQFullDrop": 0,
        "TCPRetransFail": 0,
        "TCPRcvCoalesce": 151,
        "TCPOFOQueue": 0,
        "TCPOFODrop": 0,
        "TCPOFOMerge": 0,
        "TCPChallengeACK": 0,
        "TCPSYNChallenge": 0,
        "TCPFastOpenActive": 0,
        "TCPFastOpenActiveFail": 0,
        "TCPFastOpenPassive": 0,
        "TCPFastOpenPassiveFail": 0,
        "TCPFastOpenListenOverflow": 0,
        "TCPFastOpenCookieReqd": 0,
        "TCPFastOpenBlackhole": 0,
        "TCPSpuriousRtxHostQueues": 0,
        "BusyPollRxPackets": 0,
        "TCPAutoCorking": 28376,
        "TCPFromZeroWindowAdv": 0,
        "TCPToZeroWindowAdv": 0,
        "TCPWantZeroWindowAdv": 0,
        "TCPSynRetrans": 0,
        "TCPOrigDataSent": 119438,
        "TCPHystartTrainDetect": 3,
        "TCPHystartTrainCwnd": 60,
        "TCPHystartDelayDetect": 0,
        "TCPHystartDelayCwnd": 0,
        "TCPACKSkippedSynRecv": 0,
        "TCPACKSkippedPAWS": 0,
        "TCPACKSkippedSeq": 0,
        "TCPACKSkippedFinWait2": 0,
        "TCPACKSkippedTimeWait": 0,
        "TCPACKSkippedChallenge": 0,
        "TCPWinProbe": 0,
        "TCPKeepAlive": 6,
        "TCPMTUPFail": 0,
        "TCPMTUPSuccess": 0,
        "TCPDelivered": 119453,
        "TCPDeliveredCE": 0,
        "TCPAckCompressed": 0,
        "TCPZeroWindowDrop": 0,
        "TCPRcvQDrop": 0,
        "TCPWqueueTooBig": 0,
        "TCPFastOpenPassiveAltKey": 0,
        "TcpTimeoutRehash": 0,
        "TcpDuplicateDataRehash": 0,
        "type": "TcpExt"
      },
      ...
    ]

    $ cat /proc/net/netstat | jc --proc-net-netstat -p -r
    [
      {
        "SyncookiesSent": "0",
        "SyncookiesRecv": "0",
        "SyncookiesFailed": "0",
        "EmbryonicRsts": "0",
        "PruneCalled": "0",
        "RcvPruned": "0",
        "OfoPruned": "0",
        "OutOfWindowIcmps": "0",
        "LockDroppedIcmps": "0",
        "ArpFilter": "0",
        "TW": "3",
        "TWRecycled": "0",
        "TWKilled": "0",
        "PAWSActive": "0",
        "PAWSEstab": "0",
        "DelayedACKs": "10",
        "DelayedACKLocked": "53",
        "DelayedACKLost": "0",
        "ListenOverflows": "0",
        "ListenDrops": "0",
        "TCPHPHits": "2387",
        "TCPPureAcks": "12711",
        "TCPHPAcks": "53535",
        "TCPRenoRecovery": "0",
        "TCPSackRecovery": "0",
        "TCPSACKReneging": "0",
        "TCPSACKReorder": "0",
        "TCPRenoReorder": "0",
        "TCPTSReorder": "0",
        "TCPFullUndo": "0",
        "TCPPartialUndo": "0",
        "TCPDSACKUndo": "0",
        "TCPLossUndo": "0",
        "TCPLostRetransmit": "0",
        "TCPRenoFailures": "0",
        "TCPSackFailures": "0",
        "TCPLossFailures": "0",
        "TCPFastRetrans": "0",
        "TCPSlowStartRetrans": "0",
        "TCPTimeouts": "0",
        "TCPLossProbes": "0",
        "TCPLossProbeRecovery": "0",
        "TCPRenoRecoveryFail": "0",
        "TCPSackRecoveryFail": "0",
        "TCPRcvCollapsed": "0",
        "TCPBacklogCoalesce": "2883",
        "TCPDSACKOldSent": "0",
        "TCPDSACKOfoSent": "0",
        "TCPDSACKRecv": "0",
        "TCPDSACKOfoRecv": "0",
        "TCPAbortOnData": "0",
        "TCPAbortOnClose": "1",
        "TCPAbortOnMemory": "0",
        "TCPAbortOnTimeout": "0",
        "TCPAbortOnLinger": "0",
        "TCPAbortFailed": "0",
        "TCPMemoryPressures": "0",
        "TCPMemoryPressuresChrono": "0",
        "TCPSACKDiscard": "0",
        "TCPDSACKIgnoredOld": "0",
        "TCPDSACKIgnoredNoUndo": "0",
        "TCPSpuriousRTOs": "0",
        "TCPMD5NotFound": "0",
        "TCPMD5Unexpected": "0",
        "TCPMD5Failure": "0",
        "TCPSackShifted": "0",
        "TCPSackMerged": "0",
        "TCPSackShiftFallback": "0",
        "TCPBacklogDrop": "0",
        "PFMemallocDrop": "0",
        "TCPMinTTLDrop": "0",
        "TCPDeferAcceptDrop": "0",
        "IPReversePathFilter": "0",
        "TCPTimeWaitOverflow": "0",
        "TCPReqQFullDoCookies": "0",
        "TCPReqQFullDrop": "0",
        "TCPRetransFail": "0",
        "TCPRcvCoalesce": "151",
        "TCPOFOQueue": "0",
        "TCPOFODrop": "0",
        "TCPOFOMerge": "0",
        "TCPChallengeACK": "0",
        "TCPSYNChallenge": "0",
        "TCPFastOpenActive": "0",
        "TCPFastOpenActiveFail": "0",
        "TCPFastOpenPassive": "0",
        "TCPFastOpenPassiveFail": "0",
        "TCPFastOpenListenOverflow": "0",
        "TCPFastOpenCookieReqd": "0",
        "TCPFastOpenBlackhole": "0",
        "TCPSpuriousRtxHostQueues": "0",
        "BusyPollRxPackets": "0",
        "TCPAutoCorking": "28376",
        "TCPFromZeroWindowAdv": "0",
        "TCPToZeroWindowAdv": "0",
        "TCPWantZeroWindowAdv": "0",
        "TCPSynRetrans": "0",
        "TCPOrigDataSent": "119438",
        "TCPHystartTrainDetect": "3",
        "TCPHystartTrainCwnd": "60",
        "TCPHystartDelayDetect": "0",
        "TCPHystartDelayCwnd": "0",
        "TCPACKSkippedSynRecv": "0",
        "TCPACKSkippedPAWS": "0",
        "TCPACKSkippedSeq": "0",
        "TCPACKSkippedFinWait2": "0",
        "TCPACKSkippedTimeWait": "0",
        "TCPACKSkippedChallenge": "0",
        "TCPWinProbe": "0",
        "TCPKeepAlive": "6",
        "TCPMTUPFail": "0",
        "TCPMTUPSuccess": "0",
        "TCPDelivered": "119453",
        "TCPDeliveredCE": "0",
        "TCPAckCompressed": "0",
        "TCPZeroWindowDrop": "0",
        "TCPRcvQDrop": "0",
        "TCPWqueueTooBig": "0",
        "TCPFastOpenPassiveAltKey": "0",
        "TcpTimeoutRehash": "0",
        "TcpDuplicateDataRehash": "0",
        "type": "TcpExt"
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils
from jc.parsers.universal import simple_table_parse


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/netstat` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for item in proc_data:
        for key, val in item.items():
            if key != 'type':
                item[key] = int(val)

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []
    rows: List = []
    this_row: str = ''
    headers: str = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            row_name, header_data = line.split(':', maxsplit=1)

            if row_name in rows:
                # this is data
                _, row_data = line.split(':', maxsplit=1)
                data_table = headers + row_data
                output_line = simple_table_parse(data_table.splitlines())
                output_line[0]['type'] = this_row
                raw_output.extend(output_line)
                continue

            else:
                # this is a header row
                rows.append(row_name)
                this_row = row_name
                headers = header_data + '\n'
                continue

    return raw_output if raw else _process(raw_output)
