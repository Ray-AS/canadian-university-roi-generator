namespace backend.Models.Policy;

public class PolicyRecommendations
{
  public AreasRequiringAttention AreasRequiringAttention { get; set; } = new();
  public List<BestPractice> BestPractices { get; set; } = new();
  public Recommendations Recommendations { get; set; } = new();
}
