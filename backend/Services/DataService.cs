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
using CsvHelper.Configuration;
using backend.Data;
using backend.Models.Entities;
using Microsoft.EntityFrameworkCore;

namespace backend.Services;

public class DataService
{
  private readonly ReportDbContext? _context;
  // Report data (i.e. .json and .csv) are output but python service in /reports dir in root of project
  private string BasePath { get; } = "../reports";
  public Summary Summary { get; private set; } = new();
  public Rankings Rankings { get; private set; } = new();
  public Analysis Analysis { get; private set; } = new();
  public Methodology Methodology { get; private set; } = new();
  public PolicyRecommendations PolicyRecommendations { get; private set; } = new();
  public VisualizationsDetails Visualizations { get; private set; } = new();
  public Table Table { get; private set; } = new();

  public DataService(ReportDbContext context)
  {
    _context = context;
    LoadJsonData();
    LoadCsvData();
  }

  // public DataService()
  // {
  //   LoadJsonData();
  //   LoadCsvData();
  // }

  // TODO: Move async query functions to separate class
  // Return all field data
  public async Task<IEnumerable<FieldDataEntity>> GetAllFieldsAsync()
  {
    if (_context == null) return new List<FieldDataEntity>();
    return await _context.FieldData.ToListAsync();
  }

  // Return a single field's data
  public async Task<FieldDataEntity?> GetFieldByNameAsync(string fieldName)
  {
    if (_context == null) return null;
    return await _context.FieldData
        .FirstOrDefaultAsync(f => f.Field == fieldName);
  }

  // Read .json files from /reports dir and store in-memory
  private void LoadJsonData()
  {
    // Ensure key names match C# models (need to manually define JsonPropertyNames for keys with numbers in them in the C# models)
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

    // Throw error if any expected .json files don't exist
    if (tempSummary is null || tempRankings is null || tempAnalysis is null || tempMethodology is null || tempPolicyRecommendations is null || tempVisualizations is null) throw new FileNotFoundException("Problem loading json data.");

    Summary = tempSummary;
    Rankings = tempRankings;
    Analysis = tempAnalysis;
    Methodology = tempMethodology;
    PolicyRecommendations = tempPolicyRecommendations;
    Visualizations = tempVisualizations;
  }

  // Read .csv files from /reports dir and store in-memory (also will be used to seed db)
  private void LoadCsvData()
  {
    var csvPath = Path.Combine(BasePath, "roi_table.csv");

    var config = new CsvConfiguration(CultureInfo.InvariantCulture)
    {
      HasHeaderRecord = true,
    };

    using var reader = new StreamReader(csvPath);
    using var csv = new CsvReader(reader, config);

    csv.Context.RegisterClassMap<TableRowMap>();
    var rows = csv.GetRecords<TableRow>().ToList();

    Table = new Table { RoiTable = rows };
  }
}
