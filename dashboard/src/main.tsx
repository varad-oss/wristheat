import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { Amplify } from 'aws-amplify';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Console, RoleGate, SiteRoutes, WearerArea } from './App';
import { useRole } from './role';
import { loadConfig } from './config';
import './styles.css';

const root = createRoot(document.getElementById('root')!);

function ConsoleForRole(props: { user: string; onSignOut: () => void }) {
  return <RoleGate role={useRole()}><Console {...props} /></RoleGate>;
}

const signInHeader = { Header: () => <div className="login-head"><h1>WristHeat</h1><p>Sign in as a supervisor or a wearer</p></div> };

const consoleElement = (
  <Authenticator hideSignUp components={signInHeader}>
    {({ signOut, user }) => <ConsoleForRole user={user?.signInDetails?.loginId ?? user?.username ?? ''} onSignOut={() => signOut?.()} />}
  </Authenticator>
);

const wearerElement = (
  <Authenticator hideSignUp components={signInHeader}>
    {({ signOut, user }) => <WearerArea user={user?.signInDetails?.loginId ?? user?.username ?? ''} onSignOut={() => signOut?.()} />}
  </Authenticator>
);

loadConfig()
  .then((cfg) => {
    Amplify.configure({ Auth: { Cognito: { userPoolId: cfg.userPoolId, userPoolClientId: cfg.userPoolClientId } } });
    root.render(
      <StrictMode>
        <BrowserRouter><SiteRoutes consoleElement={consoleElement} wearerElement={wearerElement} /></BrowserRouter>
      </StrictMode>,
    );
  })
  .catch((e) => root.render(<p style={{ padding: 24 }}>Couldn't load the dashboard configuration: {String(e)}</p>));
