#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: ./scripts/restore-postgres.sh backups/postgres/felix_blog_YYYYMMDD_HHMMSS.sql.gz"
  exit 1
fi

PROJECT_DIR="/opt/felixfu-blog"
BACKUP_FILE="$1"
RESTORE_FILE="/tmp/felix_blog_restore.sql"

cd "$PROJECT_DIR"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "Creating safety backup before restore..."
./scripts/backup-postgres.sh

echo "Restoring from: $BACKUP_FILE"
gunzip -c "$BACKUP_FILE" > "$RESTORE_FILE"
docker compose exec -T postgres psql -U felix_blog -d felix_blog -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker compose exec -T postgres psql -U felix_blog -d felix_blog < "$RESTORE_FILE"
rm "$RESTORE_FILE"
docker compose restart backend

echo "Restore complete. Backend restarted."
