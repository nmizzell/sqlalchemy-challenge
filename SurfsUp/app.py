# Import the dependencies.
from pathlib import Path
from sqlalchemy import create_engine, text


#################################################
# Database Setup
database_path = r"C:\Users\nmizz\Documents\GitHub\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# #Test query to make sure the the databse is connected
# query = text("SELECT * FROM station")
# data = engine.execute(query)

# for record in data:
#     print(record)
#################################################


# reflect an existing database into a new model


# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
