### Building and running our application
Prerequisites: Modern System with Windows 10/11, Linux or MacOS

Install docker cli or docker desktop for your operating system by going to the following website:
https://www.docker.com/products/docker-desktop/

And scrolling down a bit. There you can select the download button and choose a version of Docker that is 
compatible with your operating system. Then after downloading follow the instructions of the installer.

### Building the container
You can build an image for the routeguesser application and run it by typing:
`docker compose up --build`

in the main project directory (should be the name of the repository iteself 
and not a subfolder so e.g. C:\Users\Bob\Documents\routeguesser)

The game application will be available at:
http://localhost:8080/game.html

You can go to this link in a modern browser like Chrome or Firefox and paste it there.

You can verify that the containers are running by going to the docker desktop application or typing
`docker ps`

If you wish to uninstall Docker Desktop you can do it easily by searching the name of the application
in your system and then selecting an option to uninstall.