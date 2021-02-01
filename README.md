# Purdue TripTimer Server

[![Build Status](https://github.com/chrisx8/purduetriptimer-server/workflows/build/badge.svg)](https://github.com/chrisx8/purduetriptimer-server/actions?query=workflow%3Abuild)
[![CodeFactor](https://www.codefactor.io/repository/github/chrisx8/purduetriptimer-server/badge)](https://www.codefactor.io/repository/github/chrisx8/purduetriptimer-server)

Purdue TripTimer a Hello World 2020 project by [@aaryan-gautam](https://github.com/aaryan-gautam), [@afshirazi](https://github.com/afshirazi), [@chrisx8](https://github.com/chrisx8), and [@HenryWellman](https://github.com/HenryWellman).

This repository contains the server-side implementation. The Android app is at [chrisx8/purduetriptimer](https://github.com/chrisx8/purduetriptimer).

[Hello World 2020 submission](https://devpost.com/software/purdue-triptimer)

## Install using Docker

Replace `[replace_me]` with your actual database URL. 

Supported databases: SQLite, MySQL (requires mysqlclient), PostgreSQL (requires psycopg2). 

```bash
docker run -e DATABASE_URL=[replace_me] -d -p 8000:8000 chrisx8/purduetriptimer-server
```

## License

[MIT License](LICENSE)
