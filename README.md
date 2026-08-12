# mongodb-sandbox

play around with mongodb

## Dev Container

This repo now includes a Dev Container that installs MongoDB (Ubuntu packages) by default.

1. Open the repo in VS Code.
2. Run **Dev Containers: Reopen in Container**.
3. Start MongoDB inside the container:

   ```bash
   mongod --dbpath /data/db --bind_ip_all
   ```

4. In a second terminal, connect with:

   ```bash
   mongosh
   ```
