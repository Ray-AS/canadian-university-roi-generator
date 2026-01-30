import { useEffect, useState } from 'react';
import { getRankings } from '../api';
import { type RankedField, type Rankings } from '../models';
import { formatFieldName } from '../formatters';
import LoadingSpinner from './LoadingSpinner';

export default function RankingsPage() {
  const styles = {
    container: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px',
    },
    title: {
      fontSize: '2.5rem',
      marginBottom: '40px',
      textAlign: 'center' as const,
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '30px',
    },
    rankingSection: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    },
    rankingTitle: {
      fontSize: '1.3rem',
      marginBottom: '20px',
      color: '#333',
      borderBottom: '2px solid #007bff',
      paddingBottom: '10px',
    },
    rankingList: {
      listStyle: 'none',
      padding: 0,
      margin: 0,
      counterReset: 'ranking',
    },
    rankingItem: {
      display: 'flex',
      justifyContent: 'space-between',
      padding: '12px',
      marginBottom: '8px',
      backgroundColor: '#f8f9fa',
      borderRadius: '4px',
      counterIncrement: 'ranking',
    },
    rankingField: {
      fontWeight: 'bold' as const,
    },
    rankingValue: {
      color: '#007bff',
      fontWeight: 'bold' as const,
    },
  };


  const [rankings, setRankings] = useState<Rankings | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRankings();
  }, []);

  const loadRankings = async () => {
    try {
      setLoading(true);
      const data = await getRankings();
      console.log(data);
      setRankings(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!rankings) return null;

  const renderRankingList = (title: string, items: RankedField[], valueFormatter: (val: number) => string) => (
    <div style={styles.rankingSection}>
      <h3 style={styles.rankingTitle}>{title}</h3>
      <ol style={styles.rankingList}>
        {items.map((item) => (
          <li key={item.rank} style={styles.rankingItem}>
            <span style={styles.rankingField}>{formatFieldName(item.field)}</span>
            <span style={styles.rankingValue}>{valueFormatter(item.value)}</span>
          </li>
        ))}
      </ol>
    </div>
  );

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Field Rankings</h1>

      <div style={styles.grid}>
        {renderRankingList(
          'By 5-Year ROI',
          rankings.by_5yr_roi,
          (val) => `${val.toFixed(2)}x`
        )}

        {renderRankingList(
          'By Earnings per Dollar',
          rankings.byEarningsPerDollar,
          (val) => `$${val.toFixed(2)}`
        )}

        {renderRankingList(
          'By Debt-to-Income (Lower is Better)',
          rankings.byDebtToIncome,
          (val) => `${val.toFixed(2)}x`
        )}

        {renderRankingList(
          'By Payback Period (Faster is Better)',
          rankings.byPaybackPeriod,
          (val) => `${val.toFixed(1)} years`
        )}
      </div>
    </div>
  );
};
