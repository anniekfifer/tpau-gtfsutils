import numpy as np
from tpau_gtfsutilities.gtfs.gtfssingleton import gtfs
from tpau_gtfsutilities.helpers.datetimehelpers import GTFSDateRange
from tpau_gtfsutilities.helpers.datetimehelpers import GTFSDate

def filter_calendars_by_daterange(daterange):
    calendar = gtfs.get_table('calendar')
    filter_daterange = GTFSDateRange(daterange['start'], daterange['end'])

    calendar['_gtfs_daterange'] = calendar.apply(lambda row: GTFSDateRange(row['start_date'], row['end_date']), axis=1)
    calendar['_overlap'] = calendar['_gtfs_daterange'].apply(lambda dr: \
        filter_daterange.overlap(dr) \
    )

    calendar_filtered = calendar[calendar['_overlap'].notnull()]

    gtfs.update_table('calendar', calendar_filtered, allow_column_changes=False)
    

def filter_calendar_dates_by_daterange(daterange):
    if not gtfs.has_table('calendar_dates'): return

    calendar_dates = gtfs.get_table('calendar_dates')
    filter_daterange = GTFSDateRange(daterange['start'], daterange['end'])

    calendar_dates['_gtfs_date'] = calendar_dates.apply(lambda row: GTFSDate(row['date']), axis=1)
    calendar_dates['_inrange'] = calendar_dates.apply(lambda row: filter_daterange.includes(row['date']), axis=1)

    calendar_dates_filtered = calendar_dates[calendar_dates['_inrange']]

    gtfs.update_table('calendar_dates', calendar_dates_filtered, allow_column_changes=False)

def reset_feed_dates(daterange):
    if not gtfs.has_table('feed_info'): return

    gtfs_daterange = GTFSDateRange(daterange['start'], daterange['end'])
    feed_info = gtfs.get_table('feed_info')

    feed_info['feed_start_date'] = gtfs_daterange.start.datestring()
    feed_info['feed_end_date'] = gtfs_daterange.end.datestring()

    gtfs.update_table('feed_info', feed_info, allow_column_changes=False)
