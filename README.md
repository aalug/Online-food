# Online-food
Project made for learning purposes of Django.
It uses some code from one of 
the HTML, CSS, and JS templates.


## Setup

1. Rename `.env-sample` to `.env` and replace the values.
2. Run in your terminal `docker-compose up`.
3. Now the website should be up on `http://localhost:8000/`

## Working with Docker
To run Django commands with docker:
1. After Setup run `docker ps` and get the ID of "travelsite-web" container.
4. Run `docker exec -it <container ID> bash`
5. Now in bash django commands can be used (e.g. `python manage.py makemigrations`)

### Additional information
Additional information about docker can bo found on
`https://docs.docker.com/get-started/`
