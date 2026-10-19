# Data Directory

## Public data

`plants.json` contains the small, source-linked starter dataset used by the MVP.

## Local/private data

The running application creates a local SQLite database (`garden.db`) for garden observations. This file is intentionally ignored by Git and must not be committed to a public repository.

Future private or personal datasets should be stored under:

```text
data/private/
```

This directory is also ignored by Git.
