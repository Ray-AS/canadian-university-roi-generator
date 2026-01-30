namespace backend.Models.Policy;

public class Recommendations
{
  public List<string> HighEnrollmentLowRoiFields { get; set; } = new();
  public List<string> HighDebtBurdenFields { get; set; } = new();
  public List<string> SystemWide { get; set; } = new();
}
