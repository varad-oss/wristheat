import { Link } from 'react-router-dom';
import { Footer } from '../components/Footer';
import { PublicHeader } from '../App';
import { HONESTY } from './Method';

const AWS: [string, string][] = [
  ['API Gateway', 'receives every watch reading and guards the supervisor routes'],
  ['Lambda', 'runs the strain model, the heat-data fetch and the workflow steps'],
  ['DynamoDB', 'keeps readings, per-minute estimates, sessions and incidents'],
  ['Step Functions', 'escalates an unanswered alert and waits for confirmed recovery'],
  ['EventBridge Scheduler', 'refreshes site heat and air quality every 10 minutes'],
  ['Amazon Polly', 'speaks the alert in English and Hindi'],
  ['Amazon SNS', 'emails the supervisor, a backup contact or a solo wearer\'s emergency contact'],
  ['Amazon Bedrock', 'drafts the incident report from logged facts only'],
  ['Cognito', 'signs in supervisors and wearers, each to their own view'],
  ['CloudWatch + X-Ray', 'tracks samples, latency, transitions and errors'],
];

const STATS: { figure: string; who: string; text: string; source: string; url: string; wide?: boolean }[] = [
  { figure: '2.41 billion', who: 'Outdoor and manual workers', wide: true,
    text: 'workers face excessive heat at work. About 19,000 die and 22.85 million are injured each year.',
    source: 'ILO, 2024', url: 'https://www.ilo.org/publications/ensuring-safety-and-health-work-changing-climate' },
  { figure: '23 students', who: 'School children', wide: true,
    text: 'collapsed after a morning assembly in Chitrakoot, Uttar Pradesh, in August 2024. In May, students fainted at assemblies across Bihar.',
    source: 'Careers360', url: 'https://news.careers360.com/uttar-pradesh-23-students-faint-at-school-in-ups-chitrakoot-due-heat' },
  { figure: '12 candidates', who: 'Recruitment and military training',
    text: 'died on a 10 km excise constable recruitment run in Jharkhand in 2024. The US armed forces logged 471 heat strokes that year.',
    source: 'MSMR, June 2025', url: 'https://health.mil/News/Articles/2025/06/01/MSMR-Heat-Illness-2025' },
  { figure: '1,301 deaths', who: 'Pilgrims, runners and crowds',
    text: 'during the 2024 Hajj in heat up to 51.8 °C. The 2007 Chicago Marathon was halted; one runner died and about 300 were treated.',
    source: 'Hajj 2024 summary', url: 'https://en.wikipedia.org/wiki/2024_Hajj_extreme_heat_disaster' },
  { figure: '40,984 cases', who: 'India, summer 2024',
    text: 'of suspected heatstroke and 114 deaths between 1 March and 18 June 2024, from hospital reporting alone.',
    source: 'NCDC via South First', url: 'https://thesouthfirst.com/health/summers-wrath-114-heatwave-deaths-reported-nearly-41000-cases-of-suspected-heatstroke' },
];

export function Landing() {
  return (
    <>
      <PublicHeader />
      <main id="main" className="landing">
        <section className="hero">
          <div className="hero-copy">
            <h1>Heat strain for every wearer, not one number for everyone.</h1>
            <p>WristHeat reads each person's own smartwatch, estimates their heat strain on AWS, and warns them and whoever is responsible.</p>
            <div className="hero-ctas">
              <Link className="btn btn-primary" to="/demo">See the live demo</Link>
              <Link className="btn" to="/console">Sign in</Link>
            </div>
          </div>
          <figure className="hero-visual">
            <img className="hero-shot" fetchPriority="high" src="/landing/command.png" width={1232} height={978}
                 alt="Supervisor console: group status counts, a list of who needs action now, and live trainee cards" />
            <img className="hero-watch" src="/landing/watch-amber.png" width={450} height={450}
                 alt="Galaxy Watch showing SLOW DOWN with advice to drink water" />
          </figure>
        </section>

        <section className="scale" aria-labelledby="scale-title">
          <h2 id="scale-title" className="scale-lead"><span className="num">489,000</span> people die from heat in an average year.</h2>
          <p className="scale-sub">A heat warning gives everyone the same number. The people below cannot tell when their own body is at its limit, and neither can the person responsible for them.</p>
          <div className="scale-grid">
            {STATS.map((x) => (
              <article key={x.who} className={`stat ${x.wide ? 'stat-wide' : ''}`}>
                <p className="stat-figure num">{x.figure}</p>
                <h3>{x.who}</h3>
                <p>{x.text} <a href={x.url} target="_blank" rel="noreferrer">{x.source}</a></p>
              </article>
            ))}
          </div>
        </section>

        <section className="modes" aria-label="Two ways to use WristHeat">
          <article className="mode mode-solo">
            <div>
              <h2>On your own</h2>
              <p>Out for a long run, a hike or a shift alone. Your watch tells you to slow down, then to stop. If you reach RED and don't confirm you have stopped within 90 seconds, your emergency contact is emailed.</p>
            </div>
            <div className="watch-row">
              <img loading="lazy" src="/landing/watch-calibrating.png" width={450} height={450} alt="Watch measuring resting heart rate before the run" />
              <img loading="lazy" src="/landing/watch-amber.png" width={450} height={450} alt="Watch telling the wearer to slow down and drink water" />
              <img loading="lazy" src="/landing/watch-recovered.png" width={450} height={450} alt="Watch confirming recovery after rest" />
            </div>
          </article>
          <article className="mode mode-group">
            <img loading="lazy" src="/landing/report.png" width={1280} height={627} alt="Session report: time in each state, peaks, and incident response times" />
            <div>
              <h2>With a group</h2>
              <p>A coach, a PE teacher, a drill instructor or a site supervisor sees every wearer at once and who needs action now. Unanswered alerts escalate, incidents close only when the data confirms recovery, and every session prints as a record.</p>
            </div>
          </article>
        </section>

        <section className="plan">
          <h2>Plan around the heat, before anyone starts</h2>
          <p>A 24-hour heat-flag forecast for the site, the best window to train, and the US Army work, rest and water guidance for today's flag.</p>
          <img loading="lazy" src="/landing/today.png" width={1232} height={265} alt="Today panel: hourly heat flags, best window, and the work/rest and water table for a YELLOW flag" />
        </section>

        <section className="aws">
          <h2>Built on AWS, end to end</h2>
          <dl>
            {AWS.map(([svc, job]) => <div key={svc}><dt>{svc}</dt><dd>{job}</dd></div>)}
          </dl>
        </section>

        <section className="limits">
          <h2>What WristHeat is not</h2>
          <ul>{HONESTY.map((s, i) => <li key={i}>{s}</li>)}</ul>
          <p><Link to="/method">Read how the estimate works</Link></p>
        </section>

        <section className="closing">
          <h2>Watch a simulated group train, live.</h2>
          <Link className="btn btn-primary" to="/demo">See the live demo</Link>
        </section>
      </main>
      <Footer />
    </>
  );
}
