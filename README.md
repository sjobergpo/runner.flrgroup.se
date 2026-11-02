# Runner · runner.flrgroup.se

Marketing, support, and privacy website for **Runner**, the Apple Watch running app. English only. Static HTML and CSS; no runtime dependencies, JavaScript, trackers, cookies, or external fonts.

## App Store URLs

| App Store field | URL |
| --- | --- |
| Marketing URL | https://runner.flrgroup.se/ |
| Support URL | https://runner.flrgroup.se/support/ |
| Privacy Policy URL | https://runner.flrgroup.se/privacy/ |

App Store listing: https://apps.apple.com/app/runner-running-watch/id6816334642 (no country code, so Apple opens the visitor’s own storefront). The site’s App Store links use the campaign link `https://apps.apple.com/app/apple-store/id6816334642?pt=127207286&ct=website&mt=8`, so visits and downloads from the website appear under **Analytics → Acquisition → Campaigns** in App Store Connect. The JSON-LD `installUrl` keeps the plain listing URL. The public contact address is **runner@flrgroup.se**.

## Local preview and checks

```sh
python3 scripts/check_site.py
python3 -m http.server 8765 --directory site
```

Open http://localhost:8765/. The check verifies local links, fragment destinations, required pages, metadata, image descriptions, contact links, and self-hosted assets. No build step is needed.

Before publishing content changes, inspect the homepage, support, privacy, and 404 pages at phone, tablet, and desktop widths. Check keyboard focus and browser zoom. The original Runner app repository is separate and private; this public repository contains only website files and the selected public-facing artwork.

## GitHub Pages deployment

The workflow in `.github/workflows/pages.yml` checks the site on pull requests and deploys `site/` on relevant pushes to `main` or a manual **Publish website** run. The workflow uploads only `site/`, not the repository or app source. The `github-pages` environment is the deployment target.

In repository **Settings → Pages**, use **GitHub Actions** as the source. Set the custom domain to **runner.flrgroup.se**. Custom domains for Actions-based publishing are configured in Pages settings; a CNAME file in the source is not required.

### one.com DNS

Under the DNS records for **flrgroup.se**, create:

| Type | Hostname | Alias target | TTL |
| --- | --- | --- | --- |
| CNAME | `runner` | `sjobergpo.github.io` | Default (3600 seconds) |

The target does not include a repository name, path, or URL scheme. Configure the custom domain in GitHub before pointing the DNS record at it. Only the `runner` hostname is needed; the root, `www`, and other app subdomains retain their own configuration.

After DNS resolves and GitHub issues its certificate, enable **Enforce HTTPS** in Pages settings. Visit all three App Store URLs directly and check the certificate before using them in App Store Connect.

References: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [one.com CNAME records](https://help.one.com/hc/en-us/articles/360000803517-How-do-I-create-a-CNAME-record), [GitHub Pages IP logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection).

## Content and artwork maintenance

- Edit the HTML directly under `site/`. The shared header, footer, and metadata are repeated on the four pages; keep them consistent. Layout and color tokens are in `site/assets/style.css`.
- Update feature descriptions against the released app, especially purchase gating, requirements, permissions, controls, and sync. Do not describe unreleased capabilities as available.
- `watch-artwork.png` and `app-icon.png` come from Runner’s existing app assets. The watch hardware canvas is cropped with CSS using the same geometry as the app’s watch preview. It is overlaid with the real metric screenshot.
- The watch screen uses four 416 × 496 captures of the real watch view with example data, one per main metric: `watch-metrics.png` (PACE, cyan), `watch-average-pace.png` (AVG PACE, Midnight Blush), `watch-lap-pace.png` (LAP PACE, white) and `watch-altitude-gain.png` (ALT GAIN, yellow). Regenerate them in the app repo with `.img/screenshots_workflow/store-assets.sh website` and copy them from `.img/screenshots_workflow/captures/website/` (`website-lap-pace.png` becomes `watch-lap-pace.png`). The clock shows the simulator’s time, so start the run just after a minute boundary and check that all four show the same time.
- The homepage stacks the images and cycles through them with CSS in Double Tap order (`.watch-screen-alt`, 24 s cycle, about 6 s each). With reduced motion only the pace image is shown. To show fewer metrics, remove `.watch-screen-alt` images from `site/index.html` and adjust the cycle in `style.css`. Check the screen alignment and the accessible example values on the homepage after replacement.
- `social-preview.png` is the 1200 × 630 sharing image. Replace it when the headline or identity changes. Open Graph URLs intentionally point at the production custom domain.
- `app-store-badge.svg` is Apple’s official black “Download on the App Store” badge (en-us) from Apple Marketing Tools (toolbox.marketingtools.apple.com). Do not modify it.
- FLR Group is a brand, not a company. Refer to the developer as “we” or “us”; FLR Group appears only as the footer link.
- Keep `site/privacy/index.html` accurate when app or hosting data practices change and update its effective date. Saved Apple Health data is not deleted merely by removing Runner.

## Verification at initial publication

The initial site was checked in Safari at desktop, tablet, and phone widths. Core content and navigation require no JavaScript. Static checks cover every deployed page. Real workout behavior remains the app’s responsibility; this website does not change or validate sensor or HealthKit behavior.
