{ pkgs ? import <nixpkgs> {}, lib ? pkgs.lib, fetchFromGitHub ? pkgs.fetchFromGitHub }:

let
  poetry2nix = import (fetchFromGitHub {
    owner = "nix-community";
    repo = "poetry2nix";
    rev = "e0b44e9e2d3aa855d1dd77b06f067cd0e0c3860d";
    sha256 = "sha256-puYyylgrBS4AFAHeyVRTjTUVD8DZdecJfymWJe7H438=";
  }) { inherit pkgs; };
in
  poetry2nix.mkPoetryApplication {
    projectDir = ./.;
  }
