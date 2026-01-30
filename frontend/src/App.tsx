import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './components/HomePage'
import Layout from './components/Layout'
import FieldsPage from './components/FieldsPage'
import FieldDetailPage from './components/FieldDetailPage'
import RankingsPage from './components/RankingsPage'
import AnalysisPage from './components/AnalysisPage'
import MethodologyPage from './components/MethodologyPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="fields" element={<FieldsPage />} />
          <Route path="fields/:fieldName" element={<FieldDetailPage />} />
          <Route path="rankings" element={<RankingsPage />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="methodology" element={<MethodologyPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
