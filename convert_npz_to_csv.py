from src.dataprocessing import (
    prepare_csv_conv,
    write_top_csv_row,
    parse_npzdata_in_csv,
    get_sample,
    get_config,
    get_BallAnomaly_properties,
)

# path to .npz directory
l_path = "measurements/acryl_skip_8_d_30/"

# load info
tmp, _ = get_sample(l_path, idx=0)
# get object and anomaly properties
config = get_config(tmp)
anomaly = get_BallAnomaly_properties(tmp)
# create conversion info
conv_info = prepare_csv_conv(l_path)
# write csv header
write_top_csv_row(conv_info, config, anomaly)
# convert data to .csv
parse_npzdata_in_csv(conv_info)
