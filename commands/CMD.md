## CMD
[Documentation](https://docs.docker.com/reference/dockerfile/#cmd)

The **CMD** instruction sets the command to be executed when running a container from an image.

You can specify CMD instructions using shell or exec forms:
> CMD ["executable","param1","param2"] (exec form)
> CMD ["param1","param2"] (exec form, as default parameters to ENTRYPOINT)
> CMD command param1 param2 (shell form)
### REMINDERS
- There can only be one CMD instruction in a Dockerfile. If you list more than one CMD, only the last one takes effect.

- If CMD is used to provide default arguments for the ENTRYPOINT instruction, both the CMD and ENTRYPOINT instructions should be specified in the exec form.
### BEST PRACTICE 
- If you would like your container to run the same executable every time, then you should consider using ENTRYPOINT in combination with CMD. See ENTRYPOINT. If the user specifies arguments to docker run then they will override the default specified in CMD, but still use the default ENTRYPOINT.

