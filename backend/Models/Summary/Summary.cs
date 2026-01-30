namespace backend.Models.Summary;

public class Summary
{
  public string ReportDate { get; set; } = string.Empty;
  public OverallAverages OverallAverages { get; set; } = new();
  public BestPerforming BestPerforming { get; set; } = new();
}
