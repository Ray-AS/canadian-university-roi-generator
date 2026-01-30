using backend.Models.Entities;
using Microsoft.EntityFrameworkCore;

namespace backend.Data;

public class ReportDbContext : DbContext
{
  public ReportDbContext(DbContextOptions<ReportDbContext> options) : base(options)
  {
  }

  public DbSet<FieldDataEntity> FieldData { get; set; }

  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    base.OnModelCreating(modelBuilder);

    // EF Core configuration for data in entity on build
    modelBuilder.Entity<FieldDataEntity>(entity =>
    {
      entity.HasKey(e => e.Id);
      entity.HasIndex(e => e.Field).IsUnique();

      entity.Property(e => e.Tuition).HasPrecision(18, 2);
      entity.Property(e => e.Earnings2018).HasPrecision(18, 2);
      entity.Property(e => e.Earnings2024Adjusted).HasPrecision(18, 2);
      entity.Property(e => e.EstimatedDebt).HasPrecision(18, 2);
      entity.Property(e => e.TotalTuition).HasPrecision(18, 2);
      entity.Property(e => e.DebtToIncome).HasPrecision(18, 4);
      entity.Property(e => e.PaybackYears).HasPrecision(18, 2);
      entity.Property(e => e.Earnings5yr).HasPrecision(18, 2);
      entity.Property(e => e.Roi5yrWithDebt).HasPrecision(18, 4);
      entity.Property(e => e.Roi5yrWithTuition).HasPrecision(18, 4);
      entity.Property(e => e.EarningsPerDollarTuition).HasPrecision(18, 4);
    });
  }
}
