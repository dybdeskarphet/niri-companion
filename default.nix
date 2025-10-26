{
  pkgs ? import <nixpkgs> {},
  python ? (
    if pkgs ? python3_13
    then pkgs.python3_13
    else pkgs.python3
  ),
}: let
  lib = pkgs.lib;
  pypkgs = python.pkgs;

  # Override typer to a version compatible with pyproject (>=0.19.1)
  typer_019 = pypkgs.typer.overrideAttrs (old: rec {
    version = "0.19.1";
    src = pkgs.fetchPypi {
      pname = "typer";
      inherit version;
      sha256 = "sha256-y4gUM6SxXazIdbsFg9GmHnhJeAZ0H5q6eSq8qzkMA+Y=";
    };
  });
in
  pypkgs.buildPythonPackage rec {
    pname = "niri-companion";
    version = "2.4.0";

    # PEP 517/518 build using setuptools declared in pyproject.toml
    pyproject = true;
    src = ./.;

    build-system = [pypkgs.setuptools];

    # Runtime dependencies from pyproject.toml
    dependencies = [
      pypkgs.pydantic
      pypkgs.rich
      pypkgs."tomli-w"
      typer_019
      pypkgs.watchdog
    ];

    # Run tests with pytest
    nativeCheckInputs = [pypkgs.pytestCheckHook];
    doCheck = false;

    # Optional: only import safe submodules during import checks
    # to avoid triggering config load at import time.
    pythonImportsCheck = [
      "companion.utils.general"
      "companion.utils.genconfig"
      "companion.models.config"
    ];
  }
