export interface AppConfig { apiUrl: string; region: string; userPoolId: string; userPoolClientId: string }

let config: AppConfig | null = null;

export async function loadConfig(): Promise<AppConfig> {
  const res = await fetch('/config.json', { cache: 'no-store' });
  if (!res.ok) throw new Error(`config.json: HTTP ${res.status}`);
  config = (await res.json()) as AppConfig;
  return config;
}

export function getConfig(): AppConfig {
  if (!config) throw new Error('config not loaded');
  return config;
}
