# The Continous Integration

Arnold uses CircleCI for its continuous integration workflow. We will describe
here quality checks that are performed on this repository.

# Linters

You can run all linters thanks to the `bin/lint` script. By default all linters
will run on Arnold's repository, but you can choose to run one specific linter
at a time by giving the linter name as an argument (more details in sections
below):

```bash
# Run all checks
$ bin/lint

# Check Dockerfile
$ bin/lint docker

# Check Bash scripts
$ bin/lint bash

# Check Ansible playbooks
$ bin/lint ansible
```

## Dockerfile

[Haskell Dockerfile Linter](https://github.com/hadolint/hadolint) helps us to
build a Docker image following official [best
practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

It also uses [ShellCheck](https://github.com/koalaman/shellcheck) (see below) to
lint the Bash code inside the `RUN` instructions.

### Shell

[ShellCheck](https://github.com/koalaman/shellcheck) is a GPLv3 tool that gives
warnings and suggestions for bash/sh shell scripts.

> This Linter is included in Arnold's Docker image.

### Ansible

[ansible-lint](https://github.com/willthames/ansible-lint) checks playbooks for
practices and behavior that could potentially be improved. We use also [more
rules](https://github.com/tsukinowasha/ansible-lint-rules).

> This Linter is included in Arnold's Docker image.
