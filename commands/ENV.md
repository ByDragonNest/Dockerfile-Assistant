## ENV
[Documentation](https://docs.docker.com/reference/dockerfile/#env)

> ENV key=value ...

The ENV instruction sets the environment variable `key` to the value `value`. 
This value will be in the environment for all subsequent instructions in the build stage and can be replaced inline in many as well. 
The value will be interpreted for other environment variables, so quote characters will be removed if they are not escaped. Like command line parsing, quotes and backslashes can be used to include spaces within values.

The ENV instruction allows for multiple key=value ... variables to be set at one time, and the example below will yield the same net results in the final image:
> ENV MY_NAME="John Doe" MY_DOG=Rex\ The\ Dog \
> MY_CAT=fluffy

The environment variables set using ENV will persist when a container is run from the resulting image.

### BEST PRACTICE
To make new software easier to run, you can use ENV to update the PATH environment variable for the software your container installs. 
For example, ENV PATH=/usr/local/nginx/bin:$PATH ensures that CMD ["nginx"] just works.

ENV can also be used to set commonly used version numbers so that version bumps are easier to maintain, as seen in the following example:

Lastly, ENV can also be used to set commonly used version numbers so that version bumps are easier to maintain, as seen in the following example:
> ENV PG_MAJOR=9.3
> ENV PG_VERSION=9.3.4
> RUN curl -SL https://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …
> ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH