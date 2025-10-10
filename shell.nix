{
  pkgs ? import <nixpkgs> {},
  python ? pkgs.python3,
}: let
  pypkgs = python.pkgs;
  package = import ./default.nix {inherit pkgs python;};
in
  pkgs.mkShell {
    packages = [
      python
      package
      pypkgs.pip
      pypkgs.setuptools
      pypkgs.wheel
      pypkgs.pytest
      pypkgs."pytest-cov"
    ];
  }
