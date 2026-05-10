# QuBins

> **QuBins** — the place for your QuBits: prebuilt quantum compartments, pick
> one, run your Qiskit notebook on (my)binder or as a container ("bin").

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

## How it works

`Dockerfile` is parameterised by `QISKIT_VERSION` (which is really a
`<qiskit-minor>-<flavor>` build target) and installs the dependency list at
`versions/<target>/requirements.txt`. The `build-matrix.yml` workflow has
two stages:

1. **build** — for each `<target>`, build an image per architecture on a
   native runner (`ubuntu-latest` for amd64, `ubuntu-24.04-arm` for arm64),
   load the result into the local docker daemon, and run Trivy against
   it (HIGH/CRITICAL with available fixes block the run). The base image
   is force-pulled so security fixes flow through instead of riding on
   the GHA layer cache. The scan runs on every branch.
2. **publish to GHCR** (only on `main` / `workflow_dispatch`) — re-run
   the build with `push: true` so `docker/build-push-action` produces
   the SLSA provenance attestation alongside `ghcr.io/.../qiskit:<target>-<arch>`.
   All layers are cache hits from step 1, so this is fast.
3. **manifest** (only on `main` / `workflow_dispatch`) — combine the
   per-arch tags into a multi-arch `ghcr.io/.../qiskit:<target>` with
   `docker buildx imagetools create`, sign the manifest with cosign
   keyless, then force-sync a per-target stub branch containing only
   `binder/Dockerfile` (a one-line `FROM ghcr.io/...` reference).
   Targets matching the `LATEST_QISKIT` env var also get a
   `latest-<flavor>` tag and stub branch.

mybinder consumes the stub branch and pulls the pre-built image instead of
rebuilding the dep tree from scratch (cold start ~30s).

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

To add a new Qiskit version:

1. Create `versions/<X.Y>-small/requirements.txt` and
   `versions/<X.Y>-xl/requirements.txt`.
2. Add `<X.Y>-small` and `<X.Y>-xl` to the `matrix.version` list in
   `.github/workflows/build-matrix.yml`.
3. Add two rows to the table above.
4. To make the new version the `latest` alias, bump `LATEST_QISKIT` at
   the top of `.github/workflows/build-matrix.yml`.

## License

Apache-2.0. Qiskit itself is also Apache-2.0; see [LICENSE](LICENSE).
