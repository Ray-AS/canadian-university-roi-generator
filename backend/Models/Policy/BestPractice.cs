using System.Text.Json.Serialization;

namespace backend.Models.Policy;

public class BestPractice
{
  public string Field { get; set; } = string.Empty;
  [JsonPropertyName("roi_5yr")]
  public decimal Roi5yr { get; set; }
  public decimal DebtToIncome { get; set; }
}
