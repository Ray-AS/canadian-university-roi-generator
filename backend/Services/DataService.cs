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
  private Summary Summary { get; } = new();
  private Rankings Rankings { get; } = new();
  private Analysis Analysis { get; } = new();
  private Methodology Methodology { get; } = new();
  private PolicyRecommendations PolicyRecommendations { get; } = new();
  private VisualizationsDetails Visualizations { get; } = new();
  private Table Table { get; } = new();
}
