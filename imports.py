import convokit
import pandas as pd
import os
from pathlib import Path

# Get the project root directory (where your script is)
PROJECT_ROOT = Path(__file__).parent

# Build paths relative to project root
raw_data_file = PROJECT_ROOT / "data" / "guyana_utterances.csv"