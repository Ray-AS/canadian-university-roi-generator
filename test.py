from pathlib import Path
import shutil
import tempfile
import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    """Sample dataset for testing calculations"""
    return pd.DataFrame(
        {
            "field": ["education", "business", "comp_sci"],
            "tuition": [5500, 8000, 7500],
            "earnings_2024_adjusted": [28000, 34000, 32000],
            "estimated_debt": [20000, 30000, 28000],
            "enrollment": [3000000, 15000000, 5000000],
            "total_tuition": [22000, 32000, 30000],
        }
    )


@pytest.fixture
def complete_data():
    """Complete dataset with ROI for testing outputs"""
    return pd.DataFrame(
        {
            "field": ["education", "business", "comp_sci"],
            "tuition": [5500, 8000, 7500],
            "total_tuition": [22000, 32000, 30000],
            "earnings_2024_adjusted": [28000, 34000, 32000],
            "estimated_debt": [20000, 30000, 28000],
            "enrollment": [3000000, 15000000, 5000000],
            "debt_to_income": [0.71, 0.88, 0.88],
            "payback_years": [9.5, 11.7, 11.7],
            "roi_5yr_w_tuition": [5.5, 4.3, 4.5],
            "roi_5yr_w_debt": [6.0, 4.8, 5.0],
            "earnings_per_dollar_tuition": [1.27, 1.06, 1.07],
            "earnings_5yr": [30600, 37150, 34970],
            "earnings_2018": [23140, 28100, 26450],
        }
    )


@pytest.fixture
def temp_dir():
    """Temporary directory for test outputs"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)
