# Pin to a digest so a re-tagged base can't silently change the
# build under us; Dependabot proposes digest bumps weekly and they
# go through the full Trivy + smoke gate like any other change.
# Tag retained in the comment for human readability — the digest is
# the source of truth.
FROM quay.io/jupyter/base-notebook:python-3.13@sha256:5bcf92a903b64a32b0d87a103b34e3e9fcab4d1e0c4579be9963966a09f9bbfb

ARG QISKIT_VERSION
ENV QISKIT_VERSION=${QISKIT_VERSION}

USER root

# xl images bundle nbgitpuller, which shells out to `git` at runtime
# to clone the user's notebook repo into the running session. The
# Jupyter base-notebook image is intentionally minimal and ships
# without git, so without this step nbgitpuller raises FileNotFoundError
# on every git-pull URL. small images don't ship nbgitpuller and stay
# git-less to preserve the "small = small" property.
RUN if [[ "${QISKIT_VERSION}" == *-xl ]]; then \
      apt-get update \
      && apt-get install -y --no-install-recommends git \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/* ; \
    fi

COPY versions/${QISKIT_VERSION}/requirements.txt /tmp/req.txt
# jupyter-server upgrade patches CVE-2026-35397 / -40110 / -40934 that the
# base image still ships at 2.17.0; remove once the base bumps it.
RUN pip install --no-cache-dir --no-compile -r /tmp/req.txt \
 && pip install --no-cache-dir --no-compile --upgrade 'jupyter-server>=2.18.0' \
 && rm /tmp/req.txt \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

# Smoke test: catches wheels that resolve cleanly but break at import
# time (e.g. a python-version bump where pip picked a wheel that
# doesn't actually load). Runs at build time so the gate is the
# build itself.
RUN python -c 'import qiskit; from qiskit import QuantumCircuit; QuantumCircuit(2).measure_all()'

USER ${NB_UID}
WORKDIR /home/${NB_USER}
