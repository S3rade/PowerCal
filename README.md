## The Process of Power Cal

![Image of Process of Programme](https://github.com/Serade12/PowerCal/blob/main/Untitled%20Diagram.png)


## Set Up From Scratch ! 

# On a Clean Machine , run the following Commands to install Docker: 

1. `curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -`
2. `echo 'deb https://download.docker.com/linux/debian stretch stable' > /etc/apt/sources.list.d/docker.list`
3. `apt-get update`
4. `apt-get remove docker docker-engine docker.io`
5. `apt-get install -y docker-ce`
6. `apt install cgroup-tools cgroupfs-mount libcgroup-dev libcgroup1 libpam-cgroup golang-github-containerd-cgroups-dev docker-compose -y`

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
  8. `exit`


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
 
 ## References
 1. [Installtion Guide For Docker On Kali Linux 2018](https://medium.com/@calypsobronte/installing-docker-in-kali-linux-2018-1-ef3a8ce3648)
 

