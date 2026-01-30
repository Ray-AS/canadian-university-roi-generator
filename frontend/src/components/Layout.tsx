import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column' as const,
      backgroundColor: '#f5f5f5',
    },
    nav: {
      backgroundColor: '#333',
      padding: '0 20px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    },
    navContent: {
      maxWidth: '1200px',
      margin: '0 auto',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      height: '60px',
    },
    logo: {
      color: 'white',
      fontSize: '1.5rem',
      fontWeight: 'bold' as const,
      textDecoration: 'none',
    },
    navLinks: {
      display: 'flex',
      gap: '25px',
    },
    navLink: {
      color: 'white',
      textDecoration: 'none',
      fontSize: '1rem',
      transition: 'color 0.2s',
    },
    main: {
      flex: 1,
      paddingTop: '20px',
      paddingBottom: '40px',
    },
    footer: {
      backgroundColor: '#333',
      color: 'white',
      textAlign: 'center' as const,
      padding: '20px',
      marginTop: 'auto',
    },
  };

  return (
    <div style={styles.container}>
      <nav style={styles.nav}>
        <div style={styles.navContent}>
          <Link to="/" style={styles.logo}>ROI Analysis</Link>
          <div style={styles.navLinks}>
            <Link to="/" style={styles.navLink}>Home</Link>
            <Link to="/fields" style={styles.navLink}>Fields</Link>
            <Link to="/rankings" style={styles.navLink}>Rankings</Link>
            <Link to="/analysis" style={styles.navLink}>Analysis</Link>
            <Link to="/methodology" style={styles.navLink}>Methodology</Link>
          </div>
        </div>
      </nav>
      
      <main style={styles.main}>
        <Outlet />
      </main>

      <footer style={styles.footer}>
        <p>Data Source: Statistics Canada</p>
      </footer>
    </div>
  );
};
