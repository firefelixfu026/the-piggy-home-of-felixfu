#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/opt/felixfu-blog"
BACKUP_DIR="$PROJECT_DIR/backups/postgres"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/felix_blog_$TIMESTAMP.sql"

cd "$PROJECT_DIR"
mkdir -p "$BACKUP_DIR"

docker compose exec -T postgres pg_dump -U felix_blog -d felix_blog > "$BACKUP_FILE"
gzip "$BACKUP_FILE"

find "$BACKUP_DIR" -name 'felix_blog_*.sql.gz' -type f -mtime +"$RETENTION_DAYS" -delete

echo "Backup created: $BACKUP_FILE.gz"
ls -lh "$BACKUP_FILE.gz"
