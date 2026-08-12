# mongodb-sandbox

play around with mongodb

## Python example

This repository includes a simple Python example that inserts a made-up surface pressure observation into MongoDB and reads it back out.

The example stores:

- `valid_time`
- `added_time`
- `latitude`
- `longitude`
- `pressure_hpa`

Install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

Run the example against a local MongoDB instance:

```bash
python weather_pressure_example.py
```

You can also point it at a different database, collection, or connection string:

```bash
python weather_pressure_example.py \
  --uri mongodb://localhost:27017/ \
  --database weather_demo \
  --collection surface_pressure
```

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
