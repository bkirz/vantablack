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
    Uses the maximum DISPLAYBPM if available, otherwise falling back to the max BPM.

    If both an SSCSimfile and an SSCChart are provided, and if the chart contains any
    timing fields, the chart will be used as the source of timing.
    """

    match displaybpm.displaybpm(sf, ssc_chart):
        case displaybpm.StaticDisplayBPM(value=value):
            return value
        case displaybpm.RangeDisplayBPM(max=max):
            return max
        case displaybpm.RandomDisplayBPM():
            # We can safely delegate to displaybpm most of the time, since its max value
            # is almost always the same as the mmod bpm. However, if the displaybpm is set
            # to random ('*' in the simfile) then we can't get the mmod value that way.
            # This kludge short-circuits that behavior by forcibly removing '*' values.
            copied_simfile = copy.copy(sf)
            if copied_simfile.displaybpm == "*":
                del copied_simfile.displaybpm

            copied_ssc = copy.copy(ssc_chart)
            if copied_ssc.displaybpm == "*":
                del copied_ssc.displaybpm

            return mmod_bpm(copied_simfile, copied_ssc)
