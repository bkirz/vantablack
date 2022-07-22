import copy
import decimal

import simfile
from simfile.timing import displaybpm


def mmod_bpm(
    sf: simfile.Simfile, ssc_chart: simfile.SSCChart = simfile.SSCChart()
) -> decimal.Decimal:
    """
    Given a simfile, replicates the calculation done by stepmania to determine the
    maximum BPM to use when calculating the scroll modifier for an M-Mod.
    If a DISPLAYBPM is set (and isn't set to '*'), it uses its max value.
    Otherwise it finds the max BPM from the file's BPMS field.

    If both an SSCSimfile and an SSCChart are provided, and if the chart contains any
    timing fields, the chart will be used as the source of timing.
    """

    # We can safely delegate to displaybpm most of the time, since its max value
    # is almost always what we want. However, if the displaybpm is set to random ('*'
    # in the simfile) then we can't get the mmod value that way. This kludge short-circuits
    # that behavior by forcibly removing '*' values.
    copied_file = copy.copy(sf)
    if copied_file.displaybpm == '*':
        del copied_file.displaybpm

    copied_ssc = copy.copy(ssc_chart)
    if copied_ssc.displaybpm == '*':
        del copied_ssc.displaybpm

    match displaybpm.displaybpm(copied_file, copied_ssc):
        case displaybpm.StaticDisplayBPM(value=value):
            return value
        case displaybpm.RangeDisplayBPM(max=max):
            return max
