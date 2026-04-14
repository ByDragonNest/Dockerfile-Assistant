## LABEL
[Documentation](https://docs.docker.com/reference/dockerfile/#label)

> LABEL key=value key=value key=value ...

The **LABEL** instruction adds metadata to an image. A LABEL is a key-value pair. 
To include spaces within a LABEL value, use quotes and backslashes as you would in command-line parsing.

An image can have more than one label. You can specify multiple labels on a single line. Prior to Docker 1.10, this decreased the size of the final image, but this is no longer the case.