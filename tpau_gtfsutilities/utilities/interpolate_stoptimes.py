import geopandas as gpd

from .gtfsutility import GTFSUtility
from tpau_gtfsutilities.gtfs.gtfssingleton import gtfs
from tpau_gtfsutilities.config.utilityconfig import utilityconfig

from tpau_gtfsutilities.gtfs.methods.edit.interpolation import interpolate_stop_times

class InterpolateStoptimes(GTFSUtility):
    name = 'interpolate_stoptimes'

    def run(self):
        settings = utilityconfig.get_settings()

        for feed in settings['gtfs_feeds']:
            gtfs.load_feed(feed)

            if not interpolate_stop_times():
                print("Cannot interpolate stop times -- feed needs to have shapes.txt and needs to use shape_dist_traveled in stop_times.txt")
            gtfs.close_tables()
            feed_no_extension = feed[:-4]
            gtfs.write_feed(feed_no_extension)