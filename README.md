# Tech Briefing PWA

A small installable web app for android phones. It includes live headline loading from Google News RSS through the AllOrigins public CORS proxy, a daily system-design concept, a C++/DSA exercise, and a local archive.

## Files
- `index.html`: app interface and logic
- `manifest.json`: installable app metadata
- `sw.js`: offline shell cache
- `icon.svg`: app icon

## Quick test
Open `index.html` in a browser. Some browsers block service workers and live RSS loading when opened as a local file; use the hosted setup below for full functionality.

## Host it free with GitHub Pages
1. Create a GitHub repository, e.g. `tech-briefing`.
2. Upload all four files to the repository root.
3. In repository Settings → Pages, choose deploy from branch `main`, folder `/ (root)`, and save.
4. Wait for the published URL shown by GitHub Pages.
5. On your Samsung, open that HTTPS URL in Chrome.
6. Tap Chrome ⋮ → Add to Home screen (or Install app if offered).
7. Name it `Tech Briefing`. The custom icon and standalone app window should appear.

## Limitations
- Live headlines require an internet connection and a third-party public RSS proxy; the proxy may be rate-limited or unavailable. The app provides direct Google News search links as a fallback.
- News freshness and article summaries are controlled by publishers and feed providers.
- The archive is saved in local browser storage on this device and may be cleared by browser data cleanup. It does not sync between devices.
- The system-design and coding items are currently curated starter content, not automatically generated or rotated each day.
- No background push notifications are configured.
