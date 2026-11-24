# Going live on Render

Last updated 2026-11-24. MW chose Render (not K-State hosting) on 2026-11-24. MW approves every merge into `main`;
Render deploys `main` automatically, so a merge is a deploy.

## What Render runs (render.yaml)

- **Website** `cnap-hub`: the Django app on Render's Starter plan, with a 5 GB disk for uploaded files.
  Every start runs migrations, loads reference data (never fictional data), makes sure the first administrator
  exists, and collects static files.
- **Database** `cnap-hub-db`: PostgreSQL 16, Basic plan. Render backs it up daily.
- **Scheduled jobs**: publication and grant reminders (7:00 a.m.), reporting-session e-mails (8:00 a.m.),
  NeuroSync speaker surveys (every 10 minutes), and sign-in clean-up (3:00 a.m.). Times are Central standard time;
  Render runs schedules in UTC, so they shift an hour in daylight saving time.
- **Health check**: `/healthz`.

Approximate cost: about $7 (website) + $6 (database) + $1.25 (disk) + about $4 (four small scheduled jobs) a month,
plus Postmark (about $15 a month). Check Render's pricing page before signing up.

## Steps for MW (once)

1. **Postmark** (e-mail): create an account at postmarkapp.com, add a "server," verify the address the Hub sends
   from (a sender signature), and copy the server API token.
2. **Render**: sign up at render.com with the GitHub account that owns the repository, and add a payment method.
3. In Render: **New → Blueprint**, pick `mkdawills/CNAP_Reporting_Hub`, branch `main`. Render reads `render.yaml`
   and asks for these values:
   - `EMAIL_URL`: `smtp+tls://TOKEN:TOKEN@smtp.postmarkapp.com:587` (the Postmark token twice).
   - `DEFAULT_FROM_EMAIL`: for example `CNAP Member Hub <the verified address>`.
   - `ADMIN_EMAIL`, `ADMIN_FIRST_NAME`, `ADMIN_LAST_NAME`: MW's own, for the first administrator account.
4. Wait for the first deploy (about 5 minutes). Open `https://cnap-hub.onrender.com`, choose "E-mail me a sign-in
   link," and sign in.
5. Later, a domain: buy it, add it under the website's Settings → Custom Domains, then add the domain to
   `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `SITE_URL` in the `cnap-hub-settings` group.

## Before the first real records

- **Data approval (assumed until MW says otherwise):** profiles, publications, talks, and grants go in first.
  Reporting sessions, including confidential mentoring surveys, stay closed until K-State agrees the data can live
  outside K-State. Nothing opens a survey until an administrator opens a reporting session.
- **Accounts:** add people under Manage → People. Each person signs in with an e-mailed link.
- **Older records:** an administrator can enter publications, talks, and grants for any person ("entering for").
  A bulk import from earlier exports is a separate build (docs/legacy-product-exports.md).
- **Never** run `seed --fictional` on Render.

## Checks after each deploy

- `/healthz` answers "ok"; sign in as MW; open Home, My tasks, Funding, and an administrator screen.
- Render's Logs show no errors; the scheduled jobs' last runs succeeded.

## Still open

- Domain (MW): a free `onrender.com` address works until one is chosen.
- Member profiles with photo, research interests, and a short bio, and the member directory: built in the
  prototype only. The app's profile today holds department, title, ORCID, eRA Commons, and trainee level.
  Who may see whom is MW's decision before the directory is built.
- Single sign-on with the K-State eID is not available outside K-State hosting; sign-in links and passwords are used.
