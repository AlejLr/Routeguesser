# Use the official Nginx image as the base
FROM nginx:latest

# Set the working directory in the container
WORKDIR /usr/share/nginx/html

# Copy all static files from the frontend directory to the container
COPY . .

# Expose the default Nginx HTTP port
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
