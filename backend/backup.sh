#!/bin/bash
set -e

BACKUP_DIR="/backups"
RETAIN_COUNT=7
INTERVAL=21600  # 6 hours

echo "[BACKUP] Starting backup service. Retaining last ${RETAIN_COUNT} backups."
echo "[BACKUP] Backup interval: every $(($INTERVAL / 3600)) hours."

while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql"

    echo "[BACKUP] Creating backup: ${BACKUP_FILE}"

    # Retry up to 10 times if postgres isn't ready yet
    for i in {1..10}; do
        if PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump -h postgres -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" > "${BACKUP_FILE}" 2>/tmp/pg_dump_err; then
            echo "[BACKUP] Backup successful: $(wc -c < "${BACKUP_FILE}" | awk '{print $1}') bytes"
            break
        else
            echo "[BACKUP] pg_dump failed (attempt $i/10). Retrying in 10s..."
            cat /tmp/pg_dump_err || true
            sleep 10
        fi
    done

    # Rotate old backups
    BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/backup_*.sql 2>/dev/null | wc -l)
    if [ "$BACKUP_COUNT" -gt "$RETAIN_COUNT" ]; then
        ls -1t "${BACKUP_DIR}"/backup_*.sql | tail -n +$(($RETAIN_COUNT + 1)) | xargs -r rm
        echo "[BACKUP] Rotated old backups. Keeping ${RETAIN_COUNT} most recent."
    fi

    echo "[BACKUP] Next backup in $(($INTERVAL / 3600)) hours."
    sleep $INTERVAL
done
