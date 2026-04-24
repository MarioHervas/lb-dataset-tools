import zipfile
from typing import Optional

import pandas as pd
from pathlib import Path
from dataclasses import dataclass

@dataclass
class LetterboxdData:
    ratings:    pd.Dataframe
    diary:      pd.DataFrame
    watched:    pd.DataFrame
    watchlist:  Optional[pd.DataFrame] = None
    reviews:    Optional[pd.DataFrame] = None
    likes_films:Optional[pd.DataFrame] = None
    username:   str = ""
