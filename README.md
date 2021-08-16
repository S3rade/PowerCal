##  The Process of Power Cal

![Image of Process of Programme](https://github.com/Serade12/PowerCal/blob/main/Images/PowerCal_Flow.png)

## DISCLAIMERS

**IF YOU ARE SETTING IT UP IN YOUR OWN ENVIROMENT ENSURE THE PATHS ARE CORRECT AS WELL AS LOCATION OF SCRIPTS** 

**SAFEST IS TO FOLLOW THE SAME FILE STRUCTURE SEEN BELOW!** 

## File Structure In Host Machine
 Main File Structure:
 
![Main File Structure](https://github.com/Serade12/PowerCal/blob/main/Images/main_file_structure.JPG)

Cacert File Structure:

![Cacert File Structure](https://github.com/Serade12/PowerCal/blob/main/Images/cacert_file_structure.JPG)

## Set Up From Scratch ! 

# On a Clean Machine , run the following Commands to install Docker: 

1. `curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -`
2. `echo 'deb https://download.docker.com/linux/debian stretch stable' > /etc/apt/sources.list.d/docker.list`
3. `apt-get update`
4. `apt-get remove docker docker-engine docker.io`
5. `apt-get install -y docker-ce`
6. `apt install cgroup-tools cgroupfs-mount libcgroup-dev libcgroup1 libpam-cgroup golang-github-containerd-cgroups-dev docker-compose net-tools curl -y`

# With the Docker Programme Installed,
We will need a base image to be used on all the other docker machines, the following commands will be used to get our base image ready for the application we are using.

- Creation of the Docker Volume and relevant details:
  1. `docker volume create cost_vol`
  2. `docker volume inspect cost_vol`
  3. `ln -s /var/lib/docker/volumes/cost_vol/_data /root/cost_vol`
  

- Transfering Scripts into the Docker Folder to be used:
  1. `cp /root/scrips.zip /root/cost_vol`
  2. `cd /root/cost_vol`
  3. `unzip scripts.zip`
  4. `chmod u+x /root/iot_vol/scripts/*.py`
 
 
- Pulling of Debian image and Running it as a container :
  1. `docker pull debian:stretch-slim`
  2. `docker run -dit --name cost-base debian:stretch-slim bash`
  3. `docker images`


- Attaching the Docker to a terminal and running programme installtions: 
  1. `docker exec -it cost-base bash`
  2. `apt update`
  3. `apt upgrade`
  4. `apt install -y mariadb-server mosquitto mosquitto-clients ufw vim nano python3 python3-pip`
  5. `apt install -y python-dev default-libmysqlclient-dev`
  6. `pip3 install ipython flask dweepy mysqlclient`
  7. `pip3 install flask_mysqldb`
  8. `pip3 install paho-mqtt`
  9. `pip3 install flask flask-bootstrap4 pyotp`
  10. `pip3 install imutils opencv-python scikit-build numpy`
  11. `exit`


- Saving the Debian Image locally under another Image name:
  1. `docker commit cost-base cost-image`
  2. `docker stop cost-base`
  3. `docker save -o cost-image.tar cost-image`
  4. `docker rm cost-base`


- Additional Commands if needed :
  1. Removing of Image: 
      `docker rmi image_name`
  2. Removing of Container:
      `docker rm container_name`
  3. Backup Image:
      `docker save -o output_filename.tar image_name`
      
      
 Thats all for setup !
 
 ## Docker Settings and StartUp Commands 
 
 1. Creation of Private Network 
   - `docker network create --subnet=172.16.0.0/16 cost_network`
   - `docket network ls`
 
 2. Starting of the Docker Containers 
   - `docker run --cap-add=NET_ADMIN -it --rm --hostname iot-sensor --net cost_network --ip 172.16.0.11 -v cost_vol:/root/cost_vol --name iot-sensor cost-image bash`
 
 
 ## File Names and It's Purposes
 1. `/images/PowerCal_Flow.png` is the _**Use Case Diagram**_.
 
 2. `DB/init_mysql.sql` is the _**MySQL(MariaDB) database creation and building**_.
 
 3. `DB/docker_app.py` is the _**Programme to running of the webpage for users to see**_. 
 
 4. `DB/start_webdb.sh` is the _**script to excecute init_mysql.sql and powercal.py scripts and start MySQL services.**_.
 
 5. `DB/static` is the  _**folder used to call the image to the webpage **_.
 
 6. `DB/templates` is the _**folder with the template layout for Webpage*_. 
 
 7. `MQTT/cacert/passwords` is the _**hashed password for MQTT to load in during simple_pass.conf to set the username and password on initialization**_.
 
 8. `MQTT/cacert/tls.conf` is the _**TLS config for mosquitto MQTT to run**_.
 
 9. `MQTT/cacert/docker_generate-ca.sh` is the _**CA Cert Generator for authentication details*__
 
 10. `IOT SENSOR/iot_sensor.py` is the _**Raspberry Pi IOT Sensor Simulation**_.
 
 11. `IOT SENSOR/EmulateGPIO.py` is the  _**python script used during the import for iot_sensor.py to allow it to run the Raspberry Pi Simulation**_.\
 
  
 ## Setting Up PowerCal
 
 1. Launch your IOT Sensor , MQTT and Database Dockers
 
 2. Download PowerCal into your docker root directory, for my case its at /root/cost_vol/scripts
 
 3. DOCKER RUN COMMANDS:
    SENSOR DOCKER
    - `docker run --cap-add=NET_ADMIN -it --rm --hostname iot-sensor --net cost_network --ip 172.16.0.11 -v cost_vol:/root/cost_vol --name iot-sensor cost-image bash`
    
    MQTT DOCKER
    - `docker run --cap-add=NET_ADMIN -it --rm --hostname iot-mqtt --net cost_network  --ip 172.16.0.12 -v cost_vol:/root/cost_vol --name iot-mqtt cost-image bash`
    
    DB DOCKER
    - `docker run --cap-add=NET_ADMIN -it --rm --hostname iot-db --net cost_network --ip 172.16.0.13 -v cost_vol:/root/cost_vol --name iot-db cost-image bash`
 
 4. Launch MQTT broker in your MQTT docker by using the commands:
    - `cd /root/cost_vol/scripts/cacert ` Be sure to change to your Docker root directory 
    
    - `mosquitto -v -c tls.conf`
    
    With this now your MQTT Broker is running
    
 5. On your IOT Sensor Docker, launch iot_sensor.py script using the commands:
    - `cd /root/cost_vol/scripts` Be sure to change to your Docker root directory 
    
    - `./sensor.py` Change the Sensor to the name of your own sensor file.
   
    Errors you may Face: 
    
    Insufficent privileges: `chmod u+x filename`
    
    Import EmulateGPIO Cant load module : ensure EmulateGPIO.py is in the same root directory as iot_sensor.py 
 
 6. On your Database Docker, launch powercal.py usings the codes: 
    - `modprobe ip6table_filter`
    
    - `cd /root/cost_vol/scripts` Be sure to change to your Docker root directory 
        
    - `./start_webdb.sh`  
    
    Errors you may Face: 
    
    Insufficent privileges: `chmod u+x filename`
 
 6.Now you can see the Table of the databse by going to databaseip:8080 in web browser of your choice. 
 
 7.ADD/UPDATE Function
    - When u run a script to perform add function (say: BasicOven.py), make sure to run the script and confirm that any changes made appears on the webdb.
    **Special case for iot_SaferoomLight.py
    - For this u need to use the following command: Iot_saferoomlight.py -v (.mov file name)


 ## References
 1. [Installtion Guide For Docker On Kali Linux 2018](https://medium.com/@calypsobronte/installing-docker-in-kali-linux-2018-1-ef3a8ce3648)
 2. [Installation Guide on Mosquitto for Linux](http://www.steves-internet-guide.com/install-mosquitto-linux/)
 3. [Beginners Guide To The Paho MQTT Python Client](http://www.steves-internet-guide.com/into-mqtt-python-client/)
 4. [Mosquitto Username and Password Authentication Configuration and Testing](http://www.steves-internet-guide.com/mqtt-username-password-example/)
 

