# QuBins

[![Build matrix](https://github.com/JanLahmann/qubins/actions/workflows/build-matrix.yml/badge.svg)](https://github.com/JanLahmann/qubins/actions/workflows/build-matrix.yml)

> **QuBins** — the place for your QuBits: prebuilt quantum compartments, pick
> one, run your Qiskit notebook on (my)binder or as a container ("bin").

Currently published: 7 Qiskit minors × 2 flavors × 2 architectures =
28 multi-arch images, daily-rebuilt, Trivy-gated, cosign-signed.

Docker images and Binder URLs for specific Qiskit versions, so you can spin up
a Jupyter environment running exactly the Qiskit version you need.

Two flavors per Qiskit version:

- **small** — `qiskit` + `qiskit-aer` + `qiskit-ibm-runtime`. Lean image,
  fast `docker pull`.
- **xl** — broad environment based on
  [Qiskit-documentation's notebook tester](https://github.com/JanLahmann/Qiskit-documentation/blob/main/scripts/nb-tester/requirements.txt):
  `qiskit[all]`, all `qiskit-addon-*`, `qiskit-experiments`,
  `qiskit-ibm-transpiler[ai-local-mode]`, `qiskit-serverless`,
  `qiskit-ibm-catalog`, a scientific stack (`scipy`, `scikit-learn`,
  `pyscf`, `plotly`, `sympy`, `ffsim`, `gem-suite`, `python-sat`,
  `pandas`), plus `pylatexenc` for LaTeX rendering and `nbgitpuller`
  for git-backed notebook distribution. Qiskit-ecosystem packages are
  pinned; the rest is resolved by pip. Notebooks from the Qiskit
  documentation site should run unmodified. On arm64,
  `qiskit-ibm-transpiler` and `gem-suite` are omitted because they
  lack aarch64 wheels and need a Rust/C++ toolchain to build.

## Versions

| Qiskit  | Flavor | Binder | Docker |
| ------- | ------ | ------ | ------ |
| latest  | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/latest-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:latest-small` |
| latest  | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/latest-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:latest-xl` |
| 2.4     | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.4-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.4-small` |
| 2.4     | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.4-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.4-xl` |
| 2.3    | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.3-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.3-small` |
| 2.3    | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.3-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.3-xl` |
| 2.2    | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.2-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.2-small` |
| 2.2    | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.2-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.2-xl` |
| 2.1    | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.1-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.1-small` |
| 2.1    | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.1-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.1-xl` |
| 2.0    | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.0-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.0-small` |
| 2.0    | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/2.0-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.0-xl` |
| 1.4     | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/1.4-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:1.4-small` |
| 1.4     | xl\*   | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/qubins/1.4-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:1.4-xl` |

`latest` aliases the current Qiskit minor (today: `2.4`); the alias is
updated when a new minor ships. The bare `:latest` tag (what Docker
pulls when no tag is specified) is `latest-small`.

\* `1.4-xl` is a reduced set: `qiskit-addon-*`, `qiskit-serverless`,
`qiskit-ibm-catalog`, and `qiskit-ibm-transpiler` are 2.x-only and not
included. Contents: qiskit 1.4 core + aer + ibm-runtime + experiments
(unpinned, resolved against 1.x) + the same scientific stack as 2.x-xl.

Older Qiskit minors `1.0`/`1.1`/`1.2`/`1.3` are no longer published.
They carried unfixable QPY-deserialisation CVEs (RCE in `< 1.4.2`,
DoS in `< 1.3.0`) and were holding the base image back to a
python-3.12 stream with a much larger CVE backlog. Use `1.4` if you
need a 1.x environment, or one of the 2.x tags for any new work.

Images are published as multi-arch manifests covering `linux/amd64` and
`linux/arm64` (Apple Silicon, Graviton). Both arches must build for a
release to publish; addons that lack arm64 wheels are arch-gated in the
relevant `requirements.txt` (e.g. `qiskit-ibm-transpiler` and `gem-suite`
in 2.x-xl).

For users not using Docker or Binder:

```
pip install "qiskit~=2.4.0"
```

## Run on your laptop (Docker)

Pull and start any tag, mapping Jupyter's port:

```sh
docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:latest-small
```

Watch the container's stdout — Jupyter prints a tokenised URL once
ready, looking like:

```
http://127.0.0.1:8888/lab?token=<long-hex-string>
```

Open that URL in your browser. The token is required on first connect.

To work on notebooks already on your laptop, mount your folder into
the container's workspace:

```sh
docker run --rm -p 8888:8888 \
  -v "$PWD:/home/jovyan/work" \
  ghcr.io/janlahmann/qiskit:latest-small
```

Jupyter runs as the unprivileged `jovyan` user (UID 1000); on Linux,
either make the host directory readable/writable by that UID or pass
`--user $(id -u):$(id -g)` to match your own. Add `-d` if you want it
detached, and `--name qubins` if you want to `docker stop qubins` later.

## Pull your own notebook repo (nbgitpuller)

The **xl** images bundle [nbgitpuller](https://github.com/jupyterhub/nbgitpuller),
which lets a Binder URL auto-clone a notebook repo into the running
session on first launch. The URL shape:

```
https://mybinder.org/v2/gh/JanLahmann/qubins/latest-xl?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252FYOU%252FYOUR-REPO%26urlpath%3Dlab%252Ftree%252FYOUR-REPO%252Fnotebook.ipynb
```

The least-painful way to build one is the
[nbgitpuller link generator](https://nbgitpuller.readthedocs.io/en/latest/link.html):
set *JupyterHub URL* to `https://mybinder.org/v2/gh/JanLahmann/qubins/<tag>`
(e.g. `latest-xl` or `2.4-xl`), paste your notebook repo URL, optionally
add a default file path, and copy the result. Share that URL — anyone
who clicks lands in a fresh QuBins session with your notebooks already
checked out.

## How it works

`Dockerfile` is parameterised by `QISKIT_VERSION` (which is really a
`<qiskit-minor>-<flavor>` build target) and installs the dependency list at
`versions/<target>/requirements.txt`. The `build-matrix.yml` workflow has
three stages:

1. **build + scan** — for each `<target>`, build an image per architecture
   on a native runner (`ubuntu-latest` for amd64, `ubuntu-24.04-arm` for
   arm64), load the result into the local docker daemon, and run Trivy
   against it (HIGH/CRITICAL with available fixes block the run). A
   final `RUN python -c 'import qiskit; from qiskit import QuantumCircuit;
   QuantumCircuit(2).measure_all()'` smoke test catches wheels that
   resolve cleanly but break at import. The base image is force-pulled
   so security fixes flow through instead of riding on the GHA layer
   cache. This stage runs on every branch.
2. **publish to GHCR** (only on `main` / `workflow_dispatch`) — re-run
   the build with `push: true` so `docker/build-push-action` produces
   the SLSA provenance attestation alongside `ghcr.io/.../qiskit:<target>-<arch>`.
   All layers are cache hits from step 1, so this is fast.
3. **manifest + sign** (only on `main` / `workflow_dispatch`) — combine
   the per-arch tags into a multi-arch `ghcr.io/.../qiskit:<target>` with
   `docker buildx imagetools create`, sign the manifest with cosign
   keyless OIDC, then force-sync a per-target stub branch containing
   only `binder/Dockerfile` (a one-line `FROM ghcr.io/...` reference).
   Targets matching the `LATEST_QISKIT` env var also get a
   `latest-<flavor>` tag and stub branch.

mybinder consumes the stub branch and pulls the pre-built image instead of
rebuilding the dep tree from scratch (cold start ~30s).

### Staying current

- A daily cron at **04:00 UTC** (= 05:00 CET) reruns the full matrix on
  `main`, so upstream base-image CVE fixes flow into published images
  within a day even when no one pushes a commit.
- Dependabot watches three ecosystems: the docker base image, the GHA
  action versions, and the pip pins in the `LATEST_QISKIT` minor's
  `requirements.txt` files. Each Dependabot PR runs through the same
  Trivy + smoke gate.
- A second daily workflow (`detect-new-qiskit.yml`, also at 04:00 UTC)
  polls PyPI for the latest qiskit version. If a new minor appears,
  the workflow auto-scaffolds `versions/<X.Y>-{small,xl}/`, updates
  the matrix + `LATEST_QISKIT` + `dependabot.yml` directories + README,
  and opens a PR. The xl flavor commonly needs a human nudge to relax
  addon pins that don't yet support the new minor.

## Verifying images

Every multi-arch tag is signed via cosign keyless OIDC:

```
cosign verify ghcr.io/janlahmann/qiskit:2.4-small \
  --certificate-identity-regexp='^https://github.com/JanLahmann/(qubins|containers4qiskit)/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com
```

Build provenance attestations are produced automatically by
`docker/build-push-action`; see them via `docker buildx imagetools
inspect ghcr.io/.../qiskit:<tag> --format '{{ json .Provenance }}'`.

## Adding a new Qiskit minor

The detector workflow handles this automatically: when PyPI ships a new
minor, it opens a `bot/qiskit-<X.Y>` PR with the small + xl scaffolding,
matrix entries, `LATEST_QISKIT` bump, `dependabot.yml` directories, and
README rows. Review the PR — usually the xl needs a couple of addon
pins relaxed because addons lag the qiskit minor — and merge.

If you ever need to scaffold by hand: create
`versions/<X.Y>-{small,xl}/requirements.txt`, add the entries to both
matrix lists in `.github/workflows/build-matrix.yml`, bump
`LATEST_QISKIT`, swap the `dependabot.yml` pip directories, and
prepend two rows to the table above. `.github/scripts/scaffold-new-qiskit.py`
does all of this in one shot if you set `MINOR` and `VERSION` in env.

## License & acknowledgements

Apache-2.0. See [LICENSE](LICENSE).

Qiskit is a trademark of IBM. This project is independent and not
affiliated with IBM; it just packages the open-source Qiskit
distributions for convenient consumption.
