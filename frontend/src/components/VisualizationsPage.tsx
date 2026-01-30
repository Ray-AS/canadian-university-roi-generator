import { useEffect, useState } from 'react';
import { getVisualizations } from '../api';
import { type VisualizationsDetails } from '../models';
import LoadingSpinner from './LoadingSpinner';

export default function VisualizationsPage() {
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
    vizSection: {
      marginBottom: '60px',
      paddingBottom: '40px',
      borderBottom: '2px solid #e9ecef',
    },
    vizHeader: {
      marginBottom: '25px',
    },
    vizTitle: {
      fontSize: '1.8rem',
      marginBottom: '10px',
      color: '#007bff',
    },
    vizDescription: {
      fontSize: '1.05rem',
      color: '#555',
      lineHeight: '1.6',
    },
    imageContainer: {
      marginBottom: '20px',
      borderRadius: '8px',
      overflow: 'hidden',
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    },
    image: {
      width: '100%',
      height: 'auto',
      display: 'block',
    },
    insightBox: {
      padding: '20px',
      backgroundColor: '#e7f3ff',
      borderRadius: '8px',
      borderLeft: '4px solid #007bff',
      fontSize: '1.05rem',
      lineHeight: '1.6',
    },
    downloadBox: {
      marginTop: '40px',
      padding: '25px',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      border: '2px solid #dee2e6',
    },
  };

  const [visualizations, setVisualizations] = useState<VisualizationsDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVisualizations();
  }, []);

  const loadVisualizations = async () => {
    try {
      setLoading(true);
      const data = await getVisualizations();
      console.log(data);
      setVisualizations(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!visualizations) return null;

  const getImagePath = (filename: string) => `../figures/${filename}`;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Data Visualizations</h1>
      <p style={styles.subtitle}>
        Visual representations of ROI analysis across different fields of study
      </p>

      <div style={styles.content}>
        {visualizations.visualizations.map((viz, index) => (
          <section key={index} style={styles.vizSection}>
            <div style={styles.vizHeader}>
              <h2 style={styles.vizTitle}>
                {index + 1}. {viz.name}
              </h2>
              <p style={styles.vizDescription}>{viz.description}</p>
            </div>

            <div style={styles.imageContainer}>
              <img 
                src={getImagePath(viz.filename)} 
                alt={viz.name}
                style={styles.image}
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  const parent = target.parentElement;
                  if (parent) {
                    const fallback = document.createElement('div');
                    fallback.style.cssText = 'padding: 60px; text-align: center; background-color: #f8f9fa; border-radius: 8px; color: #666;';
                    fallback.innerHTML = `
                      <p>Image: ${viz.filename}</p>
                      <p style="font-size: 0.9rem; margin-top: 10px;">Place this file in <code>public/figures/</code></p>
                    `;
                    parent.appendChild(fallback);
                  }
                }}
              />
            </div>

            {viz.filename === 'tuition_vs_earnings.png' && (
              <div style={styles.insightBox}>
                <strong>Key Insight:</strong> Some of the lowest-tuition fields produce competitive earnings, suggesting strong value for students.
              </div>
            )}
            {viz.filename === 'roi_by_field.png' && (
              <div style={styles.insightBox}>
                <strong>Key Insight:</strong> Fields where debt-based ROI is significantly lower than tuition-based ROI indicate students are over-borrowing relative to costs.
              </div>
            )}
            {viz.filename === 'payback_years.png' && (
              <div style={styles.insightBox}>
                <strong>Key Insight:</strong> Fields requiring 15+ years for debt repayment may discourage students despite long-term career potential.
              </div>
            )}
            {viz.filename === 'debt_to_income_ratio.png' && (
              <div style={styles.insightBox}>
                <strong>Key Insight:</strong> Fields with ratios above 1.2x may face significant repayment stress and warrant financial aid attention.
              </div>
            )}
          </section>
        ))}

        <div style={styles.downloadBox}>
          <h3>Accessing Visualization Files</h3>
          <p>All visualization files are available in the <code>figures/</code> directory of the project.</p>
          <p>To view images in this interface, place the PNG files in <code>public/figures/</code>:</p>
          <ul>
            {visualizations.visualizations.map((viz, index) => (
              <li key={index}><code>{viz.filename}</code></li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
