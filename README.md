# containers4qiskit

Docker images and Binder URLs for specific Qiskit versions, so you can spin up
a Jupyter environment running exactly the Qiskit version you need.

For each supported Qiskit version, this repo publishes:

- A Docker image at `ghcr.io/janlahmann/qiskit:<version>`
- A `<version>` stub branch consumed by [mybinder.org](https://mybinder.org)
  that pulls the pre-built image (cold start ~30s)

## Versions

| Version | Binder | Docker |
| ------- | ------ | ------ |
| 2.4     | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/containers4qiskit/2.4) | `docker run --rm -p 8888:8888 ghcr.io/janlahmann/qiskit:2.4` |

For users not using Docker or Binder:

```
pip install "qiskit~=2.4.0"
```

## How it works

`Dockerfile.template` is parameterised by `QISKIT_VERSION` and reads pinned
dependencies from `versions/<version>/requirements.txt`. The
`build-matrix.yml` workflow builds one image per matrix entry, pushes to
`ghcr.io`, and force-syncs a per-version stub branch containing only
`binder/Dockerfile` (a one-line `FROM ghcr.io/...` reference). mybinder
consumes that branch and pulls the pre-built image instead of rebuilding the
Qiskit pip layer from scratch.

To add a version:

1. Create `versions/<X.Y>/requirements.txt` with `qiskit~=<X.Y>.0` and any
   pinned addons (`qiskit-aer`, `qiskit-ibm-runtime`, ...).
2. Add `<X.Y>` to the `matrix.version` list in
   `.github/workflows/build-matrix.yml`.
3. Add a row to the table above.

## License

Apache-2.0. Qiskit itself is also Apache-2.0; see [LICENSE](LICENSE).
