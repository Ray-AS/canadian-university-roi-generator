namespace backend.Models.Policy;

public class BestPractice
{
  public string Field { get; set; } = string.Empty;
  public decimal Roi5yr { get; set; }
  public decimal DebtToIncome { get; set; }
}
