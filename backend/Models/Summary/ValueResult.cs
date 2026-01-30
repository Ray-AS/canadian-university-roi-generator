namespace backend.Models.Summary;

public class ValueResult
{
  public string Field { get; set; } = string.Empty;
  public decimal EarningsPerDollar { get; set; }
  public decimal AnnualTuition { get; set; }
  public decimal MedianEarnings { get; set; }
}
