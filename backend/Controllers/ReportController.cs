using backend.DTOs;
using backend.Models.Analysis;
using backend.Models.Methodology;
using backend.Models.Policy;
using backend.Models.Rankings;
using backend.Models.Summary;
using backend.Models.Table;
using backend.Models.VisualizationsDetails;
using backend.Services;
using Microsoft.AspNetCore.Mvc;

namespace backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ReportController : ControllerBase
{
  private readonly DataService _service;

  public ReportController(DataService service)
  {
    _service = service;
  }

  [HttpGet]
  public ActionResult<CompleteReportDto> GetReport()
  {
    CompleteReportDto completeReport = new CompleteReportDto(
      _service.Summary,
      _service.Rankings,
      _service.Analysis,
      _service.Methodology,
      _service.PolicyRecommendations,
      _service.Visualizations,
      _service.Table
    );

    return completeReport;
  }

  [HttpGet("summary")]
  public ActionResult<Summary> GetSummary()
  {
    return _service.Summary is null ? NotFound() : Ok(_service.Summary);
  }

  [HttpGet("rankings")]
  public ActionResult<Rankings> GetRankings()
  {
    return _service.Rankings is null ? NotFound() : Ok(_service.Rankings);
  }

  [HttpGet("analysis/{fieldName}")]
  public ActionResult<FieldAnalysis> GetAnalysis(string fieldName)
  {
    var fieldAnalysis = _service.Analysis.Fields.Find(field => field.Field == fieldName);

    return fieldAnalysis is null ? NotFound() : Ok(fieldAnalysis);
  }

  [HttpGet("analysis")]
  public ActionResult<Analysis> GetAnalysis()
  {
    return _service.Analysis is null ? NotFound() : Ok(_service.Analysis);
  }

  [HttpGet("methodology")]
  public ActionResult<Methodology> GetMethodology()
  {
    return _service.Methodology is null ? NotFound() : Ok(_service.Methodology);
  }

  [HttpGet("recommendations")]
  public ActionResult<PolicyRecommendations> GetPolicyRecommendations()
  {
    return _service.PolicyRecommendations is null ? NotFound() : Ok(_service.PolicyRecommendations);
  }

  [HttpGet("visualizations")]
  public ActionResult<VisualizationsDetails> GetVisualizations()
  {
    return _service.Visualizations is null ? NotFound() : Ok(_service.Visualizations);
  }

  [HttpGet("table")]
  public ActionResult<Table> GetTable()
  {
    return _service.Table is null ? NotFound() : Ok(_service.Table);
  }
}
