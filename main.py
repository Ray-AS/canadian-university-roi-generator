from calculation import calculate_roi_by_field
from configs import (
    STAT_CAN_TABLES,
)
from fetch import fetch_statcan_table
from plots import plot_debt_to_income, plot_payback_years, plot_tuition_vs_earnings
from normalization import filter_statcan_data
from preparation import (
    estimate_debt_by_fields,
    merge_dfs,
    prepare_debt_data,
    prepare_earnings_data,
    prepare_enrollment_data,
    prepare_tuition_data,
)

# from mock import make_mock_merged_df


def main():
    tuition_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["tuition"]),
        ["2020/2021", "2021/2022", "2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    prepared_tuition_data = prepare_tuition_data(tuition_data)

    earnings_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["earnings"]),
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        field_of_study_exclude=["Total, field of study"],
    )

    earnings_by_major = (
        earnings_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .mean()
        .reset_index()
    )

    prepared_earnings_data = prepare_earnings_data(earnings_by_major)

    enrollment_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["enrollments"]),
        ["2020/2021", "2021/2022", "2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    enrollment_summary = (
        enrollment_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .sum()
        .reset_index()
    )

    prepared_enrollment_data = prepare_enrollment_data(enrollment_summary)

    debt_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["debt"]),
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        level_of_study_include=["Bachelor's"],
    )

    prepared_debt_data = prepare_debt_data(debt_data)
    debts_by_field = estimate_debt_by_fields(
        prepared_debt_data["debt_2024"].iloc[0], prepared_tuition_data
    )

    merged = merge_dfs(
        prepared_tuition_data,
        prepared_earnings_data,
        prepared_enrollment_data,
        debts_by_field,
    )

    merged_w_roi = calculate_roi_by_field(merged)

    print("-----------------------TUITION-----------------------")
    print(prepared_tuition_data)
    print("-----------------------EARNINGS-----------------------")
    print(prepared_earnings_data)
    print("-----------------------ENROLLMENT-----------------------")
    print(prepared_enrollment_data)
    print("-----------------------DEBT-----------------------")
    print(debts_by_field)
    print(merged_w_roi)
    print(merged_w_roi.columns)

    plot_tuition_vs_earnings(merged_w_roi)
    plot_debt_to_income(merged_w_roi)
    plot_payback_years(merged_w_roi)


if __name__ == "__main__":
    main()
