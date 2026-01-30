using System.Text.Json;
using backend.Models.Analysis;
using backend.Models.Methodology;
using backend.Models.Policy;
using backend.Models.Rankings;
using backend.Models.Summary;
using backend.Models.Table;
using backend.Models.VisualizationsDetails;
using CsvHelper;
using System.Globalization;

namespace backend.Services;

public class DataService
{
  private string BasePath { get; } = "../../reports";
  public Summary Summary { get; private set; } = new();
  public Rankings Rankings { get; private set; } = new();
  public Analysis Analysis { get; private set; } = new();
  public Methodology Methodology { get; private set; } = new();
  public PolicyRecommendations PolicyRecommendations { get; private set; } = new();
  public VisualizationsDetails Visualizations { get; private set; } = new();
  public Table Table { get; private set; } = new();

  public DataService()
  {
    LoadJsonData();
    LoadCsvData();
  }

  private void LoadJsonData()
  {
    var options = new JsonSerializerOptions
    {
      PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
      PropertyNameCaseInsensitive = true
    };

    var tempSummary = JsonSerializer.Deserialize<Summary>(File.ReadAllText(Path.Combine(BasePath, "summary.json")), options);
    var tempRankings = JsonSerializer.Deserialize<Rankings>(File.ReadAllText(Path.Combine(BasePath, "rankings.json")), options);
    var tempAnalysis = JsonSerializer.Deserialize<Analysis>(File.ReadAllText(Path.Combine(BasePath, "analysis.json")), options);
    var tempMethodology = JsonSerializer.Deserialize<Methodology>(File.ReadAllText(Path.Combine(BasePath, "methodology.json")), options);
    var tempPolicyRecommendations = JsonSerializer.Deserialize<PolicyRecommendations>(File.ReadAllText(Path.Combine(BasePath, "policy_recommendations.json")), options);
    var tempVisualizations = JsonSerializer.Deserialize<VisualizationsDetails>(File.ReadAllText(Path.Combine(BasePath, "visualizations.json")), options);

    if (tempSummary is null || tempRankings is null || tempAnalysis is null || tempMethodology is null || tempPolicyRecommendations is null || tempVisualizations is null) throw new FileNotFoundException("Problem loading json data.");

    Summary = tempSummary;
    Rankings = tempRankings;
    Analysis = tempAnalysis;
    Methodology = tempMethodology;
    PolicyRecommendations = tempPolicyRecommendations;
    Visualizations = tempVisualizations;
  }

  private void LoadCsvData()
  {
    var csvPath = Path.Combine(BasePath, "roi_table.csv");

    using var reader = new StreamReader(csvPath);
    using var csv = new CsvReader(reader);

    csv.Configuration.CultureInfo = CultureInfo.InvariantCulture;
    csv.Configuration.HasHeaderRecord = true;

    csv.Configuration.RegisterClassMap<TableRowMap>();

    var rows = csv.GetRecords<TableRow>().ToList();
    Table = new Table { RoiTable = rows };
  }
}
