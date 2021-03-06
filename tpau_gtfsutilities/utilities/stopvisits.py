import geopandas as gpd
from shapely.geometry import MultiPolygon

from .gtfsutility import GTFSUtility
from tpau_gtfsutilities.config.utilityconfig import utilityconfig
from tpau_gtfsutilities.config.utilityoutput import utilityoutput

from tpau_gtfsutilities.gtfs.methods.edit.calendars import remove_exception_calendars
from tpau_gtfsutilities.gtfs.methods.filters.subset import subset_entire_feed
from tpau_gtfsutilities.gtfs.methods.filters.polygon import filter_stops_by_multipolygon
from tpau_gtfsutilities.gtfs.methods.analysis.stopvisits import calculate_stop_visits

class StopVisits(GTFSUtility):
    name = 'stop_visits'

    def read_multipolygon_from_file(self, filepath):
        # Input: path to either shapefile or geojson
        # returns a multipolygon so both polygon and multipolygon
        # inputs can be read

        gdf = gpd.read_file(filepath).to_crs(epsg=4326)
        return MultiPolygon(gdf.geometry.iloc[0])

    def run_on_gtfs_singleton(self, settings):
        time_range_defined = 'time_range' in settings.keys() \
            and not isinstance(settings['time_range'], str) \
            and 'start' in settings['time_range'].keys() \
            and 'end' in settings['time_range'].keys()
    
        if time_range_defined:
            subset_entire_feed(settings['date_range'], settings['time_range'], trim_trips=True)
        else:
            subset_entire_feed(settings['date_range'])

        polygon_file = settings['polygon']
        
        if (polygon_file):
            polygon_file_path = utilityconfig.get_input_file_path(polygon_file)
            multipolygon = self.read_multipolygon_from_file(polygon_file_path)
            filter_stops_by_multipolygon(multipolygon)

        stop_visits_report = calculate_stop_visits()
        if time_range_defined:
            stop_visits_report['start_time'] = settings['time_range']['start']
            stop_visits_report['end_time'] = settings['time_range']['end']
        else:
            stop_visits_report['start_time'] = ''
            stop_visits_report['end_time'] = ''
        utilityoutput.write_or_append_to_output_csv(stop_visits_report, 'stop_visits.csv', write_gtfs_filename=True)
