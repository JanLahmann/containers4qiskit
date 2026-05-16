// QuBins launch redirector.
//
// Reads query params, builds the appropriate mybinder URL using the
// same encoding logic as the landing page generator, and redirects.
// Supported params:
//   image=<tag>            (default: latest-xl)
//   repo=<github url>      repo loader (nbgitpuller)
//   branch=<ref>           optional, repo loader only
//   path=<subpath>         optional, repo loader only
//   file=<raw url>         single-file loader (jupyterlab-open-url-parameter)
//
// Precedence: `file` wins over `repo`; if neither, bare image launch.
//
// We use location.replace() so the redirector doesn't pollute the
// user's history. The destination URL is also rendered into the
// fallback section in case the redirect fails or the user wants to
// inspect it.

(() => {
  "use strict";
  const REPO = "QuBins/qiskit-images";
  const params = new URLSearchParams(location.search);

  const image  = (params.get("image") || "latest-xl").trim();
  const repo   = params.get("repo");
  const branch = params.get("branch");
  const path   = params.get("path");
  const file   = params.get("file");

  let url;
  if (file) {
    const inner = `lab?fromURL=${encodeURIComponent(file)}`;
    url = `https://mybinder.org/v2/gh/${REPO}/${image}?urlpath=${encodeURIComponent(inner)}`;
  } else if (repo) {
    let repoName = "repo";
    try {
      const u = new URL(repo);
      const parts = u.pathname.replace(/\.git$/, "").split("/").filter(Boolean);
      repoName = parts[parts.length - 1] || "repo";
    } catch (_) { /* fall back to default repoName */ }
    const inner = new URLSearchParams();
    inner.set("repo", repo);
    if (branch) inner.set("branch", branch);
    inner.set("urlpath", path ? `lab/tree/${repoName}/${path}` : `lab/tree/${repoName}`);
    const innerEncoded = encodeURIComponent("git-pull?" + inner.toString());
    url = `https://mybinder.org/v2/gh/${REPO}/${image}?urlpath=${innerEncoded}`;
  } else {
    url = `https://mybinder.org/v2/gh/${REPO}/${image}`;
  }

  // Reveal fallback first (in case the redirect is blocked) and only
  // then trigger location.replace. If a browser strips the redirect
  // (rare), the link is already wired.
  document.getElementById("launch-link").href = url;
  document.getElementById("launch-url").textContent = url;
  document.getElementById("fallback").style.display = "block";

  // Fire-and-forget Umami event: which image/mode actually got
  // launched. Best-effort — guard for the script not loading.
  try {
    if (window.umami && typeof window.umami.track === "function") {
      const mode = file ? "file" : (repo ? "repo" : "bare");
      window.umami.track("launch-redirect", { image, mode });
    }
  } catch (_) { /* analytics is best-effort */ }

  // Brief delay so the user can see the destination before the jump.
  setTimeout(() => { location.replace(url); }, 400);
})();
