## ENTRYPOINT
[Documentation](https://docs.docker.com/reference/dockerfile/#entrypoint)

**ENTRYPOINT** allows you to configure a container that will run as an executable.

ENTRYPOINT has two possible forms:
> The exec form, which is the preferred form:
    > ENTRYPOINT ["executable", "param1", "param2"]
> The shell form:
    > ENTRYPOINT command param1 param2

For more information about the different forms, see (https://docs.docker.com/reference/dockerfile/#shell-and-exec-form)

### REMINDERS
Both CMD and ENTRYPOINT instructions define what command gets executed when running a container. There are few rules that describe their co-operation:
- Dockerfile should specify at least one of CMD or ENTRYPOINT commands.
- ENTRYPOINT should be defined when using the container as an executable.
- CMD should be used as a way of defining default arguments for an ENTRYPOINT command or for executing an ad-hoc command in a container.
- CMD will be overridden when running the container with alternative arguments.