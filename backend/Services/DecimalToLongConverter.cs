using System.Globalization;

namespace backend.Services;

public class DecimalToLongConverter : CsvHelper.TypeConversion.DefaultTypeConverter
{
  public override object ConvertFromString(string? text, CsvHelper.IReaderRow row, CsvHelper.Configuration.MemberMapData memberMapData)
  {
    if (string.IsNullOrEmpty(text))
      return 0L;

    if (decimal.TryParse(text, NumberStyles.Any, CultureInfo.InvariantCulture, out var decimalValue))
    {
      return (long)decimalValue;
    }
    return 0L;
  }
}
