namespace backend.Models.Methodology;

public class RoiCalculation
{
  public decimal EarningsGrowth { get; set; }
  public string BasePeriod { get; set; } = string.Empty;
  public string TuitionRoiFormula { get; set; } = string.Empty;
  public string DebtRoiFormula { get; set; } = string.Empty;
}
