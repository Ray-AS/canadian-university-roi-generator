namespace backend.Models.Methodology;

public class Methodology
{
  public List<string> DataSources { get; set; } = new();
  public Assumptions Assumptions { get; set; } = new();
  public List<string> Limitations { get; set; } = new();
  public DataYears DataYears { get; set; } = new();
}
