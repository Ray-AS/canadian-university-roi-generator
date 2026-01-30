using System.Text.Json.Serialization;

namespace backend.Models.Methodology;

public class InflationAdjustment
{
  [JsonPropertyName("cpi_2018_to_2024")]
  public decimal Cpi2018To2024 { get; set; }
  [JsonPropertyName("cpi_2020_to_2024")]
  public decimal Cpi2020To2024 { get; set; }
}