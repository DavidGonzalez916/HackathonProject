import pypyodbc as pyodbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'USLMADAGONZALE2'
DATABASE_NAME = 'BasketballPlayers'

connection_string =  f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes
  """


db = pyodbc.connect(connection_string)
cursor = db.cursor()
