# Deployment Guide

This repository is installed as an agent skill, not deployed as a service.

## Prerequisites

- A Python runtime compatible with the documented `3.8+` baseline.
- Git or another method to place the repository in an agent skill directory.
- Read access to the target repository and write access to the requested output directory.

## Installation and use

Follow the repository's installation examples in [README.md](README.md#L12), then invoke the skill through the host agent. Individual scripts expose `--help` and accept local paths. Run the verification suite with `python test_inspect_repository_scripts.py` as documented in [README.md](README.md#L99).

## Deployment gaps

There is no `pyproject.toml`, requirements file, lock file, build metadata, release automation, container, signed artifact, CI workflow, supported-platform matrix, or versioned JSON output contract. The README also names `quick_validate.py`, but that file is absent from the inventory. Before organizational rollout, package the scripts, pin supported Python versions in CI, add release provenance, and treat redaction regression tests as mandatory.
