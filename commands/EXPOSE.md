## EXPOSE
[Documentation](https://docs.docker.com/reference/dockerfile/#expose)

EXPOSE port [port/protocol...]

The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
You can specify whether the port listens on TCP or UDP, and the default is TCP if you don't specify a protocol.

Regardless of the EXPOSE settings, you can override them at runtime by using the -p flag.
To set up port redirection on the host system, see (https://docs.docker.com/reference/cli/docker/container/run/#publish)

### REMINDERS
The docker network command supports creating networks for communication among containers without the need to expose or publish specific ports, because the containers connected to the network can communicate with each other over any port.

### BEST PRACTICE
[Source](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet html#rule-5-be-mindful-of-inter-container-connectivity)

**Inter-Container Connectivity** (icc) is enabled by default, allowing all containers to communicate with each other through the docker0 bridged network. 
Instead of using the `--icc=false` flag with the Docker daemon, which completely disables inter-container communication, consider defining specific network configurations. 
This can be achieved by creating custom Docker networks and specifying which containers should be attached to them. This method provides more granular control over container communication.

For detailed information, see the (https://docs.docker.com/engine/userguide/networking/)