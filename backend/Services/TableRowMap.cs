using backend.Models.Table;
using CsvHelper.Configuration;

namespace backend.Services;

public class TableRowMap : ClassMap<TableRow>
{
  public TableRowMap()
  {
    Map(m => m.Field).Name("field");
    Map(m => m.Tuition).Name("tuition");
    Map(m => m.Earnings2018).Name("earnings_2018");
    Map(m => m.Earnings2024Adjusted).Name("earnings_2024_adjusted");
    Map(m => m.EstimatedDebt).Name("estimated_debt");
    Map(m => m.Enrollment).Name("enrollment").TypeConverter<DecimalToLongConverter>();
    Map(m => m.TotalTuition).Name("total_tuition");
    Map(m => m.DebtToIncome).Name("debt_to_income");
    Map(m => m.PaybackYears).Name("payback_years");
    Map(m => m.Earnings5yr).Name("earnings_5yr");
    Map(m => m.Roi5yrWithDebt).Name("roi_5yr_w_debt");
    Map(m => m.Roi5yrWithTuition).Name("roi_5yr_w_tuition");
    Map(m => m.EarningsPerDollarTuition).Name("earnings_per_dollar_tuition");
  }
}
