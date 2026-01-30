namespace backend.Models.Analysis;

public class RoiMetrics
{
  public decimal EarningsPerDollarTuition { get; set; }
  public Comparison EarningsPerDollarComparison { get; set; }
  public decimal Roi5yrTuition { get; set; }
  public Comparison RoiTuitionComparison { get; set; }
  public decimal Roi5YrDebt { get; set; }
}
