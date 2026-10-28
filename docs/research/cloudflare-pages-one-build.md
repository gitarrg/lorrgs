# Cloudflare Pages: branch previews, env vars, one build for many backends

Research for issue #99 (map #97). Primary sources only: Cloudflare Pages docs (fetched 2026-10-28) and the `lorrgs-frontend` source (`~/wow/lorrgs-frontend`, HEAD `e76bab2`) plus the backend files that feed it.

## Answer in short

- One preview build can serve all three Game Versions. The frontend already picks its backend at runtime; `VITE_BACKEND_URL` only sets the initial/default backend.
- A branch deploy of the existing `lorrgs-frontend` project gets a stable alias `<branch>.lorrgs-frontend.pages.dev` (branch name lowercased, non-alphanumerics become `-`).
- Env vars can be set separately for Production and Preview in the dashboard. Vite inlines `VITE_*` at build time, so the Preview value must be set before the preview build runs.
- Not determinable from the repos: whether the existing project is Git-integrated or Direct Upload. This decides how a branch deploy is triggered (see "Open questions").

## 1. Branch alias URLs

- Format `<branch>.<project>.pages.dev`; "Branch name aliases are lowercased and non-alphanumeric characters are replaced with a hyphen" (`fix/api` -> `fix-api.<project>.pages.dev`). The alias "always maps to the latest commit of that branch"; per-deployment hash URLs stay reachable. Source: https://developers.cloudflare.com/pages/configuration/preview-deployments/
- Preview URLs are public by default; an optional Access policy (Settings > General) can restrict previews only (same page).
- The docs page does not state a branch-name length limit.

## 2. Env vars scoped to preview vs production

- Dashboard: "Set your environment variables directly within the Cloudflare dashboard for both your production and preview environments"; applied "at runtime and build-time". Settings > Variables and Secrets. Source: https://developers.cloudflare.com/pages/functions/bindings/ (the fetched text does not spell out the per-environment UI; verify in the dashboard).
- Build-system variables injected by default include `CF_PAGES`, `CF_PAGES_BRANCH`, `CF_PAGES_URL` (usable to vary a build per branch). Source: https://developers.cloudflare.com/pages/configuration/build-configuration/
- Consequence for us: `VITE_BACKEND_URL` is read via `import.meta.env` and baked into the bundle (`src/constants.ts`). A Preview-scoped `VITE_BACKEND_URL` therefore only works if set before the preview build; changing it later needs a rebuild. Without a Preview value, `.env.production` (`https://api2.lorrgs.io`, committed in the frontend repo) applies, so a preview would talk to prod.

## 3. How a branch deploy is triggered

- Git integration: "automatically deploy your code every time you push a change to a branch"; PRs from the same repo get a unique preview URL; pushing a new non-production branch also produces a preview. Fork PRs do not. Source: https://developers.cloudflare.com/pages/configuration/git-integration/ and the preview-deployments page.
- Preview branch control (Build > Branch control): "All non-Production branches", "None", or "Custom branches" with include/exclude wildcards (excludes evaluated first, then includes). Source: https://developers.cloudflare.com/pages/configuration/branch-build-controls/ . Useful to restrict previews to e.g. a single `dev` branch.
- Wrangler / Direct Upload: `npx wrangler pages deploy <DIR> --branch=<BRANCH_NAME>` creates/updates a preview with alias `<BRANCH_NAME>.<PROJECT_NAME>.pages.dev`; omitting `--branch` (outside a git workspace) deploys to production. Source: https://developers.cloudflare.com/pages/get-started/direct-upload/
- A Direct Upload project cannot switch to Git integration later, and a Git project "cannot switch to Direct Upload"; the alternative for Git projects is to disable automatic deployments and use Wrangler. Same sources.
- In the frontend repo there is no `wrangler.*`, no `.github/` workflow and no deploy script (only `scripts/convert_images`), and `package.json` only has `vite build`. That points to Git integration, but it is not proof.

## 4. Can one preview build serve all three Game Versions?

Yes, by the frontend's existing design:

- `src/api.ts`: `backend_url = localStorage["lorrgs_backend_url"] || BACKEND_URL`; `get_backend_url()` / `set_backend_url(url|null)` read and write it. Every request is `backend_url + path`.
- `src/store/game_versions.ts`: on load, `fetch_data("/api/game_versions")` against the current backend. If that fails and the current backend is not the build-time default, it resets via `set_backend_url(null)` and retries the default. `get_selectable_game_versions` shows versions that are active or have a non-empty `api_url`.
- `switch_game_version(gv)`: if `gv.api_url` is set, `set_backend_url(gv.api_url)` and `window.location.assign(target)` (full reload). So switching version just re-points the backend; no rebuild.
- Backend side: `lorrgs_api/routes/api_game_versions.py` returns each version's `api_url` (from `LORRGS_API_URL_<NAME>`, `lorgs/game_version.py`); a version without one is not offered. CORS already allows `https://<branch>.lorrgs-frontend.pages.dev` (`lorrgs_api/middlewares/cors_middleware.py`, tested in `test/test_api/test_cors_and_cache.py`).
- localStorage is per origin, so a preview alias remembers its own backend choice independently of `lorrgs.io`.

So the dev stack needs: (a) preview build with `VITE_BACKEND_URL` = the dev retail API; (b) the dev retail API's `/api/game_versions` returning `api_url`s for retail, mists and forever (set `LORRGS_API_URL_*` on those Lambdas). No frontend code change is needed for runtime backend selection.

Caveats found in the frontend:

- `useVersionSwitch.ts` has `MOCK_VERSIONS`/`DISPLAY` using the name `classic_mop`, while the backend renamed that Game Version to `mists` (commit `6a06c37`). `DISPLAY` is keyed by name, so a `mists` entry would get no display title/order override (falls back to the backend title and order 99) and the icon (picked by name, see `WowLogo`) may be missing. Check before relying on the Mists tab.
- If the remembered backend becomes unreachable the app only falls back when `/api/game_versions` fails; a reachable-but-wrong backend is not detected.

## Open questions (not answerable from primary sources available here)

1. Is the `lorrgs-frontend` Pages project Git-integrated or Direct Upload? Check the dashboard (Settings > Builds / Build configuration). If Git: pushing a `dev` branch is enough and Preview branch control can limit it. If Direct Upload: CI must run `wrangler pages deploy dist --branch=<name>` with a Preview-scoped build.
2. Whether the dashboard already has `VITE_BACKEND_URL` set for Production and/or Preview (that would override `.env.production`).
3. The Cloudflare docs fetched do not state whether Preview env var values can differ from Production beyond the sentence quoted in section 2; confirm in the dashboard UI.
