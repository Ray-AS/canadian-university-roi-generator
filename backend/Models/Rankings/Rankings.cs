using System.Text.Json.Serialization;

namespace backend.Models.Rankings;

public class Rankings
{
  [JsonPropertyName("by_5yr_roi")]
  public List<RankedField> By5yrRoi { get; set; } = [];
  public List<RankedField> ByEarningsPerDollar { get; set; } = [];
  public List<RankedField> ByDebtToIncome { get; set; } = [];
  public List<RankedField> ByPaybackPeriod { get; set; } = [];
}

