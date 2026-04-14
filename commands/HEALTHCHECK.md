## HEALTHCHECK
[Documentation](https://docs.docker.com/reference/dockerfile/#healthcheck)

The **HEALTHCHECK** instruction has two forms:
> HEALTHCHECK [OPTIONS] CMD command (check container health by running a command inside the container)
> HEALTHCHECK NONE (disable any healthcheck inherited from the base image)

The HEALTHCHECK instruction tells Docker how to test a container to check that it's still working. 
This can detect cases such as a web server stuck in an infinite loop and unable to handle new connections, even though the server process is still running.

When a container has a healthcheck specified, it has a health status in addition to its normal status. This status is initially starting. 
Whenever a health check passes, it becomes healthy (whatever state it was previously in). After a certain number of consecutive failures, it becomes unhealthy.

### REMINDERS
There can only be one HEALTHCHECK instruction in a Dockerfile. If you list more than one then only the last HEALTHCHECK will take effect.
The command's exit status indicates the health status of the container. The possible values are:
- 0: success - the container is healthy and ready for use
- 1: unhealthy - the container isn't working correctly
- 2: reserved - don't use this exit code