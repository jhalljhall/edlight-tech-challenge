FROM gitpod/workspace-python
USER root
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pyenv install 3.11 \
    && pyenv global 3.11