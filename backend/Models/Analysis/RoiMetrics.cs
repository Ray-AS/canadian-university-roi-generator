using System.Text.Json.Serialization;

namespace backend.Models.Analysis;

public class RoiMetrics
{
  public decimal EarningsPerDollarTuition { get; set; }
  public string EarningsPerDollarComparison { get; set; } = string.Empty;
  [JsonPropertyName("roi_5yr_tuition")]
  public decimal Roi5yrTuition { get; set; }
  public string RoiTuitionComparison { get; set; } = string.Empty;
  [JsonPropertyName("roi_5yr_debt")]
  public decimal Roi5YrDebt { get; set; }
}
