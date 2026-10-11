import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom';
import { AlertBanner } from './components/AlertBanner';
import { Footer } from './components/Footer';
import { IncidentDetail } from './pages/IncidentDetail';
import { Incidents } from './pages/Incidents';
import { Live } from './pages/Live';
import { Method } from './pages/Method';
import { TraineeDetail } from './pages/TraineeDetail';
import { useRoster } from './useRoster';

export function App({ user, onSignOut }: { user: string; onSignOut: () => void }) {
  const { roster, error } = useRoster();
  return (
    <BrowserRouter>
      <header className="top">
        <NavLink to="/" className="brand" end>
          <svg viewBox="0 0 32 32" aria-hidden="true"><rect x="5" y="3" width="2.5" height="27" fill="currentColor" /><path d="M7.5 4h19l-5 6 5 6h-19z" fill="#b42318" /></svg>
          WristHeat
        </NavLink>
        <nav aria-label="Main">
          <NavLink to="/" end>Group</NavLink>
          <NavLink to="/incidents">Incidents</NavLink>
          <NavLink to="/method">Method</NavLink>
        </nav>
        <span className="who">{user}<button className="btn btn-quiet" onClick={onSignOut}>Sign out</button></span>
      </header>
      <AlertBanner incidents={roster?.open_incidents ?? []} />
      <Routes>
        <Route path="/" element={<Live roster={roster} error={error} />} />
        <Route path="/trainee/:id" element={<TraineeDetail roster={roster} />} />
        <Route path="/incidents" element={<Incidents />} />
        <Route path="/incidents/:id" element={<IncidentDetail />} />
        <Route path="/method" element={<Method />} />
        <Route path="*" element={<main className="page"><p>Page not found.</p></main>} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}
