import dash
from utils_app import *
import feather


##################################################
df = feather.read_dataframe('ninetoten.feather')
metadata = feather.read_dataframe('metadata.feather')
lons = pd.unique(metadata['longitude'])
lats = pd.unique(metadata['latitude'])
