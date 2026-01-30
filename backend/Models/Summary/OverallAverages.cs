using System.Text.Json.Serialization;

namespace backend.Models.Summary;

public class OverallAverages
{
  public decimal AvgAnnualTuition { get; set; }
  public decimal AvgTotalDebt { get; set; }
  [JsonPropertyName("avg_earnings_year_2")]
  public decimal AvgEarningsYear2 { get; set; }
  [JsonPropertyName("avg_5yr_roi")]
  public decimal Avg5yrRoi { get; set; }
  public decimal AvgPaybackPeriodYears { get; set; }
}
