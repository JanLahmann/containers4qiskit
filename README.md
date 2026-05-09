# containers4qiskit

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
  documentation site should run unmodified.

## Versions

| Qiskit | Flavor | Binder | Docker |
| ------ | ------ | ------ | ------ |
| 2.4    | small  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/containers4qiskit/2.4-small) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.4-small` |
| 2.4    | xl     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/containers4qiskit/2.4-xl) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.4-xl` |

Images are published as multi-arch manifests covering `linux/amd64` and
`linux/arm64` (Apple Silicon, Graviton). `2.4-xl` arm64 is best-effort —
if a pinned addon lacks arm64 wheels, only the `linux/amd64` variant is
published for that tag.

For users not using Docker or Binder:

```
pip install "qiskit~=2.4.0"
```

## How it works

`Dockerfile.template` is parameterised by `QISKIT_VERSION` (which is really a
`<qiskit-minor>-<flavor>` build target) and installs the dependency list at
`versions/<target>/requirements.txt`. The `build-matrix.yml` workflow has
two stages:

1. **build** — for each `<target>`, build an image per architecture on a
   native runner (`ubuntu-latest` for amd64, `ubuntu-24.04-arm` for arm64)
   and push as `ghcr.io/.../qiskit:<target>-<arch>`.
2. **manifest** — combine the per-arch tags into a multi-arch
   `ghcr.io/.../qiskit:<target>` with `docker buildx imagetools create`,
   then force-sync a per-target stub branch containing only
   `binder/Dockerfile` (a one-line `FROM ghcr.io/...` reference).

mybinder consumes the stub branch and pulls the pre-built image instead of
rebuilding the dep tree from scratch (cold start ~30s).

To add a new Qiskit version:

1. Create `versions/<X.Y>-small/requirements.txt` and
   `versions/<X.Y>-xl/requirements.txt`.
2. Add `<X.Y>-small` and `<X.Y>-xl` to the `matrix.version` list in
   `.github/workflows/build-matrix.yml`.
3. Add two rows to the table above.

## License

Apache-2.0. Qiskit itself is also Apache-2.0; see [LICENSE](LICENSE).
