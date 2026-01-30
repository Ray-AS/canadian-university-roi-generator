namespace backend.Models.Policy;

public class HighEnrollmentLowRoi
{
  public string Field { get; set; } = string.Empty;
  public int Enrollment { get; set; }
  public decimal Roi5yr { get; set; }
}
