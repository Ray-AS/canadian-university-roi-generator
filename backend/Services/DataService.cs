using System.Text.Json;
using backend.Models.Analysis;
using backend.Models.Methodology;
using backend.Models.Policy;
using backend.Models.Rankings;
using backend.Models.Summary;
using backend.Models.Table;
using backend.Models.VisualizationsDetails;

namespace backend.Services;

public class DataService
{
  private string BasePath { get; } = "../../reports";
  private Summary Summary { get; set; } = new();
  private Rankings Rankings { get; set; } = new();
  private Analysis Analysis { get; set; } = new();
  private Methodology Methodology { get; set; } = new();
  private PolicyRecommendations PolicyRecommendations { get; set; } = new();
  private VisualizationsDetails Visualizations { get; set; } = new();
  private Table Table { get; set; } = new();

  private void LoadJsonData()
  {
    var options = new JsonSerializerOptions
    {
      PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
    };

    var tempSummary = JsonSerializer.Deserialize<Summary>(File.ReadAllText(Path.Combine(BasePath, "summary.json")));
    var tempRankings = JsonSerializer.Deserialize<Rankings>(File.ReadAllText(Path.Combine(BasePath, "rankings.json")));
    var tempAnalysis = JsonSerializer.Deserialize<Analysis>(File.ReadAllText(Path.Combine(BasePath, "analysis.json")));
    var tempMethodology = JsonSerializer.Deserialize<Methodology>(File.ReadAllText(Path.Combine(BasePath, "methodology.json")));
    var tempPolicyRecommendations = JsonSerializer.Deserialize<PolicyRecommendations>(File.ReadAllText(Path.Combine(BasePath, "policy_recommendations.json")));
    var tempVisualizations = JsonSerializer.Deserialize<VisualizationsDetails>(File.ReadAllText(Path.Combine(BasePath, "visualizations.json")));

    if (tempSummary is null || tempRankings is null || tempAnalysis is null || tempMethodology is null || tempPolicyRecommendations is null || tempVisualizations is null) throw new FileNotFoundException("Problem loading json data.");

    Summary = tempSummary;
    Rankings = tempRankings;
    Analysis = tempAnalysis;
    Methodology = tempMethodology;
    PolicyRecommendations = tempPolicyRecommendations;
    Visualizations = tempVisualizations;
  }
}
