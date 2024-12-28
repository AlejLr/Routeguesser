### Building and running your application
Install docker cli or docker desktop for your operating system:
https://www.docker.com/products/docker-desktop/

You can build an image for the routeguesser application and run it by typing:
`docker compose up --build`

in the main project directory (should be the name of the repository iteself 
and not a subfolder so e.g. C:\Users\Bob\Documents\routeguesser)

The game application will be available at:
http://localhost:8080/game.html

You can verify that the containers are running by going to the docker desktop application or typing
`docker ps`
