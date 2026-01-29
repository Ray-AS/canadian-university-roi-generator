from pathlib import Path
import shutil
import tempfile
import numpy as np
import pandas as pd
import pytest

from calculation import calculate_roi_by_field
from normalization import normalize_ref_date
from plots import generate_all_plots
from report import generate_report


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


class TestCalculations:
    def test_normalize_ref_date_converts_academic_year(self):
        df = pd.DataFrame({"REF_DATE": ["2020/2021"]})
        result = normalize_ref_date(df)
        assert result["REF_DATE"].iloc[0] == 2020
        assert result["REF_DATE"].dtype == np.int64

    def test_calculate_roi_adds_required_columns(self, sample_data):
        result = calculate_roi_by_field(sample_data)

        required = [
            "roi_5yr_w_tuition",
            "roi_5yr_w_debt",
            "debt_to_income",
            "payback_years",
            "earnings_per_dollar_tuition",
        ]

        for col in required:
            assert col in result.columns

    def test_roi_values_are_positive(self, sample_data):
        result = calculate_roi_by_field(sample_data)

        assert (result["roi_5yr_w_tuition"] > 0).all()
        assert (result["roi_5yr_w_debt"] > 0).all()
        assert (result["payback_years"] > 0).all()

    def test_known_roi_calculation(self):
        df = pd.DataFrame(
            {
                "field": ["test"],
                "tuition": [10000],
                "earnings_2024_adjusted": [50000],
                "estimated_debt": [40000],
                "enrollment": [1000000],
                "total_tuition": [40000],
            }
        )

        result = calculate_roi_by_field(df)

        expected = 5.6
        actual = result["roi_5yr_w_tuition"].iloc[0]

        assert abs(actual - expected) / expected < 0.1


class TestOutputs:
    def test_all_plots_generated(self, complete_data, temp_dir):
        generate_all_plots(complete_data, temp_dir)

        plots = [
            "tuition_vs_earnings.png",
            "roi_by_field.png",
            "debt_to_income_ratio.png",
            "payback_years.png",
        ]

        for plot in plots:
            path = temp_dir / plot
            assert path.exists()

    def test_report_file_generated(self, complete_data, temp_dir):
        generate_report(complete_data, temp_dir)

        md_path = temp_dir / "REPORT.md"

        assert md_path.exists()
