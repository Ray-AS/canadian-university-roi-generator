import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getFieldByName } from '../api';
import { type FieldData } from '../models';
import { formatCurrency, formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function FieldDetailPage() {
  const styles = {
    container: {
      maxWidth: '1000px',
      margin: '0 auto',
      padding: '20px',
    },
    backButton: {
      padding: '10px 20px',
      marginBottom: '20px',
      backgroundColor: '#6c757d',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontSize: '1rem',
    },
    title: {
      fontSize: '2.5rem',
      marginBottom: '30px',
      textAlign: 'center' as const,
      color: '#333',
    },
    content: {
      backgroundColor: 'white',
      padding: '30px',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    },
    section: {
      marginBottom: '40px',
    },
    sectionTitle: {
      fontSize: '1.5rem',
      marginBottom: '20px',
      color: '#007bff',
      borderBottom: '2px solid #007bff',
      paddingBottom: '10px',
    },
    metricsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '15px',
    },
    metricCard: {
      padding: '20px',
      backgroundColor: '#f8f9fa',
      borderRadius: '6px',
      textAlign: 'center' as const,
    },
    metricLabel: {
      fontSize: '0.9rem',
      color: '#666',
      marginBottom: '10px',
    },
    metricValue: {
      fontSize: '1.5rem',
      fontWeight: 'bold' as const,
      color: '#333',
    },
    enrollmentCard: {
      padding: '30px',
      backgroundColor: '#e7f3ff',
      borderRadius: '8px',
      textAlign: 'center' as const,
    },
    enrollmentValue: {
      fontSize: '3rem',
      fontWeight: 'bold' as const,
      color: '#007bff',
    },
    enrollmentLabel: {
      fontSize: '1.2rem',
      color: '#666',
      marginTop: '10px',
    },
  };

  const { fieldName } = useParams<{ fieldName: string }>();
  const navigate = useNavigate();
  const [field, setField] = useState<FieldData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (fieldName) {
      loadField(fieldName);
    }
  }, [fieldName]);

  const loadField = async (name: string) => {
    try {
      setLoading(true);
      const data = await getFieldByName(name);
      console.log(data);
      setField(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!field) return null;

  return (
    <div style={styles.container}>
      <button onClick={() => navigate('/fields')} style={styles.backButton}>
        ← Back to All Fields
      </button>

      <h1 style={styles.title}>{formatFieldName(field.field)}</h1>

      <div style={styles.content}>
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Financial Metrics</h2>
          <div style={styles.metricsGrid}>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Annual Tuition</div>
              <div style={styles.metricValue}>{formatCurrency(field.tuition)}</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Total 4-Year Tuition</div>
              <div style={styles.metricValue}>{formatCurrency(field.totalTuition)}</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Estimated Debt</div>
              <div style={styles.metricValue}>{formatCurrency(field.estimatedDebt)}</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Median Earnings (Year 2)</div>
              <div style={styles.metricValue}>{formatCurrency(field.earnings2024Adjusted)}</div>
            </div>
          </div>
        </div>

        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Return on Investment</h2>
          <div style={styles.metricsGrid}>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>5-Year ROI (Tuition)</div>
              <div style={{...styles.metricValue, color: '#28a745'}}>{field.roi5yrWithTuition.toFixed(2)}x</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>5-Year ROI (Debt)</div>
              <div style={{...styles.metricValue, color: '#28a745'}}>{field.roi5yrWithDebt.toFixed(2)}x</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Earnings per Dollar</div>
              <div style={styles.metricValue}>${field.earningsPerDollarTuition.toFixed(2)}</div>
            </div>
          </div>
        </div>

        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Debt Burden</h2>
          <div style={styles.metricsGrid}>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Debt-to-Income Ratio</div>
              <div style={styles.metricValue}>{field.debtToIncome.toFixed(2)}x</div>
            </div>
            <div style={styles.metricCard}>
              <div style={styles.metricLabel}>Payback Period</div>
              <div style={styles.metricValue}>{field.paybackYears.toFixed(1)} years</div>
            </div>
          </div>
        </div>

        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Enrollment</h2>
          <div style={styles.enrollmentCard}>
            <div style={styles.enrollmentValue}>{field.enrollment.toLocaleString()}</div>
            <div style={styles.enrollmentLabel}>students enrolled</div>
          </div>
        </div>
      </div>
    </div>
  );
};
