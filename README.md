# NEXKO Renewable Solutions — website

Static, single-page site. No build step.

```
python3 -m http.server 5173   # then open http://localhost:5173
```

Deploy by uploading `index.html` and `assets/` to any static host (Netlify, Vercel, Cloudflare Pages, cPanel).

- `index.html` — all content
- `assets/styles.css` — design
- `assets/main.js` — nav, scroll reveals, enquiry form (opens email or WhatsApp; no server needed)
- `assets/img/` — photography from Unsplash (free commercial licence), logo from the existing site

Swap in real project photos by replacing files in `assets/img/` with the same names.

## Brand

Logo: **Flux**. Three swept rotor blades in a sunrise gradient (#ffc53d → #ff6a1f → #e2283c), next to a geometric NEXKO wordmark in ink (#0b1220).

`assets/brand/`
- `nexko-logo.svg` / `nexko-logo-white.svg`: primary lockups for light and dark backgrounds
- `nexko-logo-tagline*.svg`: lockups with "RENEWABLE SOLUTIONS" (the tagline is live text set in Inter; outline it in Illustrator before sending to print)
- `nexko-mark.svg`: symbol only
- `nexko-icon.svg`, `nexko-icon-512.png`, `apple-touch-icon.png`, `favicon-64.png`: app and browser icons

Everything is generated from `brand/build.py`. Edit that and run `python3 brand/build.py` to regenerate. `brand/concepts.html` is the concept sheet.
