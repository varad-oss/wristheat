export const ATTRIBUTION = 'Weather: Open-Meteo.com (CC BY 4.0) · Air quality: CAMS via Open-Meteo · ' +
  'Core-temperature estimate: ECTemp (USARIEM, US patent 10702165), used in a non-commercial research prototype';

export function Footer() {
  return (
    <footer className="footer" role="contentinfo">
      <p>{ATTRIBUTION}</p>
      <p>Estimated values from a research prototype. Not a medical device.</p>
    </footer>
  );
}
