## RUN
[Documentation](https://docs.docker.com/reference/dockerfile/#run)

The **RUN** instruction will execute any commands to create a new layer on top of the current image. The added layer is used in the next step in the Dockerfile. RUN has two forms:
> Shell form: RUN [OPTIONS] command ...
> Exec form: RUN [OPTIONS] [ "command", ... ]

For more information about the differences between these two forms, see (https://docs.docker.com/reference/dockerfile/#shell-and-exec-form)

The available [OPTIONS] for the RUN instruction are:
- --mount	1.2 (Minimum Dockerfile version)
- --network	1.3 (Minimum Dockerfile version)
- --security 1.1.2-labs (Minimum Dockerfile version)

### WARNINGS
The use of RUN `--network=host` is protected by the network.host entitlement, which needs to be enabled when starting the buildkitd daemon with `--allow-insecure-entitlement network.host` flag or in buildkitd config, 
and for a build request with `--allow network.host` flag.

### WARNINGS
> RUN --security=<sandbox|insecure>

The default security mode is sandbox. With `--security=insecure`, the builder runs the command without sandbox in insecure mode, which allows to run flows requiring elevated privileges (e.g. containerd). 
This is equivalent to running docker run `--privileged`.

### BEST PRACTICE
Group packages to install in a single RUN instruction:
> RUN apt-get update && apt-get install -y \
    > aufs-tools \
    > automake \
    > build-essential \
    > curl \
    > ruby1.9.1 \
    > ruby1.9.1-dev \
    > s3cmd=1.1.* \
    > && rm -rf /var/lib/apt/lists/*


Here-documents allow redirection of subsequent Dockerfile lines to the input of RUN or COPY commands. 
The Dockerfile considers the next lines until the line only containing a here-doc delimiter as part of the same command.

Example:
> RUN <<EOT bash
    > set -ex
    > apt-get update
    > apt-get install -y vim
    > EOT

[More about this](https://docs.docker.com/reference/dockerfile/#here-documents)

Using RUN apt-get update && apt-get install -y ensures your Dockerfile installs the latest package versions with no further coding or manual intervention. This technique is known as cache busting. You can also achieve cache busting by specifying a package version. This is known as version pinning. For example:
> RUN apt-get update && apt-get install -y \
    > package-bar \
    > package-baz \
    > package-foo=1.3.*

Version pinning forces the build to retrieve a particular version regardless of what’s in the cache. This technique can also reduce failures due to unanticipated changes in required packages.