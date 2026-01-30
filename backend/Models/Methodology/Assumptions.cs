using System;

namespace backend.Models.Methodology;

public class Assumptions
{
  public InflationAdjustment InflationAdjustment { get; set; } = new();
  public DebtEstimation DebtEstimation { get; set; } = new();
  public RoiCalculation RoiCalculation { get; set; } = new();
  public PaybackCalculation PaybackCalculation { get; set; } = new();
  public EarningsPerDollar EarningsPerDollar { get; set; } = new();
}
