import { useEffect, useState } from 'react';
import { getPolicyRecommendations } from '../api';
import { type PolicyRecommendations } from '../models';
import { formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function PolicyRecommendationsPage() {
  const styles = {
    container: {
      maxWidth: '1200px',
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
    content: {
      backgroundColor: 'white',
      padding: '40px',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    },
    section: {
      marginBottom: '50px',
    },
    sectionTitle: {
      fontSize: '1.8rem',
      marginBottom: '20px',
      color: '#007bff',
      borderBottom: '2px solid #007bff',
      paddingBottom: '10px',
    },
    intro: {
      fontSize: '1.05rem',
      marginBottom: '20px',
      color: '#555',
    },
    concernBlock: {
      marginBottom: '40px',
      padding: '25px',
      backgroundColor: '#fff3cd',
      borderRadius: '8px',
      border: '2px solid #ffc107',
    },
    concernTitle: {
      fontSize: '1.4rem',
      marginBottom: '10px',
      color: '#856404',
    },
    concernDescription: {
      marginBottom: '20px',
      color: '#856404',
    },
    fieldsList: {
      marginBottom: '20px',
    },
    fieldItem: {
      padding: '15px',
      marginBottom: '10px',
      backgroundColor: 'white',
      borderRadius: '6px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    },
    fieldName: {
      fontSize: '1.1rem',
      fontWeight: 'bold' as const,
      marginBottom: '8px',
      color: '#333',
    },
    fieldStats: {
      display: 'flex',
      gap: '20px',
      fontSize: '0.95rem',
      color: '#666',
    },
    fieldStat: {
      fontWeight: 'bold' as const,
    },
    recommendationsBox: {
      padding: '20px',
      backgroundColor: 'white',
      borderRadius: '6px',
      marginTop: '20px',
    },
    recommendationsList: {
      marginTop: '10px',
      lineHeight: '1.8',
      paddingLeft: '20px',
    },
    bestPracticesGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '20px',
      marginBottom: '20px',
    },
    bestPracticeCard: {
      padding: '20px',
      backgroundColor: '#d4edda',
      borderRadius: '8px',
      border: '2px solid #28a745',
    },
    bestPracticeTitle: {
      fontSize: '1.2rem',
      marginBottom: '15px',
      color: '#155724',
    },
    bestPracticeStats: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '10px',
    },
    bestPracticeStat: {
      textAlign: 'center' as const,
    },
    statLabel: {
      fontSize: '0.85rem',
      color: '#155724',
      marginBottom: '5px',
    },
    statValue: {
      fontSize: '1.4rem',
      fontWeight: 'bold' as const,
      color: '#155724',
    },
    systemWideGrid: {
      display: 'grid',
      gap: '15px',
    },
    systemWideCard: {
      display: 'flex',
      gap: '20px',
      padding: '20px',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      alignItems: 'center',
    },
    systemWideNumber: {
      width: '50px',
      height: '50px',
      borderRadius: '50%',
      backgroundColor: '#007bff',
      color: 'white',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '1.5rem',
      fontWeight: 'bold' as const,
      flexShrink: 0,
    },
    systemWideText: {
      fontSize: '1.05rem',
      color: '#333',
      lineHeight: '1.6',
    },
  };

  const [policy, setPolicy] = useState<PolicyRecommendations | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPolicy();
  }, []);

  const loadPolicy = async () => {
    try {
      setLoading(true);
      const data = await getPolicyRecommendations();
      console.log(data);
      setPolicy(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!policy) return null;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Policy Recommendations</h1>
      <p style={styles.subtitle}>
        Evidence-based recommendations for improving student outcomes and educational ROI
      </p>

      <div style={styles.content}>
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Areas Requiring Attention</h2>

          <div style={styles.concernBlock}>
            <h3 style={styles.concernTitle}>High Enrollment, Low ROI Fields</h3>
            <p style={styles.concernDescription}>
              These fields serve many students but show below-median returns:
            </p>
            <div style={styles.fieldsList}>
              {policy.areasRequiringAttention.highEnrollmentLowRoi.map((field, index) => (
                <div key={index} style={styles.fieldItem}>
                  <div style={styles.fieldName}>{formatFieldName(field.field)}</div>
                  <div style={styles.fieldStats}>
                    <span>{field.enrollment.toLocaleString()} students</span>
                    <span style={styles.fieldStat}>ROI: {field.roi_5yr.toFixed(2)}x</span>
                  </div>
                </div>
              ))}
            </div>
            <div style={styles.recommendationsBox}>
              <strong>Recommendations:</strong>
              <ul style={styles.recommendationsList}>
                {policy.recommendations.highEnrollmentLowRoiFields.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>

          <div style={styles.concernBlock}>
            <h3 style={styles.concernTitle}>High Debt Burden Fields</h3>
            <p style={styles.concernDescription}>
              Fields where students face significant repayment challenges:
            </p>
            <div style={styles.fieldsList}>
              {policy.areasRequiringAttention.highDebtBurden.map((field, index) => (
                <div key={index} style={styles.fieldItem}>
                  <div style={styles.fieldName}>{formatFieldName(field.field)}</div>
                  <div style={styles.fieldStats}>
                    <span style={styles.fieldStat}>Debt/Income: {field.debtToIncome.toFixed(2)}x</span>
                    <span style={styles.fieldStat}>Payback: {field.paybackYears.toFixed(1)} years</span>
                  </div>
                </div>
              ))}
            </div>
            <div style={styles.recommendationsBox}>
              <strong>Recommendations:</strong>
              <ul style={styles.recommendationsList}>
                {policy.recommendations.highDebtBurdenFields.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Best Practices to Expand</h2>
          <p style={styles.intro}>
            Fields showing strong ROI and reasonable debt burdens can serve as models:
          </p>
          <div style={styles.bestPracticesGrid}>
            {policy.bestPractices.map((field, index) => (
              <div key={index} style={styles.bestPracticeCard}>
                <h4 style={styles.bestPracticeTitle}>{formatFieldName(field.field)}</h4>
                <div style={styles.bestPracticeStats}>
                  <div style={styles.bestPracticeStat}>
                    <div style={styles.statLabel}>5-Year ROI</div>
                    <div style={styles.statValue}>{field.roi_5yr.toFixed(2)}x</div>
                  </div>
                  <div style={styles.bestPracticeStat}>
                    <div style={styles.statLabel}>Debt-to-Income</div>
                    <div style={styles.statValue}>{field.debtToIncome.toFixed(2)}x</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div style={styles.recommendationsBox}>
            <strong>Recommendations:</strong>
            <ul style={styles.recommendationsList}>
              {/*TODO: FIX RECOMMENDATIONS NOT SHOWING FOR POSITIVE*/}
              <li>Study successful curriculum and industry partnership models</li>
              <li>Promote these fields to students considering post-secondary education</li>
            </ul>
          </div>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>System-Wide Improvements</h2>
          <div style={styles.systemWideGrid}>
            {policy.recommendations.systemWide.map((recommendation, index) => (
              <div key={index} style={styles.systemWideCard}>
                <div style={styles.systemWideNumber}>{index + 1}</div>
                <div style={styles.systemWideText}>{recommendation}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};
