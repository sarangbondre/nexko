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
