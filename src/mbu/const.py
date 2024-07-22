
# Define MBU launcher exit error
EXIT_OK = 0
EXIT_INCOMPLETE = 127
EXIT_PB = 128

SAFE_PRODOUCTS_RE = r"(?P<mission>.{3})" \
                    r"_(?P<acquisition_mode>.{2})" \
                    r"_(?P<product_type>.{3})(?P<resolution>.)" \
                    r"_(?P<processing_level>.)(?P<product_class>.)(?P<polarisation>.{2})" \
                    r"_(?P<start_time>.{15})" \
                    r"_(?P<end_time>.{15})" \
                    r"_(?P<orbit>.{6})" \
                    r"_(?P<mission_data_take_id>.{6})" \
                    r"_(?P<PUID>.{4})(\.SAFE)?"


OUTPUT_CDF_RE = r"(?P<mission>.{3})-(?P<swath>\w*)-(?P<prodtype>(ocn))" \
                r"-(?P<pol>(v|h){2})" \
                r"-(?P<start>\d{8}(t|T)\d{6})" \
                r"-(?P<end>\d{8}(t|T)\d{6})" \
                r"-(?P<orbit>\d{6})" \
                r"-(?P<missionDataID>[\da-fA-F]{6})" \
                r"-(?P<numimg>\d{3})(_sw[0-9])?.nc"

TIME_CDF_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
TIME_SAFE_FORMAT = "%Y%m%dT%H%M%S"
