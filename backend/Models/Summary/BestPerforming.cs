namespace backend.Models.Summary;

public class BestPerforming
{
  public RoiResult HighestRoi { get; set; } = new();
  public ValueResult BestValue { get; set; } = new();
  public PaybackResult FastestPayback { get; set; } = new();
}
