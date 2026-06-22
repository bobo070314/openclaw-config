@echo off
cd /d C:\Users\asus\gbrain
set GBRAIN_HTTP_CORS_ORIGIN=*
bun run src/cli.ts serve --http --port 3131 --enable-dcr
