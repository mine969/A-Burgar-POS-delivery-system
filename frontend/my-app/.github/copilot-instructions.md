# Copilot / AI Agent Instructions

Purpose: give an AI agent the minimum, actionable context needed to be productive in this Next.js app.

- **Project type:** Next.js (app router) project generated with `create-next-app`.
- **Location:** primary frontend source is in `app/` (Top-level `app/layout.js`, `app/page.js`).
- **Runtime libs:** `next` v15, `react` v19. Project uses Turbopack in `package.json` scripts.

Key files and what they mean
- `app/layout.js` — root layout. Imports `./globals.css`, sets up `next/font` (Geist) and CSS variables applied to `<body>`.
- `app/globals.css` — global styles. Intended to be imported once in `layout.js` (avoid re-importing per-page).
- `app/page.js` — top-level page. NOTE: currently this file incorrectly imports `global` from `'global.css'` (should be a relative import or removed since `layout.js` already imports the globals). Example fix below.
- `package.json` — scripts: `dev` -> `next dev --turbopack`, `build` -> `next build --turbopack`, `start` -> `next start`, `lint` -> `eslint`.
- `next.config.mjs`, `eslint.config.mjs`, `postcss.config.mjs`, and `Dockerfile` — inspect for build and runtime-specific overrides before changing build behavior.

Architecture & conventions (specific to this repo)
- Uses the App Router (`app/`) — prefer server components by default. Add `"use client"` at top of a file when a client component is required.
- Global styles: import in `app/layout.js` only. Do not import `globals.css` from each page or component.
- CSS imports must be relative in `app/` (e.g. `import "./globals.css"`), not bare specifiers like `'global.css'`.
- Fonts are configured with `next/font` in `layout.js` and applied via CSS variables. Keep that pattern when adding fonts.
- Scripts use Turbopack flags; keep `--turbopack` in `dev`/`build` scripts unless you have a reason to change bundler.

Developer workflows (how to run and validate changes)
- Run dev server: `npm run dev` (opens at http://localhost:3000). The dev script uses Turbopack.
- Build for production: `npm run build` then `npm start`.
- Lint: `npm run lint` (project has `eslint` configured; prefer using this script).
- Docker: a `Dockerfile` exists at project root — inspect for environment variables and runtime command if you change server behavior.

Examples & small fixes (copyable)
- Fix incorrect CSS import in `app/page.js` (current):

  ```diff
  -import global from 'global.css'
  +// globals are applied in layout.js; remove this OR use a relative path:
  +// import './globals.css'
  ```

- Add a client component: start file with `"use client"` and keep imports consistent.

What to watch for when editing
- Keep changes minimal and focused; preserve file style and existing patterns.
- If you change build or runtime config (`next.config.mjs`, Dockerfile), run `npm run build` locally to validate.
- When adding CSS or fonts, prefer the existing `next/font` + CSS variable approach in `layout.js`.

If anything is unclear, ask for:
- backend/API endpoints and environment variables used in runtime.
- where to deploy (Vercel vs custom Docker) if you need to change deployment settings.

After making changes, run the dev server and briefly confirm the affected page(s) load without console/build errors.
