# Command Line Interface

`vue.py` provides a command line tool `vue-cli` to deploy your application.

## Deployment
### Live
With a live deployment your application is accessible on
[http://localhost:5000](http://localhost:5000).
```bash
$ vue-cli deploy live
```
This is the best deployment method for development and debugging.

### Static
With a static deployment everything your application needs,
gets packaged into a single folder,
which can be served by your favorite web server.
```bash
$ vue-cli deploy static <destination>
```
`destination` specifies the path where your application should be deployed to.

Optionally you can specifiy which applicaton you would like to deploy
```bash
$ vue-cli deploy static <destination> <app-path>
```
By default the application in your current directory gets deployed.

This is the best deployment method for production.
