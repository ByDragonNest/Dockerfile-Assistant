## USER
[Documentation](https://docs.docker.com/reference/dockerfile/#user)

> USER user[:group]
> USER UID[:GID]

The USER instruction sets the user name (or UID) and optionally the user group (or GID) to use as the default user and group for the remainder of the current stage. 
The specified user is used for RUN instructions and at runtime, runs the relevant ENTRYPOINT and CMD commands.

### WARNINGS

If you need to perform privileged operations in the Dockerfile after setting a non-root user, you can switch to the root user and then switch back to the non-root user once those operations are complete. 
This approach adheres to the principle of least privilege; only tasks that require administrator privileges are run as an administrator. 
Note that it is not recommended to use sudo for privilege elevation in a Dockerfile. Example:
    USER root
    RUN apt-get update && apt-get install -y some-package
    USER myuser

### REMINDERS

On Windows, the user must be created first if it's not a built-in account. This can be done with the net user command called as part of a Dockerfile.
Example:
    FROM microsoft/windowsservercore
    # Create Windows user in the container
    RUN net user /add patrick
    # Set it for subsequent commands
    USER patrick