using System.Text.Json.Serialization;

namespace backend.Models.Analysis;

public class FinancialMetrics
{
  public decimal AnnualTuition { get; set; }
  [JsonPropertyName("total_4yr_tuition")]
  public decimal Total4yrTuition { get; set; }
  public decimal EstimatedDebt { get; set; }
  [JsonPropertyName("median_earnings_year_2")]
  public decimal MedianEarningsYear2 { get; set; }
}
