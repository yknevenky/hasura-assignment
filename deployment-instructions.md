# Deployment Instructions

1. **Ensure Docker and Docker Compose are installed** on your local machine or server.

2. **Clone the repository** containing the eCommerce project if you haven't already.

3. **Build and start the services** using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This will start the following services:
   - **Redis**: For caching and rate limiting
   - **PostgreSQL**: For the database (used by both Django and Hasura)
   - **MongoDB**: For the MongoDB database
   - **Hasura**: For GraphQL API
   - **Mongo Data Connector**: For connecting MongoDB with Hasura

4. **Run the Django server**:
   - Make sure you have Python dependencies installed by running:
     ```bash
     pip install -r requirements.txt
     ```
   - Then, run the Django server:
     ```bash
     python manage.py runserver
     ```

5. **Access the services**:
   - Django eCommerce server: `http://127.0.0.1:8000`
   - Hasura Console: `http://localhost:8080` (admin secret: `assignment@hasura`)

6. **Stopping services**:
   When you're done, you can stop all the services with:
   ```bash
   docker-compose down
   ```

---

That's it! Your eCommerce project should now be running with the necessary services in Docker containers.