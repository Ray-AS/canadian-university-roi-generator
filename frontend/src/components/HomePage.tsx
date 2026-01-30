import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSummary } from '../api';
import { type Summary } from '../models';
import { formatCurrency, formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function HomePage() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      setLoading(true);
      const data = await getSummary();
      setSummary(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!summary) return null;

  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <h1 style={styles.heroTitle}>Canadian University ROI Analysis</h1>
        <p style={styles.heroSubtitle}>
          Comprehensive analysis of return on investment across different fields of study
        </p>
        <p style={styles.reportDate}>Report Date: {summary.reportDate}</p>
      </div>

      <div style={styles.statsSection}>
        <h2 style={styles.sectionTitle}>Overview Statistics</h2>
        <div style={styles.statsGrid}>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{formatCurrency(summary.overallAverages.avgAnnualTuition)}</div>
            <div style={styles.statLabel}>Average Annual Tuition</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{formatCurrency(summary.overallAverages.avgEarningsYear2)}</div>
            <div style={styles.statLabel}>Average Earnings (Year 2)</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{summary.overallAverages.avg5yrRoi.toFixed(2)}x</div>
            <div style={styles.statLabel}>Average 5-Year ROI</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{summary.overallAverages.avgPaybackPeriodYears.toFixed(1)} yrs</div>
            <div style={styles.statLabel}>Average Payback Period</div>
          </div>
        </div>
      </div>

      <div style={styles.highlightsSection}>
        <div style={styles.highlightColumn}>
          <h3 style={styles.highlightTitle}>Best Performing</h3>
          
          <div style={styles.highlightCard}>
            <h4>Highest ROI</h4>
            <div style={styles.fieldName}>{formatFieldName(summary.bestPerforming.roiResult.field)}</div>
            <div style={styles.highlightStat}>{summary.bestPerforming.roiResult.roi5yr.toFixed(2)}x ROI</div>
          </div>

          <div style={styles.highlightCard}>
            <h4>Best Value</h4>
            <div style={styles.fieldName}>{formatFieldName(summary.bestPerforming.valueResult.field)}</div>
            <div style={styles.highlightStat}>${summary.bestPerforming.valueResult.earningsPerDollar.toFixed(2)} per dollar</div>
          </div>

          <div style={styles.highlightCard}>
            <h4>Fastest Payback</h4>
            <div style={styles.fieldName}>{formatFieldName(summary.bestPerforming.paybackResult.field)}</div>
            <div style={styles.highlightStat}>{summary.bestPerforming.paybackResult.paybackYears.toFixed(1)} years</div>
          </div>
        </div>
      </div>

      <div style={styles.linksSection}>
        <h2 style={styles.sectionTitle}>Explore More</h2>
        <div style={styles.linksGrid}>
          <Link to="/fields" style={styles.linkCard}>
            <h3>All Fields</h3>
            <p>Browse all fields of study with detailed metrics</p>
          </Link>
          <Link to="/rankings" style={styles.linkCard}>
            <h3>Rankings</h3>
            <p>See fields ranked by various criteria</p>
          </Link>
          <Link to="/analysis" style={styles.linkCard}>
            <h3>Detailed Analysis</h3>
            <p>In-depth analysis of each field</p>
          </Link>
          <Link to="/methodology" style={styles.linkCard}>
            <h3>Methodology</h3>
            <p>Learn how the data was collected and analyzed</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
  },
  hero: {
    textAlign: 'center' as const,
    padding: '60px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '12px',
    color: 'white',
    marginBottom: '40px',
  },
  heroTitle: {
    fontSize: '3rem',
    margin: '0 0 20px 0',
  },
  heroSubtitle: {
    fontSize: '1.3rem',
    margin: '0 0 10px 0',
    opacity: 0.95,
  },
  reportDate: {
    fontSize: '1rem',
    opacity: 0.9,
  },
  statsSection: {
    marginBottom: '40px',
  },
  sectionTitle: {
    fontSize: '2rem',
    marginBottom: '20px',
    textAlign: 'center' as const,
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
    marginBottom: '20px',
  },
  statCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textAlign: 'center' as const,
  },
  statValue: {
    fontSize: '2rem',
    fontWeight: 'bold' as const,
    color: '#007bff',
    marginBottom: '10px',
  },
  statLabel: {
    fontSize: '0.95rem',
    color: '#666',
  },
  highlightsSection: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '30px',
    marginBottom: '40px',
  },
  highlightColumn: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  highlightTitle: {
    fontSize: '1.5rem',
    marginBottom: '20px',
    textAlign: 'center' as const,
  },
  highlightCard: {
    padding: '15px',
    marginBottom: '15px',
    borderRadius: '6px',
    backgroundColor: '#f8f9fa',
    borderLeft: '4px solid #28a745',
  },
  concernCard: {
    borderLeft: '4px solid #dc3545',
  },
  fieldName: {
    fontSize: '1.1rem',
    fontWeight: 'bold' as const,
    margin: '10px 0',
    color: '#333',
  },
  highlightStat: {
    fontSize: '1rem',
    color: '#007bff',
    fontWeight: 'bold' as const,
  },
  linksSection: {
    marginTop: '60px',
  },
  linksGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
  },
  linkCard: {
    display: 'block',
    padding: '30px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textDecoration: 'none',
    color: '#333',
    textAlign: 'center' as const,
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'pointer',
  },
  linkIcon: {
    fontSize: '3rem',
    marginBottom: '15px',
  },
};
