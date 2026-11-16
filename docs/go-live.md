# Going live: what is ready, and what still has to happen

Last updated 2026-11-15. Branch `feature/cnap-ui-redesign`. Nothing is merged or deployed. MW approves every merge and every deploy.

## Ready in the app (tested on fictional data)

- **Reporting:** surveys and reports, My tasks, My history, reporting sessions, reminders, the administrator home, results, snapshots, exports, and the RPPR tables. Milestones 1 to 9 are done (docs/handoff.md).
- **Publications, talks, and grants:** each publication form shows the foreign components reminder (docs/decisions.md, 2026-11-15).
- **Member Hub Home and Funding:**
  - Funding has three pages: opportunities, Grant resources, and news.
  - Grant resources holds the eight questions, the funding labels, the NIH IDeA opportunities with links, and "Collaborators and co-authors abroad".
- **Top menu bar:** Reporting and Funding menus that list only pages the app has.
- **Site Visit RSVP:** a confirmation email with a calendar file, and staff counts with a CSV download.
- **Article photos:** news and events can carry a photo, shown only after a person approves it.
- **Home link counts:** anonymous per-day counts, with an administrator report.
- **Production settings:** `python manage.py check --deploy` reports no issues under `config.settings.prod`.
  - Secure cookies, HSTS, HTTPS redirect, and no debug output.
  - Production refuses to start without K-State's mail relay.
- **Code checks:** `ruff check .` is clean, and the test suite passes. `docs/data-dictionary.md` was regenerated for the new tables.
- **Backup and restore:** a restore drill on 2026-11-15 restored a full dump into a new database with identical counts: people, answers, Site Visit RSVPs, and the audit log.

## Decisions and work that K-State IT must settle first (no real data until these are done)

1. **Hosting:** a K-State VM, or a hosting service K-State approves (docs/deployment.md). The Render copy is a public test site for fictional data only.
2. **Security review** of the app by K-State IT, including:
   - the outbound calls: PubMed look-ups, and "Find the article's photo", which reads the article's page;
   - the emails the app sends.
3. **Single sign-on** through the K-State eID (docs/sso.md). Until then, the app uses its own sign-in links and passwords.
4. **Data classification and retention:**
   - the survey answers, including confidential mentoring answers;
   - the audit log;
   - the RSVP answers, including dietary needs and photo consent.
5. **Mail relay:** K-State's SMTP relay address, set in `EMAIL_URL`, and the From address.
6. **Backups off the host:** approved storage for the nightly dumps and the media volume. Keep 30 days.
7. **Scheduled jobs:** reminders, period emails, speaker surveys, and session clean-up (docs/deployment.md, Scheduled jobs).

## Decisions for MW before launch

- **Real records:** loading CNAP's real people and roster, and any history from Piestar (docs/legacy-product-exports.md). This happens only on K-State's hosting after the security review. Never on the test copy.
- **Which prototype pages to build in the app for launch.** These exist only in the prototype today. Each needs new app work, and some need MW's approval of who may see what:
  - Community: the member directory, profiles, threads, announcements, alumni, and past speakers. Members can't see each other in the app today, so this is a permissions decision.
  - Events calendar and the NeuroSync page, with sign-up forms instead of emails, and a weekly flyer.
  - The Site Visit page and the photo gallery, including photo upload, which needs file storage.
  - Research stories, the proposal writing toolkit, and the core pages with request forms.
  - Mentor and mentee guides, which can stay fixed text and be revised once a year.
  - Search in the app.
- **Site Visit details:** dates, program blocks, and the RSVP closing date live in `apps/portal/sitevisit_views.py` until the Site Visit has its own records. Check them each year.
- **The "Talk through a draft" address:** the button opens an email to `EVALUATOR_EMAIL` until booking exists (docs/member-hub-homepage.md).

## The launch itself (after the above)

1. MW approves the merge of `feature/cnap-ui-redesign` into `main`.
2. On the K-State host:
   - set `.env` from `.env.example`, with `DJANGO_SETTINGS_MODULE=config.settings.prod`, `UI_PROTOTYPE=true` and `UI_PROTOTYPE_ONLY=true` for the Member Hub design, and `EMAIL_URL`;
   - run `make up` (migrations apply on start), then `make seed` for reference data only, never `--fictional`, and `make superuser`;
   - put nginx in front with the K-State certificate (docs/deployment.md).
3. Run `python manage.py check --deploy` and `make test` on the host. Then sign in as a test member and as an administrator.
4. Schedule the jobs and the nightly backup. Run one restore drill on the host.
5. Load the real roster, then open the first reporting session.
