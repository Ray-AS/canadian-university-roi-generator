namespace backend.Models.Entities;

public class FieldDataEntity
{
  public int Id { get; set; }
  public string Field { get; set; } = string.Empty;
  public decimal Tuition { get; set; }
  public decimal Earnings2018 { get; set; }
  public decimal Earnings2024Adjusted { get; set; }
  public decimal EstimatedDebt { get; set; }
  public long Enrollment { get; set; }
  public decimal TotalTuition { get; set; }
  public decimal DebtToIncome { get; set; }
  public decimal PaybackYears { get; set; }
  public decimal Earnings5yr { get; set; }
  public decimal Roi5yrWithDebt { get; set; }
  public decimal Roi5yrWithTuition { get; set; }
  public decimal EarningsPerDollarTuition { get; set; }
  public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
