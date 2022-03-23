# Contributing a PR
First of: Thanks for contributing a PR to this project!!

There a four main guidelines I try to follow in this projects:
* Write clean code according to Bob Martins book
* Have tests!!
  * Unit tests and selenium tests
  * In general I try to use the examples in the vue.js documentation as test cases to make sure vue.py works as vue.js
* If a new feature is implemented, please also provide documentation
* Each commit needs a certain format `[type] commit message`
  * This allows a automated generation of the changelog
  * PRs get squashed and merged, so commit messages in PRs can be arbitrary
  * type can be one of the following
    * feature: use when adding new features
    * bugfix: use when a bug gets fixed but function stays the same
    * internal: use when refactoring or no user-facing changed are made
    * docs: use when updating documentation
    * tooling: use when changing tooling
