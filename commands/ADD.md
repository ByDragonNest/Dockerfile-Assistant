## ADD
[Documentation](https://docs.docker.com/reference/dockerfile/#add)

**ADD** has two forms. The latter form is required for paths containing whitespace:
> ADD [OPTIONS] src ... dest
>
> ADD [OPTIONS] ["src", ... "dest"]

The available [OPTIONS] are:
- --keep-git-dir: 1.1 (Minimum Dockerfile version)
- --checksum: 1.6 (Minimum Dockerfile version)
- --chown
- --chmod: 1.2 (Minimum Dockerfile version)
- --link: 1.4 (Minimum Dockerfile version)
- --exclude: 1.7 (Minimum Dockerfile version)

The ADD instruction copies new files or directories from src and adds them to the filesystem of the image at the path dest. 
Files and directories can be copied from the build context, a remote URL, or a Git repository.