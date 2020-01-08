with import <nixpkgs> {};
let
    my-python-packages = python-packages: with python-packages; [
        watchdog
        setuptools
    ];
    python-with-packages = python3.withPackages my-python-packages;
in
    stdenv.mkDerivation rec {
        name = "memover-env";
        # Mandatory boilerplate for buildable env
        env = buildEnv { name = name; paths = buildInputs; };
        builder = builtins.toFile "builder.sh" ''
        source $stdenv/setup; ln -s $env $out
        '';

        buildInputs = [
            python-with-packages
        ];
    }
