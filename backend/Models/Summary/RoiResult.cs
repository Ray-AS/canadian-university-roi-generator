namespace backend.Models.Summary;

public class RoiResult
{
  public string Field { get; set; } = string.Empty;
  public decimal Roi5yr { get; set; }
  public decimal AnnualTuition { get; set; }
  public decimal MedianEarnings { get; set; }
}
