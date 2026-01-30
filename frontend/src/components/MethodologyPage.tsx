import { useEffect, useState } from 'react';
import { getMethodology } from '../api';
import { type Methodology } from '../models';
import LoadingSpinner from './LoadingSpinner';

export default function MethodologyPage() {
  const styles = {
    container: {
      maxWidth: '1000px',
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
      marginBottom: '15px',
      color: '#555',
    },
    list: {
      lineHeight: '1.8',
      color: '#555',
      paddingLeft: '25px',
    },
    listItem: {
      marginBottom: '10px',
    },
    dataYearsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '15px',
    },
    dataYearCard: {
      padding: '20px',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      textAlign: 'center' as const,
    },
    dataYearLabel: {
      fontSize: '0.9rem',
      color: '#666',
      marginBottom: '8px',
    },
    dataYearValue: {
      fontSize: '1.3rem',
      fontWeight: 'bold' as const,
      color: '#333',
    },
    assumptionBlock: {
      marginBottom: '30px',
      padding: '20px',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      borderLeft: '4px solid #007bff',
    },
    assumptionTitle: {
      fontSize: '1.3rem',
      marginBottom: '15px',
      color: '#333',
    },
    assumptionGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '10px',
      marginTop: '10px',
    },
    assumptionItem: {
      padding: '10px',
      backgroundColor: 'white',
      borderRadius: '4px',
    },
    formulaBox: {
      marginTop: '15px',
      padding: '15px',
      backgroundColor: '#fff',
      borderRadius: '6px',
      border: '1px solid #dee2e6',
      fontFamily: 'monospace',
    },
    limitationsBox: {
      padding: '20px',
      backgroundColor: '#fff3cd',
      borderRadius: '8px',
      border: '1px solid #ffc107',
    },
    limitationsIntro: {
      marginBottom: '15px',
      fontWeight: 'bold' as const,
      color: '#856404',
    },
  };

  const [methodology, setMethodology] = useState<Methodology | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMethodology();
  }, []);

  const loadMethodology = async () => {
    try {
      setLoading(true);
      const data = await getMethodology();
      console.log(data);
      setMethodology(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!methodology) return null;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Methodology & Assumptions</h1>
      <p style={styles.subtitle}>
        Understanding how the data was collected, processed, and analyzed
      </p>

      <div style={styles.content}>
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Data Sources</h2>
          <p style={styles.intro}>All data sourced from Statistics Canada tables:</p>
          <ul style={styles.list}>
            {methodology.dataSources.map((source, index) => (
              <li key={index} style={styles.listItem}>{source}</li>
            ))}
          </ul>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Data Years</h2>
          <div style={styles.dataYearsGrid}>
            <div style={styles.dataYearCard}>
              <div style={styles.dataYearLabel}>Tuition Data</div>
              <div style={styles.dataYearValue}>{methodology.dataYears.tuition}</div>
            </div>
            <div style={styles.dataYearCard}>
              <div style={styles.dataYearLabel}>Earnings Data</div>
              <div style={styles.dataYearValue}>{methodology.dataYears.earnings}</div>
            </div>
            <div style={styles.dataYearCard}>
              <div style={styles.dataYearLabel}>Enrollment Data</div>
              <div style={styles.dataYearValue}>{methodology.dataYears.enrollment}</div>
            </div>
            <div style={styles.dataYearCard}>
              <div style={styles.dataYearLabel}>Debt Data</div>
              <div style={styles.dataYearValue}>{methodology.dataYears.debt}</div>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Key Assumptions</h2>

          <div style={styles.assumptionBlock}>
            <h3 style={styles.assumptionTitle}>Inflation Adjustment</h3>
            <div style={styles.assumptionGrid}>
              <div style={styles.assumptionItem}>
                <strong>CPI (2018 to 2024):</strong> {methodology.assumptions.inflationAdjustment.cpi_2018_to_2024}
              </div>
              <div style={styles.assumptionItem}>
                <strong>CPI (2020 to 2024):</strong> {methodology.assumptions.inflationAdjustment.cpi_2020_to_2024}
              </div>
            </div>
          </div>

          <div style={styles.assumptionBlock}>
            <h3 style={styles.assumptionTitle}>Debt Estimation</h3>
            <p><strong>Method:</strong> {methodology.assumptions.debtEstimation.method}</p>
            <p><strong>Program Length:</strong> {methodology.assumptions.debtEstimation.programLength}</p>
            <div style={styles.formulaBox}>
              <strong>Formula:</strong><br />
              <code>{methodology.assumptions.debtEstimation.formula}</code>
            </div>
          </div>

          <div style={styles.assumptionBlock}>
            <h3 style={styles.assumptionTitle}>ROI Calculation</h3>
            <p><strong>Earnings Growth:</strong> {(methodology.assumptions.roiCalculation.earningsGrowth * 100).toFixed(0)}% annually</p>
            <p><strong>Base Period:</strong> {methodology.assumptions.roiCalculation.basePeriod}</p>
            <div style={styles.formulaBox}>
              <strong>Tuition-based ROI:</strong><br />
              <code>{methodology.assumptions.roiCalculation.tuitionRoiFormula}</code>
            </div>
            <div style={styles.formulaBox}>
              <strong>Debt-based ROI:</strong><br />
              <code>{methodology.assumptions.roiCalculation.debtRoiFormula}</code>
            </div>
          </div>

          <div style={styles.assumptionBlock}>
            <h3 style={styles.assumptionTitle}>Payback Period Calculation</h3>
            <div style={styles.assumptionGrid}>
              <div style={styles.assumptionItem}>
                <strong>Income to Debt Repayment:</strong> {(methodology.assumptions.paybackCalculation.incomeToDebtRepayment * 100).toFixed(0)}%
              </div>
              <div style={styles.assumptionItem}>
                <strong>Tax Rate:</strong> {(methodology.assumptions.paybackCalculation.taxRate * 100).toFixed(0)}%
              </div>
              <div style={styles.assumptionItem}>
                <strong>Interest Rate:</strong> {(methodology.assumptions.paybackCalculation.interestRate * 100).toFixed(0)}%
              </div>
            </div>
            <div style={styles.formulaBox}>
              <strong>Formula:</strong><br />
              <code>{methodology.assumptions.paybackCalculation.formula}</code>
            </div>
          </div>

          <div style={styles.assumptionBlock}>
            <h3 style={styles.assumptionTitle}>Earnings per Dollar</h3>
            <div style={styles.formulaBox}>
              <strong>Formula:</strong><br />
              <code>{methodology.assumptions.earningsPerDollar.formula}</code>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Limitations</h2>
          <div style={styles.limitationsBox}>
            <p style={styles.limitationsIntro}>
              This analysis has several important limitations to consider:
            </p>
            <ul style={styles.list}>
              {methodology.limitations.map((limitation, index) => (
                <li key={index} style={styles.listItem}>{limitation}</li>
              ))}
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
};
