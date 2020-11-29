from .gtfsutility import GTFSUtility
from tpau_gtfsutilities.config.utilityconfig import utilityconfig
from tpau_gtfsutilities.config.utilityoutput import utilityoutput
from tpau_gtfsutilities.gtfs.gtfssingleton import gtfs
from tpau_gtfsutilities.gtfs.gtfscollectionsingleton import gtfs_collection
from tpau_gtfsutilities.gtfs.gtfsreader import GTFSReader

from tpau_gtfsutilities.gtfs.methods.edit.calendars import remove_exception_calendars
from tpau_gtfsutilities.gtfs.methods.edit.cluster import cluster_stops
from tpau_gtfsutilities.gtfs.methods.analysis.stopvisits import calculate_stop_visits
from tpau_gtfsutilities.gtfs.methods.filters.subset import subset_entire_feed

class ClusterStops(GTFSUtility):
    name = 'cluster_stops'

    def run(self):
        settings = utilityconfig.get_settings()

        for feed in settings['gtfs_feeds']:
            gtfsreader = GTFSReader(feed)
            gtfs.load_feed(gtfsreader)
            gtfs.preprocess()

            subset_entire_feed(settings['date_range'], settings['time_range'])

            feed_no_extension = feed[:-4]
            gtfs_collection.add_feed(gtfs.copy(), feed_no_extension)

        cluster_stops(settings['cluster_radius'])
        
        # write stop visits report with clustered stops
        combined_visits_report = gtfs_collection.get_combined_computed_table(lambda gtfs: calculate_stop_visits(write_csv=False, gtfs_override=gtfs, include_removed_stops=False))
        utilityoutput.write_or_append_to_output_csv(combined_visits_report, 'stop_visit_report.csv', index=False)

        gtfs_collection.write_all_feeds()
