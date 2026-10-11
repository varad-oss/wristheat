import { getPublicRoster } from '../api';
import { Footer } from '../components/Footer';
import { PublicHeader } from '../App';
import { useRoster } from '../useRoster';
import { Live } from './Live';

/** Read-only public demo of the SIMULATED group; real wearers stay behind sign-in. */
export function Demo() {
  const { roster, error } = useRoster(3000, getPublicRoster);
  return (
    <>
      <PublicHeader />
      <p className="demo-banner" role="note">
        Public demo. All trainees here are SIMULATED. Real wearers are visible only to signed-in supervisors.
      </p>
      <Live roster={roster} error={error} readOnly />
      <Footer />
    </>
  );
}
