import { useEffect, useState } from 'react';
import { getAllFields } from '../api';
import { type FieldData } from '../models';
import { formatCurrency, formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function TablePage() {
  const styles = {
    container: {
      maxWidth: '1600px',
      margin: '0 auto',
      padding: '20px',
    },
    title: {
      fontSize: '2.5rem',
      marginBottom: '10px',
      textAlign: 'center' as const,
    },
    subtitle: {
      textAlign: 'center' as const,
      color: '#666',
      marginBottom: '30px',
      fontSize: '1.1rem',
    },
    tableContainer: {
      overflowX: 'auto' as const,
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse' as const,
      fontSize: '0.9rem',
    },
    headerRow: {
      backgroundColor: '#007bff',
      color: 'white',
    },
    th: {
      padding: '15px 10px',
      textAlign: 'left' as const,
      fontWeight: 'bold' as const,
      cursor: 'pointer',
      userSelect: 'none' as const,
      whiteSpace: 'nowrap' as const,
    },
    row: {
      borderBottom: '1px solid #e9ecef',
    },
    td: {
      padding: '12px 10px',
      whiteSpace: 'nowrap' as const,
    },
    tdNumber: {
      padding: '12px 10px',
      textAlign: 'right' as const,
      whiteSpace: 'nowrap' as const,
    },
    legend: {
      marginTop: '30px',
      padding: '25px',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    },
    legendList: {
      lineHeight: '2',
      paddingLeft: '20px',
      marginTop: '15px',
    },
  };

  const [fields, setFields] = useState<FieldData[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof FieldData;
    direction: 'asc' | 'desc';
  }>({ key: 'roi5yrWithTuition', direction: 'desc' });

  useEffect(() => {
    loadFields();
  }, []);

  const loadFields = async () => {
    try {
      setLoading(true);
      const data = await getAllFields();
      console.log(data);
      setFields(data);
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (key: keyof FieldData) => {
    let direction: 'asc' | 'desc' = 'desc';
    if (sortConfig.key === key && sortConfig.direction === 'desc') {
      direction = 'asc';
    }
    setSortConfig({ key, direction });
  };

  const sortedFields = [...fields].sort((a, b) => {
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortConfig.direction === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
    }

    return 0;
  });

  const getSortIndicator = (key: keyof FieldData) => {
    if (sortConfig.key !== key) return ' ↕️';
    return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Complete Data Table</h1>
      <p style={styles.subtitle}>
        Comprehensive metrics for all fields of study (click column headers to sort)
      </p>

      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.headerRow}>
              <th style={styles.th} onClick={() => handleSort('field')}>
                Field{getSortIndicator('field')}
              </th>
              <th style={styles.th} onClick={() => handleSort('tuition')}>
                Annual Tuition{getSortIndicator('tuition')}
              </th>
              <th style={styles.th} onClick={() => handleSort('estimatedDebt')}>
                Total Debt{getSortIndicator('estimatedDebt')}
              </th>
              <th style={styles.th} onClick={() => handleSort('earnings2024Adjusted')}>
                Earnings (Yr 2){getSortIndicator('earnings2024Adjusted')}
              </th>
              <th style={styles.th} onClick={() => handleSort('roi5yrWithTuition')}>
                ROI (Tuition){getSortIndicator('roi5yrWithTuition')}
              </th>
              <th style={styles.th} onClick={() => handleSort('roi5yrWithDebt')}>
                ROI (Debt){getSortIndicator('roi5yrWithDebt')}
              </th>
              <th style={styles.th} onClick={() => handleSort('debtToIncome')}>
                Debt/Income{getSortIndicator('debtToIncome')}
              </th>
              <th style={styles.th} onClick={() => handleSort('paybackYears')}>
                Payback{getSortIndicator('paybackYears')}
              </th>
              <th style={styles.th} onClick={() => handleSort('earningsPerDollarTuition')}>
                $/$ Tuition{getSortIndicator('earningsPerDollarTuition')}
              </th>
              <th style={styles.th} onClick={() => handleSort('enrollment')}>
                Enrollment{getSortIndicator('enrollment')}
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedFields.map((field) => (
              <tr key={field.id} style={styles.row}>
                <td style={styles.td}>{formatFieldName(field.field)}</td>
                <td style={styles.tdNumber}>{formatCurrency(field.tuition)}</td>
                <td style={styles.tdNumber}>{formatCurrency(field.estimatedDebt)}</td>
                <td style={styles.tdNumber}>{formatCurrency(field.earnings2024Adjusted)}</td>
                <td style={{...styles.tdNumber, color: '#28a745', fontWeight: 'bold'}}>
                  {field.roi5yrWithTuition.toFixed(2)}x
                </td>
                <td style={{...styles.tdNumber, color: '#28a745'}}>
                  {field.roi5yrWithDebt.toFixed(2)}x
                </td>
                <td style={styles.tdNumber}>{field.debtToIncome.toFixed(2)}x</td>
                <td style={styles.tdNumber}>{field.paybackYears.toFixed(1)} yrs</td>
                <td style={styles.tdNumber}>${field.earningsPerDollarTuition.toFixed(2)}</td>
                <td style={styles.tdNumber}>{field.enrollment.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={styles.legend}>
        <h3>Column Definitions</h3>
        <ul style={styles.legendList}>
          <li><strong>Annual Tuition:</strong> Average tuition cost per year</li>
          <li><strong>Total Debt:</strong> Estimated debt after 4 years</li>
          <li><strong>Earnings (Yr 2):</strong> Median earnings 2 years after graduation (2024 adjusted)</li>
          <li><strong>ROI (Tuition):</strong> 5-year return on investment based on tuition costs</li>
          <li><strong>ROI (Debt):</strong> 5-year return on investment based on debt incurred</li>
          <li><strong>Debt/Income:</strong> Ratio of total debt to annual earnings</li>
          <li><strong>Payback:</strong> Years to repay debt at 10% of post-tax income</li>
          <li><strong>$/$ Tuition:</strong> Earnings per dollar of tuition invested</li>
          <li><strong>Enrollment:</strong> Total students enrolled in this field</li>
        </ul>
      </div>
    </div>
  );
};
