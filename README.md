# Personal Alfred

Personal automatizations created for testing the Chalice framework.

## Requirements

- python 3.7 and 3.9
- poetry
- terraform 1.1.9

## Considerations

- when running from CI and not local, the config.json, deployed and
  chalice.tf.json will not be updated in repo
- A record needs to be created and connected to API Gateway endpoint manually -
  fortunately only once per API Gateway change
- Lumigo does not work with Chalice because is is injecting it's own custom handler
  which does not record the allowed HTTP methods, custom manual tracing also
  doesn't work
