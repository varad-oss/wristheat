import type { ReactNode } from 'react';
import { Link, Navigate, NavLink, Route, Routes, useParams } from 'react-router-dom';
import { AlertBanner } from './components/AlertBanner';
import { Footer } from './components/Footer';
import { Demo } from './pages/Demo';
import { IncidentDetail } from './pages/IncidentDetail';
import { Incidents } from './pages/Incidents';
import { Landing } from './pages/Landing';
import { Live } from './pages/Live';
import { Method } from './pages/Method';
import { SessionReport } from './pages/SessionReport';
import { TraineeDetail } from './pages/TraineeDetail';
import { useRoster } from './useRoster';

export function Brand({ to }: { to: string }) {
  return (
    <Link to={to} className="brand">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect x="5" y="3" width="2.5" height="27" fill="currentColor" /><path d="M7.5 4h19l-5 6 5 6h-19z" fill="#b42318" /></svg>
      WristHeat
    </Link>
  );
}

/** Public pages share a slim header: demo, method, sign-in. */
export function PublicHeader() {
  return (
    <header className="top">
      <Brand to="/" />
      <nav aria-label="Main">
        <NavLink to="/demo">Live demo</NavLink>
        <NavLink to="/method">Method</NavLink>
      </nav>
      <Link to="/console" className="btn btn-quiet who">Supervisor sign-in</Link>
    </header>
  );
}

/** Signed-in supervisor console (mounted under /console). */
export function Console({ user, onSignOut }: { user: string; onSignOut: () => void }) {
  const { roster, error } = useRoster();
  return (
    <>
      <header className="top">
        <Brand to="/console" />
        <nav aria-label="Console">
          <NavLink to="/console" end>Group</NavLink>
          <NavLink to="/console/incidents">Incidents</NavLink>
          <NavLink to="/method">Method</NavLink>
        </nav>
        <span className="who">{user}<button className="btn btn-quiet" onClick={onSignOut}>Sign out</button></span>
      </header>
      <AlertBanner incidents={roster?.open_incidents ?? []} />
      <Routes>
        <Route index element={<Live roster={roster} error={error} />} />
        <Route path="trainee/:id" element={<TraineeDetail roster={roster} />} />
        <Route path="incidents" element={<Incidents />} />
        <Route path="incidents/:id" element={<IncidentDetail />} />
        <Route path="sessions/:id/report" element={<SessionReport />} />
        <Route path="*" element={<main className="page"><p>Page not found.</p></main>} />
      </Routes>
      <Footer />
    </>
  );
}

function Legacy({ to }: { to: (p: Record<string, string | undefined>) => string }) {
  return <Navigate to={to(useParams())} replace />;
}

/** Every route of the site. `consoleElement` is the authenticated console (Authenticator-wrapped in main.tsx). */
export function SiteRoutes({ consoleElement }: { consoleElement: ReactNode }) {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/demo" element={<Demo />} />
      <Route path="/method" element={<><PublicHeader /><Method /><Footer /></>} />
      <Route path="/console/*" element={consoleElement} />
      <Route path="/incidents" element={<Navigate to="/console/incidents" replace />} />
      <Route path="/incidents/:id" element={<Legacy to={(p) => `/console/incidents/${p.id}`} />} />
      <Route path="/trainee/:id" element={<Legacy to={(p) => `/console/trainee/${p.id}`} />} />
      <Route path="/sessions/:id/report" element={<Legacy to={(p) => `/console/sessions/${p.id}/report`} />} />
      <Route path="*" element={<><PublicHeader /><main className="page"><p>Page not found. <Link to="/">Go to the home page</Link>.</p></main></>} />
    </Routes>
  );
}
