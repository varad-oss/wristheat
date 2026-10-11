import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { Amplify } from 'aws-amplify';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import { loadConfig } from './config';
import './styles.css';

const root = createRoot(document.getElementById('root')!);

loadConfig()
  .then((cfg) => {
    Amplify.configure({ Auth: { Cognito: { userPoolId: cfg.userPoolId, userPoolClientId: cfg.userPoolClientId } } });
    root.render(
      <StrictMode>
        <Authenticator hideSignUp components={{ Header: () => <div className="login-head"><h1>WristHeat</h1><p>Supervisor console</p></div> }}>
          {({ signOut, user }) => <App user={user?.signInDetails?.loginId ?? user?.username ?? ''} onSignOut={() => signOut?.()} />}
        </Authenticator>
      </StrictMode>,
    );
  })
  .catch((e) => root.render(<p style={{ padding: 24 }}>Couldn't load the dashboard configuration: {String(e)}</p>));
