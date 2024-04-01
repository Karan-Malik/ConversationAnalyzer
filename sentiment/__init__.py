from flask import Flask
from sentimentconfig import Config

app=Flask(__name__)
app.config.from_object  (Config)



from sentiment import routes
