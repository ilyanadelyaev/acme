import acme.neuro.api.application as _application


app = _application.Application()


# uwsgi magic
application = app.flask_app
