namespace backend.Models.Policy;

public class AreasRequiringAttention
{
  public List<HighEnrollmentLowRoi> HighEnrollmentLowRoi { get; set; } = new();
  public List<HighDebtBurden> HighDebtBurden { get; set; } = new();
}
