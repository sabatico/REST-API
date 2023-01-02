import os as os

from dotenv import load_dotenv

import factory.apiFactory as apiFactory
import factory.appFactory as appFactory
import factory.jwtFactory as jwtFactory
import factory.dbFactory as dbFactory

load_dotenv()

# INIT APP
app = appFactory.initialize_APP()

# INIT  sqlalchemy and migrate
dbFactory.initialize_DB(app)
# INIT JWT manager
jwtFactory.initialize_JWT(app)
# INIT API
apiFactory.initialize_API(app)
