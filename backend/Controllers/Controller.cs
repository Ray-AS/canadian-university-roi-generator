using backend.DTOs;
using backend.Services;
using Microsoft.AspNetCore.Mvc;

namespace backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class Controller : ControllerBase
{
  private readonly DataService _service;

  public Controller(DataService service)
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
}
