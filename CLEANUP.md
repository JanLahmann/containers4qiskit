# Cleanup TODO

Manual cleanup remaining after dropping Qiskit 1.0 / 1.1 / 1.2 / 1.3.
Delete this file once all items are checked off.

## Orphan stub branches

Eight `<X.Y>-<flavor>` branches still exist on the remote because the
local git proxy in this session denied `git push --delete`. Remove
them so they stop appearing on the branches page (mybinder URLs that
referenced them will 404 after deletion — desired).

From a local checkout with `gh` available:

```sh
for b in 1.0-small 1.0-xl 1.1-small 1.1-xl 1.2-small 1.2-xl 1.3-small 1.3-xl; do
  gh api -X DELETE "/repos/QuBins/qiskit-images/git/refs/heads/$b"
done
```

Or via the UI: <https://github.com/QuBins/qiskit-images/branches>
→ filter for `1.`, click the trash icon on each.

- [ ] `1.0-small`
- [ ] `1.0-xl`
- [ ] `1.1-small`
- [ ] `1.1-xl`
- [ ] `1.2-small`
- [ ] `1.2-xl`
- [ ] `1.3-small`
- [ ] `1.3-xl`

## Orphan GHCR package versions

The GHCR package `ghcr.io/qubins/qiskit` still has tags + per-arch
tags + cosign signatures published from the dropped versions. Delete
them at:

<https://github.com/orgs/QuBins/packages/container/qiskit/versions>

Tags to remove (each has an amd64 + arm64 sub-tag and a `sha256-...sig`
cosign signature; deleting the multi-arch manifest version usually
takes the children with it, but verify):

- [ ] `1.0-small`, `1.0-small-amd64`, `1.0-small-arm64`
- [ ] `1.0-xl`, `1.0-xl-amd64`, `1.0-xl-arm64`
- [ ] `1.1-small`, `1.1-small-amd64`, `1.1-small-arm64`
- [ ] `1.1-xl`, `1.1-xl-amd64`, `1.1-xl-arm64`
- [ ] `1.2-small`, `1.2-small-amd64`, `1.2-small-arm64`
- [ ] `1.2-xl`, `1.2-xl-amd64`, `1.2-xl-arm64`
- [ ] `1.3-small`, `1.3-small-amd64`, `1.3-small-arm64`
- [ ] `1.3-xl`, `1.3-xl-amd64`, `1.3-xl-arm64`

## Repo rename + landing page

- [ ] Rename the GitHub repo `containers4qiskit` → `qubins`. UI:
  Settings → Repository name → "Rename". Or:
  `gh repo rename qubins --repo QuBins/qiskit-images`.
  GitHub auto-redirects clones from the old URL; the README's
  mybinder URLs were already rewritten to point at the new name.
- [ ] Register `qubins.org`.
- [ ] Set up GitHub Pages for `qubins.org`:
  - Settings → Pages → set source (branch + `/docs` or `/` root).
  - Add `CNAME` file in the docs source with `qubins.org`.
  - Configure DNS at the registrar: `A` records to GitHub Pages
    IPs (185.199.108.153, .109.153, .110.153, .111.153) and an
    `AAAA` set, or a `CNAME` for `www.qubins.org` →
    `qubins.org`.
  - Enable "Enforce HTTPS" once DNS resolves.

## After all cleanup

- [ ] Delete this file (`git rm CLEANUP.md`)
- [ ] Delete the long-lived `claude/review-qiskit-versions-sketch-n5ecU`
  branch if it's served its purpose:
  `gh api -X DELETE /repos/QuBins/qiskit-images/git/refs/heads/claude/review-qiskit-versions-sketch-n5ecU`
