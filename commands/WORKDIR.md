## WORKDIR
[Documentation](https://docs.docker.com/reference/dockerfile/#workdir)

> WORKDIR /path/to/workdir

The **WORKDIR** instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile. 
If the WORKDIR doesn't exist, it will be created even if it's not used in any subsequent Dockerfile instruction.

In practice, if you aren't building a Dockerfile from scratch (FROM scratch), the WORKDIR may likely be set by the base image you're using.

### REMINDERS
If not specified, the default working directory is /. 

The WORKDIR instruction can be used multiple times in a Dockerfile. If a relative path is provided, it will be relative to the path of the previous WORKDIR instruction.
Example:
    WORKDIR /a
    WORKDIR b
    WORKDIR c
    RUN pwd
The output of the final pwd command in this Dockerfile would be /a/b/c.

The WORKDIR instruction can resolve environment variables previously set using ENV.

### BEST PRACTICES
For clarity and reliability, you should always use absolute paths for your WORKDIR. Also, you should use WORKDIR instead of proliferating instructions like RUN cd … && do-something, which are hard to read, troubleshoot, and maintain.