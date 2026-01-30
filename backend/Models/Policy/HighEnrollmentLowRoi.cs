using System.Text.Json.Serialization;

namespace backend.Models.Policy;

public class HighEnrollmentLowRoi
{
  public string Field { get; set; } = string.Empty;
  public int Enrollment { get; set; }
  [JsonPropertyName("roi_5yr")]
  public decimal Roi5yr { get; set; }
}
