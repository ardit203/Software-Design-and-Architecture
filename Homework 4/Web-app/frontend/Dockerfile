# Use the Node.js image
FROM node:22.12.0

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app

# Expose the frontend port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
