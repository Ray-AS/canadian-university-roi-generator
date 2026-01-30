namespace backend.Models.Summary;

public class PaybackResult
{
  public string Field { get; set; } = string.Empty;
  public decimal PaybackYears { get; set; }
  public decimal DebtToIncome { get; set; }
}
