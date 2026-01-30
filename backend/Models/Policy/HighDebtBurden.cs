namespace backend.Models.Policy;

public class HighDebtBurden
{
  public string Field { get; set; } = string.Empty;
  public decimal DebtToIncome { get; set; }
  public decimal PaybackYears { get; set; }
}
