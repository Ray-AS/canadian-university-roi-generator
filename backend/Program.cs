using backend.Data;
using backend.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

builder.Services.AddDbContext<ReportDbContext>(options =>
{
  options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection"));
});

// Register DataService as Singleton
builder.Services.AddScoped<DataService>();

// Add CORS
builder.Services.AddCors(options =>
{
  options.AddPolicy("AllowAll", policy =>
  {
    policy.AllowAnyOrigin()
            .AllowAnyHeader()
            .AllowAnyMethod();
  });
});

// Add Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
  var context = scope.ServiceProvider.GetRequiredService<ReportDbContext>();
  var dataService = scope.ServiceProvider.GetRequiredService<DataService>();

  context.Database.EnsureCreated();

  await DataSeeder.SeedDataAsync(context, dataService);
}

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
  app.UseSwagger();
  app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();


app.Run();
