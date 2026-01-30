import { useEffect, useState } from 'react';
import { getAnalysis } from '../api';
import type { Analysis, FieldAnalysis } from '../models';
import { formatCurrency } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function AnalysisPage(){
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedField, setSelectedField] = useState<FieldAnalysis | null>(null);

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      const data = await getAnalysis();
      console.log(data);
      setAnalysis(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!analysis) return null;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Detailed Field Analysis</h1>
      <p style={styles.subtitle}>
        Comprehensive breakdown of financial metrics, ROI, and debt burden for each field
      </p>

      <div style={styles.layout}>
        <div style={styles.sidebar}>
          <h3 style={styles.sidebarTitle}>Select a Field</h3>
          {analysis.fields.map((field, index) => (
            <div
              key={index}
              style={{
                ...styles.fieldButton,
                ...(selectedField?.field === field.field ? styles.fieldButtonActive : {}),
              }}
              onClick={() => setSelectedField(field)}
            >
              {field.fieldDisplayName}
            </div>
          ))}
        </div>

        <div style={styles.content}>
          {selectedField ? (
            <FieldDetailView field={selectedField} />
          ) : (
            <div style={styles.placeholder}>
              <p>← Select a field from the list to view detailed analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

function FieldDetailView({ field }: {field: FieldAnalysis}) {
  const getComparisonBadge = (comparison: string) => {
    const isAbove = comparison === 'above';
    return (
      <span
        style={{
          ...styles.badge,
          backgroundColor: isAbove ? '#d4edda' : '#f8d7da',
          color: isAbove ? '#155724' : '#721c24',
        }}
      >
        {comparison} average
      </span>
    );
  };

  return (
    <div style={styles.detailContainer}>
      <h2 style={styles.detailTitle}>{field.fieldDisplayName}</h2>

      {/* Financial Metrics */}
      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Financial Metrics</h3>
        <div style={styles.metricsGrid}>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Annual Tuition</div>
            <div style={styles.metricValue}>
              {formatCurrency(field.financialMetrics.annualTuition)}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Total 4-Year Tuition</div>
            <div style={styles.metricValue}>
              {formatCurrency(field.financialMetrics.total_4yr_tuition)}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Estimated Debt</div>
            <div style={styles.metricValue}>
              {formatCurrency(field.financialMetrics.estimatedDebt)}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Median Earnings (Year 2)</div>
            <div style={styles.metricValue}>
              {formatCurrency(field.financialMetrics.median_earnings_year_2)}
            </div>
          </div>
        </div>
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Return on Investment</h3>
        <div style={styles.metricsGrid}>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Earnings per Dollar of Tuition</div>
            <div style={styles.metricValue}>
              ${field.roiMetrics.earningsPerDollarTuition.toFixed(2)}
            </div>
            <div style={styles.metricComparison}>
              {getComparisonBadge(field.roiMetrics.earningsPerDollarComparison)}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>5-Year ROI (Tuition)</div>
            <div style={{ ...styles.metricValue, color: '#28a745' }}>
              {field.roiMetrics.roi_5yr_tuition.toFixed(2)}x
            </div>
            <div style={styles.metricComparison}>
              {getComparisonBadge(field.roiMetrics.roiTuitionComparison)}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>5-Year ROI (Debt)</div>
            <div style={{ ...styles.metricValue, color: '#28a745' }}>
              {field.roiMetrics.roi_5yr_debt.toFixed(2)}x
            </div>
          </div>
        </div>
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Debt Burden</h3>
        <div style={styles.metricsGrid}>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Debt-to-Income Ratio</div>
            <div style={styles.metricValue}>
              {field.debtBurden.debtToIncomeRatio.toFixed(2)}x
            </div>
            <div style={styles.metricSubtext}>
              {field.debtBurden.debtToIncomeRatio > 1.0 ? 'High burden' : 'Manageable'}
            </div>
          </div>
          <div style={styles.metricCard}>
            <div style={styles.metricLabel}>Estimated Payback Period</div>
            <div style={styles.metricValue}>
              {field.debtBurden.paybackPeriodYears.toFixed(1)} years
            </div>
            <div style={styles.metricSubtext}>
              At 10% of post-tax income
            </div>
          </div>
        </div>
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Enrollment</h3>
        <div style={styles.enrollmentCard}>
          <div style={styles.enrollmentValue}>
            {field.enrollment.toLocaleString()}
          </div>
          <div style={styles.enrollmentLabel}>students enrolled</div>
        </div>
      </section>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1400px',
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
    marginBottom: '40px',
    fontSize: '1.1rem',
  },
  layout: {
    display: 'grid',
    gridTemplateColumns: '300px 1fr',
    gap: '30px',
  },
  sidebar: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    height: 'fit-content',
    position: 'sticky' as const,
    top: '20px',
  },
  sidebarTitle: {
    marginBottom: '15px',
    fontSize: '1.2rem',
    color: '#333',
  },
  fieldButton: {
    padding: '12px 15px',
    marginBottom: '8px',
    backgroundColor: '#f8f9fa',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    fontSize: '0.95rem',
  },
  fieldButtonActive: {
    backgroundColor: '#007bff',
    color: 'white',
    fontWeight: 'bold' as const,
  },
  content: {
    minHeight: '500px',
  },
  placeholder: {
    backgroundColor: 'white',
    padding: '60px',
    borderRadius: '8px',
    textAlign: 'center' as const,
    color: '#999',
    fontSize: '1.2rem',
  },
  detailContainer: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  detailTitle: {
    fontSize: '2rem',
    marginBottom: '30px',
    color: '#333',
    borderBottom: '3px solid #007bff',
    paddingBottom: '15px',
  },
  section: {
    marginBottom: '40px',
  },
  sectionTitle: {
    fontSize: '1.4rem',
    marginBottom: '20px',
    color: '#555',
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
  },
  metricCard: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    textAlign: 'center' as const,
  },
  metricLabel: {
    fontSize: '0.9rem',
    color: '#666',
    marginBottom: '10px',
  },
  metricValue: {
    fontSize: '1.8rem',
    fontWeight: 'bold' as const,
    color: '#333',
    marginBottom: '8px',
  },
  metricComparison: {
    marginTop: '8px',
  },
  metricSubtext: {
    fontSize: '0.85rem',
    color: '#888',
    marginTop: '5px',
  },
  badge: {
    display: 'inline-block',
    padding: '4px 10px',
    borderRadius: '12px',
    fontSize: '0.8rem',
    fontWeight: 'bold' as const,
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
