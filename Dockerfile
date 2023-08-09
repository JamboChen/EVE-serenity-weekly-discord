# build stage
FROM python:3.11 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /project/

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


# run stage
FROM python:3.11

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

# retrieve executables
COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

# copy source code
COPY src/ /project/src

RUN if [ -f ".env" ]; then \
    cp .env /project; \
    fi

# set command/entrypoint, adapt to fit your needs
CMD ["python", "/project/src/bot.py"]
