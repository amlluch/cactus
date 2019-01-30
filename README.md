<h1>Override User model and oauth2 authenticaciton</h1>

You can run this app in a virtual environment or with docker. For running in a virtual environment proceed as usual: create a virtual environment, migrate database and register the app by doing at cactus directory <strong>python3 manage.py shell <  	AppRegister.py</strong>
  
  If you want change database user name or password, change in /config/db/database_env. It executes on port 8000. Change the docker-compose.yml file for executing in a different port.
  
<h2>Docker installation:</h2>

Follow next steps:

1) <strong>Build docker image:</strong> docker-compose build

2) <strong>Run docker for creating user and database:</strong> docker-compose up

3) <strong>Migrate database:</strong> docker-compose run --rm cactus /bin/bash -c "cd cactus; ./manage.py migrate"

4) <strong>Register the app:</strong> docker-compose run --rm cactus /bin/bash -c "cd cactus; ./manage.py shell < AppRegister.py"

5) <strong>Create superuser:</strong> docker-compose run --rm cactus /bin/bash -c "cd cactus; ./manage.py createsuperuser"

Now you can run the app: docker-compose up

<h2>End points</h2>

<h3>Django administration</h3>
/admin    -----> Django administration <br><br>

<h3>oauth2</h3>
/authentication/token/  ---> new token and login<br>
/authentication/register/  ---> new user registration and get tokens (only admin)<br>
/authentication/refresh/    ---> refresh token<br>
/authentication/revoke/ ---> revoke token<br>

<h3>Restapi User Administration</h3>
/restapi/user/ --- > get current user (authenticated)<br>
/restapi/user/<\user-name\>/ ---> User data vistualization. Admin can see any user<br>
/restapi/user/<\new-user\>/new/   ----> Create new user. Only admin<br>

