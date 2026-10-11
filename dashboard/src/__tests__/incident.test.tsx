import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../api';
import { AlertBanner } from '../components/AlertBanner';
import { hhmm } from '../format';
import { IncidentDetail } from '../pages/IncidentDetail';
import { HONESTY, Method } from '../pages/Method';
import type { Incident, IncidentSummary } from '../types';
import { NOW } from './fixtures';

vi.mock('../api', async () => {
  const actual = await vi.importActual<typeof import('../api')>('../api');
  return {
    ApiError: actual.ApiError,
    ackIncident: vi.fn(),
    getIncident: vi.fn(),
  };
});

const summary = (over: Partial<IncidentSummary> = {}): IncidentSummary => ({
  incident_id: 'inc-sim-S3-a-1', trainee_id: 'S3', trainee_name: 'Kabir', trainee_kind: 'simulated',
  session_id: 'sim-S3-a', status: 'NOTIFIED', opened_at: NOW - 60000, closed_at: null, outcome: null,
  trigger: { psi: 7.2, core_est_c: 38.62, hr: 176, wbgt_c: 31.4, flag: 'YELLOW', pm25: 51, rule: 'psi>=7' },
  escalated_at: null, acked_at: null, acked_by: null,
  advice: { en: 'Stop now. Rest in shade and cool down with water.', hi: 'अभी रुकें। छाँव में आराम करें और पानी से शरीर ठंडा करें।' },
  ...over,
});

const incident = (over: Partial<Incident> = {}): Incident => {
  const s = summary({ status: 'CLOSED', outcome: 'recovered' });
  const { advice: _advice, ...rest } = s;
  return {
    ...rest, summary: s, audio: {}, console_url: 'https://ap-south-1.console.aws.amazon.com/states/home?region=ap-south-1#/v2/executions/details/arn',
    events: [{ t: NOW - 60000, type: 'OPENED', detail: 'RED entered (psi>=7)' }, { t: NOW, type: 'CLOSED', detail: 'recovered' }],
    metrics: { time_to_ack_s: 40, time_to_recovery_s: 600, minutes_in_red: 5, peak_psi: 7.6, peak_core_c: 38.71, escalated: true },
    report: { text: 'Kabir triggered a RED alert. Estimated values; not a medical assessment.', source: 'bedrock',
              model: 'apac.amazon.nova-lite-v1:0', generated_at: NOW },
    ...over,
  };
};

beforeEach(() => {
  vi.mocked(api.getIncident).mockResolvedValue(incident({ audio: { en: 'https://a/en.mp3', hi: 'https://a/hi.mp3' } }));
  vi.mocked(api.ackIncident).mockReset();
  vi.spyOn(window.HTMLMediaElement.prototype, 'play').mockImplementation(() => Promise.reject(new Error('autoplay blocked')));
});

describe('Alert banner', () => {
  it('banner appears for an open incident and Acknowledge calls ackIncident once', async () => {
    vi.mocked(api.ackIncident).mockResolvedValue({ status: 'ACKNOWLEDGED' });
    render(<MemoryRouter><AlertBanner incidents={[summary()]} /></MemoryRouter>);
    expect(screen.getByText('Kabir: STOP — heat strain RED')).toBeInTheDocument();
    expect(screen.getByText('SIMULATED')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Acknowledge — cooling started' }));
    await waitFor(() => expect(screen.getByText(/^Acknowledged/)).toBeInTheDocument());
    expect(api.ackIncident).toHaveBeenCalledTimes(1);
  });

  it('second click is disabled while pending and shows the 409 message "Already acknowledged"', async () => {
    let reject!: (e: unknown) => void;
    vi.mocked(api.ackIncident).mockReturnValue(new Promise((_, rej) => { reject = rej; }));
    render(<MemoryRouter><AlertBanner incidents={[summary()]} /></MemoryRouter>);
    const btn = screen.getByRole('button', { name: 'Acknowledge — cooling started' });
    fireEvent.click(btn);
    expect(screen.getByRole('button', { name: /Acknowledging/ })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: /Acknowledging/ }));
    expect(api.ackIncident).toHaveBeenCalledTimes(1);
    await act(async () => reject(new api.ApiError(409, 'already_acknowledged', 'Already acknowledged')));
    expect(await screen.findByText('Already acknowledged')).toBeInTheDocument();
  });

  it('banner shows "Escalated to backup contact at hh:mm" when status ESCALATED', () => {
    const at = NOW - 10000;
    render(<MemoryRouter><AlertBanner incidents={[summary({ status: 'ESCALATED', escalated_at: at })]} /></MemoryRouter>);
    expect(screen.getByText(`Escalated to backup contact at ${hhmm(at)}`)).toBeInTheDocument();
  });

  it('toggles the advice to Hindi and shows both audio buttons', async () => {
    render(<MemoryRouter><AlertBanner incidents={[summary()]} /></MemoryRouter>);
    fireEvent.click(screen.getByRole('button', { name: 'हिंदी' }));
    expect(screen.getByText(summary().advice.hi)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '▶ Play alert (EN)' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '▶ हिंदी' })).toBeInTheDocument();
  });
});

describe('Incident page', () => {
  const renderAt = () => render(
    <MemoryRouter initialEntries={['/incidents/inc-sim-S3-a-1']}>
      <Routes><Route path="/incidents/:id" element={<IncidentDetail />} /></Routes>
    </MemoryRouter>);

  it('incident page labels the report source', async () => {
    renderAt();
    expect(await screen.findByText('Summary generated by Amazon Bedrock from the logged events below')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open in Step Functions console' })).toHaveAttribute('href', expect.stringContaining('console.aws.amazon.com'));
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('labels a template report', async () => {
    vi.mocked(api.getIncident).mockResolvedValue(incident({ report: { text: 'x', source: 'template', model: null, generated_at: NOW } }));
    renderAt();
    expect(await screen.findByText('Template summary (Bedrock unavailable)')).toBeInTheDocument();
  });
});

describe('Method page', () => {
  it('method page contains all six honesty statements verbatim', () => {
    render(<MemoryRouter><Method /></MemoryRouter>);
    expect(HONESTY).toHaveLength(6);
    const text = document.body.textContent ?? '';
    for (const s of [
      'WristHeat estimates a core-temperature trend from heart rate using ECTemp (US Army Research Institute of Environmental Medicine). It is not a thermometer and not a medical device.',
      'ECTemp was validated with chest-strap heart rate (about ±0.6 °C). It has not been validated on wrist optical sensors like the one in this watch, and studies found it misses many cases above 39 °C. Treat it as an early indicator, never as clearance to continue.',
      'WBGT is computed for open ground in sun from Open-Meteo forecast data (Liljegren method). Shade, indoor and local conditions differ.',
      'The rules that combine strain with the heat flag are our own heuristic, not a published standard.',
      'Trainees marked SIMULATED are generated by our simulator. REPLAY shows a real session recorded earlier. LIVE is a real person wearing the watch now.',
      'ECTemp is patented (US 10702165). This is a non-commercial research prototype.',
    ]) {
      expect(text).toContain(s);
    }
  });
});
