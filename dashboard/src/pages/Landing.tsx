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
  ['Amazon SNS', 'emails the supervisor, then the backup contact'],
  ['Amazon Bedrock', 'drafts the incident report from logged facts only'],
  ['Cognito', 'signs supervisors in'],
  ['CloudWatch + X-Ray', 'tracks samples, latency, transitions and errors'],
];

export function Landing() {
  return (
    <>
      <PublicHeader />
      <main className="landing">
        <section className="hero">
          <div className="hero-copy">
            <h1>Heat strain for every wearer, not one number for everyone.</h1>
            <p>WristHeat reads each person's smartwatch, estimates their heat strain on AWS, and tells the supervisor who to stop.</p>
            <div className="hero-ctas">
              <Link className="btn btn-primary" to="/demo">See the live demo</Link>
              <Link className="btn" to="/console">Supervisor sign-in</Link>
            </div>
          </div>
          <figure className="hero-visual">
            <img className="hero-shot" src="/landing/command.png" width={1232} height={978}
                 alt="Supervisor console: group status counts, a list of who needs action now, and live trainee cards" />
            <img className="hero-watch" src="/landing/watch-amber.png" width={450} height={450}
                 alt="Galaxy Watch showing SLOW DOWN with advice to drink water" />
          </figure>
        </section>

        <section className="why">
          <p className="why-fact">In August and September 2024, 12 candidates died during a 10 km excise constable recruitment run in Jharkhand.</p>
          <p className="why-body">
            A heat warning gives everyone in a place the same number. The person running cannot tell when their own body is at its limit,
            and neither can the person supervising them. <a href="https://www.deccanherald.com/amp/story/india%2Fjharkhand%2Fhumidity-lack-of-health-screening-change-in-rules-some-reasons-behind-12-deaths-at-jharkhand-recruitment-drive-report-3181567" target="_blank" rel="noreferrer">Source: Deccan Herald</a>
          </p>
        </section>

        <section className="lifecycle" aria-label="How a session runs">
          <article className="phase phase-wide">
            <div>
              <h2>Before the session</h2>
              <p>Plan around the heat. A 24-hour heat-flag forecast for your site, the best window to train, and the US Army work, rest and water guidance for today's flag.</p>
            </div>
            <img src="/landing/today.png" width={1232} height={265} alt="Today panel: hourly heat flags, best window, and work/rest and water table for a YELLOW flag" />
          </article>
          <article className="phase phase-split">
            <div>
              <h2>During the session</h2>
              <p>Each watch streams heart rate every 5 seconds. WristHeat estimates a core-temperature trend and strain index, buzzes the wrist when strain rises, and tells the supervisor who needs action.</p>
            </div>
            <div className="watch-row">
              <img src="/landing/watch-calibrating.png" width={450} height={450} alt="Watch calibrating resting heart rate" />
              <img src="/landing/watch-amber.png" width={450} height={450} alt="Watch telling the wearer to slow down" />
              <img src="/landing/watch-recovered.png" width={450} height={450} alt="Watch confirming recovery" />
            </div>
          </article>
          <article className="phase phase-wide phase-after">
            <img src="/landing/report.png" width={1280} height={627} alt="Session report: time in each state, peaks, and incident response times" />
            <div>
              <h2>After the session</h2>
              <p>Keep the record. Unanswered alerts escalate to a backup contact, an incident closes only when the data confirms recovery, and every session prints as a duty-of-care report.</p>
            </div>
          </article>
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
          <h2>Watch a simulated group run, live.</h2>
          <Link className="btn btn-primary" to="/demo">See the live demo</Link>
        </section>
      </main>
      <Footer />
    </>
  );
}
