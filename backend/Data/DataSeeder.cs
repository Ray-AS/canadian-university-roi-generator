using backend.Models.Entities;
using backend.Services;

namespace backend.Data;

public class DataSeeder
{
  public static async Task SeedDataAsync(ReportDbContext context, DataService dataService)
  {
    if (context.FieldData.Any()) return;

    var entities = dataService.Table.RoiTable.Select(row => new FieldDataEntity
    {
      Field = row.Field,
      Tuition = row.Tuition,
      Earnings2018 = row.Earnings2018,
      Earnings2024Adjusted = row.Earnings2024Adjusted,
      EstimatedDebt = row.EstimatedDebt,
      Enrollment = row.Enrollment,
      TotalTuition = row.TotalTuition,
      DebtToIncome = row.DebtToIncome,
      PaybackYears = row.PaybackYears,
      Earnings5yr = row.Earnings5yr,
      Roi5yrWithDebt = row.Roi5yrWithDebt,
      Roi5yrWithTuition = row.Roi5yrWithTuition,
      EarningsPerDollarTuition = row.EarningsPerDollarTuition
    }).ToList();

    await context.FieldData.AddRangeAsync(entities);
    await context.SaveChangesAsync();
  }
}
