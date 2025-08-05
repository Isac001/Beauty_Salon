# **Beauty Salon**

### Step 1: Install git:

```bash
sudo apt-get install git
```

# Step 2: Installation of the Database Solution on PostgreSQL (Required)

_For Ubuntu_ OR _WSL_:

Dependency Installation

```bash
sudo apt update &&
sudo locale-gen pt_BR.UTF-8 &&
sudo apt install git python3-pip postgresql postgresql-client
```

To update the server and install the main dependencies related to the project, use the following commands:


```bash
sudo service postgresql start &&
sudo -u postgres psql
```

Then:

```bash
CREATE DATABASE beautysalon;
CREATE USER beautysalon WITH PASSWORD 'root';
\c beautysalon;
GRANT ALL PRIVILEGES ON DATABASE beautysalon TO beautysalon;
GRANT ALL ON SCHEMA public TO beautysalon;

```

After configuring the project, use the following command to exit the terminal:

```bash
\q
```

### Step 3: Now enter the directory where the project root is located by using:

```bash
cd ~/beauty_salon
```

Install the requirements of the project using the following command:


```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```


### Step 3: Next, you should run the commands to create the tables in the database using the migration and loadfixture commands.

```bash
python3 manage.py loadfixtures
```

Finally, some checks should be performed before starting the system execution.

In the settings.py file of the project, you should provide the IP used by the application to connect to the server. This value should be inserted in the ALLOWED_HOSTS and CORS_ORIGIN_WHITELIST properties.

In the .env file, you should verify if the system's access data to the DBMS corresponds to the ones configured in the previous step.

After these steps, the solution is ready for execution, as shown in the following command.

```bash
python3 manage.py runserver
```

Once the installation process is completed, you can access the the solution from a web browser with this ip address:

Locally, using this address _http://127.0.0.1:8000_.