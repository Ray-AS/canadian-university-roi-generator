namespace backend.Models.Summary;

public class AreasOfConcern
{
  public RoiResult LowestRoi { get; set; } = new();
  public ValueResult LowestValue { get; set; } = new();
  public PaybackResult SlowestPayback { get; set; } = new();
}
