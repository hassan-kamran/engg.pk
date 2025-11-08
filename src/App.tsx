import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ForumPage from './pages/ForumPage';
import UniversitiesPage from './pages/UniversitiesPage';
import CareerPathsPage from './pages/CareerPathsPage';
import JobsPage from './pages/JobsPage';
import ScholarshipsPage from './pages/ScholarshipsPage';
import IndustryInsightsPage from './pages/IndustryInsightsPage';
import SubjectConnectionsPage from './pages/SubjectConnectionsPage';
import StartupsPage from './pages/StartupsPage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="forum" element={<ForumPage />} />
          <Route path="universities" element={<UniversitiesPage />} />
          <Route path="careers" element={<CareerPathsPage />} />
          <Route path="jobs" element={<JobsPage />} />
          <Route path="scholarships" element={<ScholarshipsPage />} />
          <Route path="insights" element={<IndustryInsightsPage />} />
          <Route path="subjects" element={<SubjectConnectionsPage />} />
          <Route path="startups" element={<StartupsPage />} />
          <Route path="about" element={<AboutPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
