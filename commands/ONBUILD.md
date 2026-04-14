## ONBUILD
[Documentation](https://docs.docker.com/reference/dockerfile/#onbuild)

> ONBUILD INSTRUCTION

The **ONBUILD** instruction adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build. 
The trigger will be executed in the context of the downstream build, as if it had been inserted immediately after the FROM instruction in the downstream Dockerfile.

Here's how it works:
1. When it encounters an ONBUILD instruction, the builder adds a trigger to the metadata of the image being built. The instruction doesn't otherwise affect the current build.
2. At the end of the build, a list of all triggers is stored in the image manifest, under the key OnBuild. They can be inspected with the docker inspect command.
3. Later the image may be used as a base for a new build, using the FROM instruction. As part of processing the FROM instruction, the downstream builder looks for ONBUILD triggers, and executes them in the same order they were registered. 
If any of the triggers fail, the FROM instruction is aborted which in turn causes the build to fail. If all triggers succeed, the FROM instruction completes and the build continues as usual.
4. Triggers are cleared from the final image after being executed. In other words they aren't inherited by "grand-children" builds.