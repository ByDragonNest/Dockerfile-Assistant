## COPY
[Documentation](https://docs.docker.com/reference/dockerfile/#copy)

**COPY** has two forms. The latter form is required for paths containing whitespace.
> COPY [OPTIONS] src ... dest
> COPY [OPTIONS] ["src", ... "dest"]

The available [OPTIONS] are:
- --from	
- --chown [!] WARNING: Only octal notation is currently supported.
- --chmod: 1.2 (Minimum Dockerfile version) [!] WARNING: Only octal notation is currently supported.
- --link: 1.4 (Minimum Dockerfile version)
- --parents: 1.7 (Minimum Dockerfile version)
- --exclude: 1.7 (Minimum Dockerfile version)

The COPY instruction copies new files or directories from `src` and adds them to the filesystem of the image at the path `dest`. Files and directories can be copied from the build context, build stage, named context, or an image.

### REMINDERS
The ADD and COPY instructions are functionally similar, but serve slightly different purposes. Learn more about the differences between ADD and COPY.

### BEST PRACTICE
Here-documents allow redirection of subsequent Dockerfile lines to the input of RUN or COPY commands. 
The Dockerfile considers the next lines until the line only containing a here-doc delimiter as part of the same command.

Example:
> FROM alpine
> ARG FOO=bar
> COPY <<-EOT /script.sh
    > echo "hello ${FOO}"
    > EOT
    > ENTRYPOINT ash /script.sh

[More about this](https://docs.docker.com/reference/dockerfile/#here-documents)