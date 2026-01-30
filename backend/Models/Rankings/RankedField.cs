namespace backend.Models.Rankings;

public class RankedField
{
  public int Rank { get; set; }
  public string Field { get; set; } = string.Empty;
  public decimal Value { get; set; }
}
