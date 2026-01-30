namespace backend.Models.Methodology;

public class PaybackCalculation
{
  public decimal IncomeToDebtRepayment { get; set; }
  public decimal TaxRate { get; set; }
  public decimal InterestRate { get; set; }
  public string Formula { get; set; } = string.Empty;
}
