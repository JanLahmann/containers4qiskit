FROM quay.io/jupyter/base-notebook:python-3.13

ARG QISKIT_VERSION
ENV QISKIT_VERSION=${QISKIT_VERSION}

USER root
COPY versions/${QISKIT_VERSION}/requirements.txt /tmp/req.txt
RUN pip install --no-cache-dir --no-compile -r /tmp/req.txt \
 && rm /tmp/req.txt \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

USER ${NB_UID}
WORKDIR /home/${NB_USER}
