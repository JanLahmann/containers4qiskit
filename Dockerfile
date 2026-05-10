FROM quay.io/jupyter/base-notebook:python-3.13

ARG QISKIT_VERSION
ENV QISKIT_VERSION=${QISKIT_VERSION}

USER root
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
