namespace backend.Models.Analysis;

public class FieldAnalysis
{
  public string Field { get; set; } = string.Empty;
  public string FieldDisplayName { get; set; } = string.Empty;
  public FinancialMetrics FinancialMetrics { get; set; } = new();
  public RoiMetrics RoiMetrics { get; set; } = new();
  public DebtBurden DebtBurden { get; set; } = new();
  public int Enrollment { get; set; }
}
