#!/bin/bash

API_URL="${COLOR:-127.0.0.1/internal/api/v1/clients/${CLIENT_ID}/uploadingSettings}"
API_TOKEN="${API_TOKEN}"
HOST_HEADER="ekd-ftp-uploader"

# Выполнение запроса
curl --location "$API_URL" \
--header "Server-Api-Token: Configured $API_TOKEN" \
--header "Content-Type: application/json" \
--header "Host: $HOST_HEADER" \
--data-raw "{
    \"tenantId\": \"${TENANT_ID}\",
    \"protocol\": \"${PROTOCOL}\",
    \"rootDirectory\": \"${SFTP_DIR}\",
    \"username\": \"${SFTP_USERNAME}\",
    \"password\": \"${SFTP_PASSWORD}\",
    \"hostname\": \"${SFTP_HOST}\",
    \"port\": ${SFTP_PORT},
    \"startUploadingDate\": \"${START_UPLOADING_DATE}\",
    \"execPbszEnabled\": ${EXEC_PBSZ_ENABLED},
    \"localPassiveModeEnabled\": ${LOCAL_PASSIVE_ENABLED},
    \"forceUtf8ControlEncodingEnabled\": ${FORCE_UTF8_ENABLED},
    \"sendOptionUtf8Enabled\": ${SEND_UTF8_ENABLED}
}"