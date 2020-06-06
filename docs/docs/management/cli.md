# Command Line Interface

`vue.py` provides a command line tool `vue-cli` to deploy your application.

## Deployment
A `vue.py` application can be deployed via several provider.

Get help about the available provider and their arguments
```bash
$ vue-cli deploy -h
```

This installs all the required packages for e.g. the flask provider
```bash
pip install vuepy[flask]
```

### Flask
With a flask live deployment your application is accessible on
[http://localhost:5000](http://localhost:5000).
```bash
$ vue-cli deploy flask
```
This is the best deployment method when debugging.

### Static
With a static deployment everything your application needs,
gets packaged into a single folder,
which can be served by your favorite web server.
```bash
$ vue-cli deploy static <destination> --package
```
* `destination` specifies the path where your application should be deployed to.
* `--package` (optional) packages the python code into the vuepy.js file.
