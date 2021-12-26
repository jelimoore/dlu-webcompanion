class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[USER]:[PASSWORD]@[SERVER]/[DB]" # fill this in with your database details
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # this is required from the ORM, don't touch this
    
    # UNUSED, TO BE ADDED LATER
    DLU_HOSTNAME = ''   # the FQDN/IP of your DLU server