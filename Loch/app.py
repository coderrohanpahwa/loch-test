
from hospital_management_system import app as application

if __name__ == "__main__":
    application.run(debug=application.config['DEBUG'],port=application.config["PORT"])

