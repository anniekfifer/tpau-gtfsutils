from tpau_gtfsutilities.gtfs.gtfssingleton import gtfs

def prune_table_from_table_column(target, source, column, columns={}):
    # remove rows from target if column value not present in same column of source,  e.g.:
    #   prune_table_from_table_column('frequencies', 'trips', 'trip_id')
    # removes rows from frequencies if trip_id is not present in trips. 
    # 
    # column arg is omitted if columns dict is used to use columns with different names, e.g:
    #   prune_table_from_table_column('transfers', 'stops', columns={'transfers': 'from_stop_id', 'stops': 'stop_id'})

    # TODO handle missing optional tables

    if not gtfs.has_table(target): return

    target_df = gtfs.get_table(target, index=False)
    source_df = gtfs.get_table(source, index=False)

    target_col = column if not columns else columns[target]
    source_col = column if not columns else columns[source]

    target_pruned = target_df[target_df[target_col].isin(source_df[source_col])]
    gtfs.update_table(target, target_pruned)


def prune_unused_trips():
    prune_table_from_table_column('frequencies', 'trips', 'trip_id')
    prune_table_from_table_column('stop_times', 'trips', 'trip_id')
    # prune_table_from_table_column('attributions', 'trips', 'trip_id')

def prune_unused_calendars():
    # 'alternate' mode (see http://gtfs.org/reference/static/#calendar_datestxt)
    if gtfs.has_table('calendar_dates') and not gtfs.has_table('calendar'):
        prune_table_from_table_column('calendar_dates', 'trips', 'service_id') 
    else:
        prune_table_from_table_column('calendar', 'trips', 'service_id') 
        prune_table_from_table_column('calendar_dates', 'calendar', 'service_id') 

def prune_unused_stops():
    prune_stops_from_stop_times()
    # prune_table_from_table_column('transfers', 'stops', columns={'transfers': 'from_stop_id', 'stops': 'stop_id'})
    # prune_table_from_table_column('transfers', 'stops', columns={'transfers': 'to_stop_id', 'stops': 'stop_id'})
    # prune_table_from_table_column('pathways', 'stops', columns={'pathways': 'from_stop_id', 'stops': 'stop_id'})
    # prune_table_from_table_column('pathways', 'stops', columns={'pathways': 'to_stop_id', 'stops': 'stop_id'})

def prune_stops_from_stop_times():
    stops = gtfs.get_table('stops', index=False)
    stop_times = gtfs.get_table('stop_times')

    stops_pruned = stops[ \
        (stops['stop_id'].isin(stop_times['stop_id'])) \
            | (stops['stop_id'].isin(stops['parent_station'])) \
    ]

    # filter again to remove unused parent stops
    stops_pruned = stops_pruned[ \
        (stops_pruned['stop_id'].isin(stop_times['stop_id'])) \
            | (stops_pruned['stop_id'].isin(stops_pruned['parent_station'])) \
    ]

    gtfs.update_table('stops', stops_pruned)

def prune_unused_routes():
    prune_table_from_table_column('routes', 'trips', 'route_id')
    # prune_table_from_table_column('fare_rules', 'routes', 'route_id')
    # prune_table_from_table_column('attributions', 'routes', 'route_id')

def prune_unused_shapes():
    # prune_table_from_table_column('shapes', 'trips', 'shape_id')
    pass
