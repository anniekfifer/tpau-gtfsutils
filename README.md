# TPAU GTFS Utilities

## How To Use

### Requirements

- Anaconda

### Installation/Setup (Windows)

- Download repository by running `git clone git@github.com:anniekfifer/tpau-gtfsutils.git` in the CMD tool
- In the Anaconda Prompt application, run `initial-setup.bat` from the project root directory 

### Configuring and running a utility

- Edit the input parameters in the appropriate config yaml file in the `config/` folder. Follow formatting guidelines in the file's comments. 
- Copy or move any input GTFS is in the `data/` folder (GTFS in this folder will be read from, but not be altered in any way)
- To run a utility:
  - Open Anaconda Prompt application
  -  In project root directory, run `tpau-utils.bat` with the appropriate utility name (i.e., `tpau-utils.bat average_headway`)
    - Utilities:
      - Average Headway (`average_headway`): Generates csv report of average headways by route
      - One Day (`one_day`): Produces a subset of the feed within the given date or date range and time with service exceptions removed.

### Configuring and running example

- Edit `config/average_headway.yaml` input parameters to use example values in comments
- Make sure that `good_feed.zip` (included in repo for testing) is in `data/`
- In the Anaconda Prompt application, run `tpau-utils.bat average_headway`
  
### Output

- Application output will go to `output/` directory

## Behavior

### Average Headways
  
### Interpolate Stoptimes

### Cluster Stops

### One Day

### Stop Visits

### GTFS Output Notes

GTFS output may include some minor unintentional changes to the data, such as:

- Decimal truncation -- Decimals are rounded to the nearest 12 decimal places. This would most commonly occur in lat/lon coordinates, but 12 decimal places is sufficiently for most purposes. Trailing zeros are also stripped from decimals over one place.
- Conversion to float -- Columns that have a mixure of integer and float values will have integers converted to floats (i.e. 0 will become 0.0)
- Column reordering -- Columns that serve as IDs for a file (i.e. trip_id in trips.txt) may be brought to the front of the columns.
- Quotation removal -- The utilities remove wrapping quotes for fields that do not otherwise contain quotations or commas. 
