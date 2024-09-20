# Import things
import pytest
import pandas as pd
import main as m

# Suppress the FutureWarning's
@pytest.mark.filterwarnings("ignore")

# Define our tests
def test_seconds():
    # Create some testing data
    d = {'KMs': [200, 50, 2000, 4000], 'Duration': ['02:03:49', '00:26:49.123', '1.06:11:50.098', '2.12:22:50']}
    df = pd.DataFrame(data=d)

    cols = ["Duration"]
    # Test on a standard hours, minutes and seconds
    assert m.convert_to_seconds(df,cols)["Duration_seconds"][0] == 7429, "Output was not 7429"
    # Test on hours, minutes, seconds and milliseconds
    assert m.convert_to_seconds(df,cols)["Duration_seconds"][1] == 1609.123, "Output was not 1609.123"
    # Test when more than 24 hours
    assert m.convert_to_seconds(df,cols)["Duration_seconds"][2] == 108710.098, "Output was not 108710.098"
    # Test when more than two days
    assert m.convert_to_seconds(df,cols)["Duration_seconds"][3] == 217370, "Output was not 217370"