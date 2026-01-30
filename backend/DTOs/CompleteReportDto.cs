using backend.Models.Analysis;
using backend.Models.Methodology;
using backend.Models.Policy;
using backend.Models.Rankings;
using backend.Models.Summary;
using backend.Models.Table;
using backend.Models.VisualizationsDetails;

namespace backend.DTOs;

public record CompleteReportDto(
  Summary Summary,
  Rankings Rankings,
  Analysis Analysis,
  Methodology Methodology,
  PolicyRecommendations PolicyRecommendations,
  VisualizationsDetails Visualizations,
  Table Table
);