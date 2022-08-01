import copy
import decimal

from simfile import Simfile, SSCChart
from simfile.timing import displaybpm


def mmod_bpm(
    simfile: Simfile, ssc_chart: SSCChart = SSCChart()
) -> decimal.Decimal:
    """
    Given a simfile, replicates the calculation done by stepmania to determine the
    maximum BPM to use when calculating the scroll modifier for an M-Mod.
    Uses the maximum DISPLAYBPM if available, otherwise falling back to the max BPM.

    If both an SSCSimfile and an SSCChart are provided, and if the chart contains any
    timing fields, the chart will be used as the source of timing.
    """

    match displaybpm.displaybpm(simfile, ssc_chart):
        case displaybpm.StaticDisplayBPM(value=value):
            return value
        case displaybpm.RangeDisplayBPM(max=max):
            return max
        case displaybpm.RandomDisplayBPM():
            # We can safely delegate to displaybpm most of the time, since its max value
            # is almost always the same as the mmod bpm. However, if the displaybpm is set
            # to random ('*' in the simfile) then we can't get the mmod value that way.
            # This kludge short-circuits that behavior by forcibly removing '*' values.
            if simfile.displaybpm == "*":
                simfile = copy.copy(simfile)
                del simfile.displaybpm

            if ssc_chart.displaybpm == "*":
                ssc_chart = copy.copy(ssc_chart)
                del ssc_chart.displaybpm

            return mmod_bpm(simfile, ssc_chart)
