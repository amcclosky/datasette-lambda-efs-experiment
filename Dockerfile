FROM lambci/lambda:build-python3.8

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

RUN pipx install pre-commit \
    && pipx install invoke \
    && pipx install httpie \
    && pipx install black
