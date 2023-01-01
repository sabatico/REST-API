import os as os

from dotenv import load_dotenv

import apiFactory as apiFactory
import appFactory as appFactory
import jwtFactory as jwtFactory
import sqlFactory as sqlFactory

load_dotenv()

# INIT APP
app = appFactory.initialize_APP()

# INIT  sqlalchemy and migrate
sqlFactory.initialize_DB(app)
# INIT JWT manager
jwtFactory.initialyze_JWT(app)
# INIT API
apiFactory.initialyze_API(app)
