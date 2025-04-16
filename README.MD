###### COMMANDS

### DOCKER

# Launch Dev Build

docker-compose -f docker-compose.dev.yml build

# Start Dev Containers

docker-compose -f compose.dev.yml up -d

# Launch Prod Build

docker-compose -f docker-compose.prod.yml build

# Start Prod Containers

docker-compose -f compose.prod.yml up -d

# Launch just the backend

fastapi dev app/main.py
