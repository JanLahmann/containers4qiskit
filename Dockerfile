# Stay on python-3.12 until we either drop 1.x Qiskit support or numpy
# back-ports cp3.13+ wheels to the 1.x stream. Qiskit 1.x pins
# numpy<2; the newest numpy<2 (1.26.4) has no cp3.13 wheel, and the
# base image carries no C compiler to build from source.
# pull: true in the workflow forces a fresh digest of this tag every
# build, so security fixes still flow through without us pinning a
# specific digest.
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

USER ${NB_UID}
WORKDIR /home/${NB_USER}
