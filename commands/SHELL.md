## SHELL
[Documentation](https://docs.docker.com/reference/dockerfile/#shell)

> SHELL ["executable", "parameters"]

The **SHELL** instruction allows the default shell used for the shell form of commands to be overridden. 
The default shell on Linux is ["/bin/sh", "-c"], and on Windows is ["cmd", "/S", "/C"]. The SHELL instruction must be written in JSON form in a Dockerfile.