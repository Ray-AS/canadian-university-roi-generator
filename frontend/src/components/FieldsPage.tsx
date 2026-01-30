import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllFields } from '../api';
import { type FieldData } from '../models';
import { formatCurrency, formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function FieldsPage() {
  const styles = {
    container: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px',
    },
    title: {
      fontSize: '2.5rem',
      marginBottom: '30px',
      textAlign: 'center' as const,
    },
    controls: {
      marginBottom: '30px',
      textAlign: 'center' as const,
    },
    label: {
      fontSize: '1.1rem',
      fontWeight: 'bold' as const,
    },
    select: {
      marginLeft: '10px',
      padding: '8px 15px',
      fontSize: '1rem',
      borderRadius: '4px',
      border: '1px solid #ddd',
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
      gap: '20px',
    },
    card: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      cursor: 'pointer',
      transition: 'transform 0.2s, box-shadow 0.2s',
    },
    cardTitle: {
      fontSize: '1.3rem',
      marginBottom: '15px',
      color: '#333',
      borderBottom: '2px solid #007bff',
      paddingBottom: '10px',
    },
    metric: {
      display: 'flex',
      justifyContent: 'space-between',
      padding: '8px 0',
      borderBottom: '1px solid #f0f0f0',
    },
    metricLabel: {
      color: '#666',
      fontSize: '0.95rem',
    },
    metricValue: {
      fontWeight: 'bold' as const,
      color: '#333',
    },
    enrollmentBadge: {
      marginTop: '15px',
      padding: '8px',
      backgroundColor: '#e9ecef',
      borderRadius: '4px',
      textAlign: 'center' as const,
      fontSize: '0.9rem',
      color: '#495057',
    },
  };

  const [fields, setFields] = useState<FieldData[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'roi' | 'tuition' | 'earnings' | 'payback'>('roi');
  const navigate = useNavigate();

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

  const sortedFields = [...fields].sort((a, b) => {
    switch (sortBy) {
      case 'roi':
        return b.roi5yrWithTuition - a.roi5yrWithTuition;
      case 'tuition':
        return a.tuition - b.tuition;
      case 'earnings':
        return b.earnings2024Adjusted - a.earnings2024Adjusted;
      case 'payback':
        return a.paybackYears - b.paybackYears;
      default:
        return 0;
    }
  });

  if (loading) return <LoadingSpinner />;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>All Fields of Study</h1>
      
      <div style={styles.controls}>
        <label style={styles.label}>
          Sort by:{' '}
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value as 'roi' | 'tuition' | 'earnings' | 'payback')}
            style={styles.select}
          >
            <option value="roi">Highest ROI</option>
            <option value="tuition">Lowest Tuition</option>
            <option value="earnings">Highest Earnings</option>
            <option value="payback">Fastest Payback</option>
          </select>
        </label>
      </div>

      <div style={styles.grid}>
        {sortedFields.map((field) => (
          <div 
            key={field.id} 
            style={styles.card}
            onClick={() => navigate(`/fields/${field.field}`)}
          >
            <h3 style={styles.cardTitle}>{formatFieldName(field.field)}</h3>
            
            <div style={styles.metric}>
              <span style={styles.metricLabel}>Annual Tuition:</span>
              <span style={styles.metricValue}>{formatCurrency(field.tuition)}</span>
            </div>

            <div style={styles.metric}>
              <span style={styles.metricLabel}>Earnings (Yr 2):</span>
              <span style={styles.metricValue}>{formatCurrency(field.earnings2024Adjusted)}</span>
            </div>

            <div style={styles.metric}>
              <span style={styles.metricLabel}>5-Year ROI:</span>
              <span style={{...styles.metricValue, color: '#28a745'}}>{field.roi5yrWithTuition.toFixed(2)}x</span>
            </div>

            <div style={styles.metric}>
              <span style={styles.metricLabel}>Payback Period:</span>
              <span style={styles.metricValue}>{field.paybackYears.toFixed(1)} years</span>
            </div>

            <div style={styles.metric}>
              <span style={styles.metricLabel}>Debt/Income:</span>
              <span style={styles.metricValue}>{field.debtToIncome.toFixed(2)}x</span>
            </div>

            <div style={styles.enrollmentBadge}>
              {field.enrollment.toLocaleString()} students
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
