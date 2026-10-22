# Tech Briefing v4 — reliable scheduled RSS ingestion

This update removes browser-side RSS proxy fetching. A GitHub Actions workflow fetches publisher feeds server-side each morning and publishes `data/headlines.json` to the same GitHub Pages site. The app reads that same-origin JSON file, avoiding browser CORS restrictions and public proxy dependence during normal use.

## Deploy to the SAME repository
1. Extract this ZIP.
2. In the existing GitHub repository, upload/replace all files from this package, including the hidden `.github/workflows/update-feeds.yml` file and the `scripts/` and `data/` folders. On GitHub web, use Add file → Upload files; ensure the `.github/workflows` path is preserved. If uploading hidden folders is awkward, use GitHub Desktop or git.
3. Commit to the branch that GitHub Pages publishes.
4. Open the repository's Actions tab → `Update Tech Briefing feeds` → `Run workflow` → `Run workflow`.
5. Wait for a green check. Verify `data/headlines.json` now contains headlines and an updated timestamp.
6. Open your existing Tech Briefing app and tap Refresh. If stale, close it fully and reopen it; the service worker cache version is bumped to v4.
7. Confirm the GitHub Pages URL is unchanged so your existing home-screen icon still opens the app.

## Morning update
The workflow is scheduled for 08:00 India Standard Time (02:30 UTC) daily. GitHub scheduled workflows can start late and can be delayed; run manually if needed.

## Alerts
A PWA cannot reliably schedule a local notification for 8 AM while closed without a push service/server or native Android component. This app no longer falsely implies that enabling browser notifications schedules a morning alert. Set a daily Samsung Clock alarm labelled “Open Tech Briefing”. For true push notifications later, add a push provider (e.g. Firebase Cloud Messaging) and subscription endpoint.

## Limits
- Feed publishers can change/block feeds. The workflow logs failures per source and succeeds if at least one feed has content.
- `data/headlines.json` is committed to the repo, so public repo users can see it. Do not add secrets to the file.
- Daily system design and coding exercises rotate from curated built-in sets; they are not generated dynamically from the headlines.
- Archive remains local to the device/browser.
