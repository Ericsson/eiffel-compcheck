# Eiffel Compcheck
This repository contains tooling for examining the validity of Eiffel compositions. For descriptions and documentation of Eiffel, For descriptions and documentation, see the [Eiffel repository](https://github.com/Ericsson/eiffel).

Eiffel and the contents of this repository are licensed under the [Apache License 2.0](./LICENSE).

## Usage
There are multiple types of checks, each implemented as a separate Python script. Run `<script> -h` for usage instructions. Each operates on an array of events, searching for problems:
* checkdependencies.py checks for unsatisfied dependency declarations
* checkimplrequirements.py checks for unsatisfied implementation requirement declarations
* checknodependents.py checks for artifacts without dependents
* checkunmatchedimplementations.py checks for artifacts declaring themselves implementations of non-existent artifacts
