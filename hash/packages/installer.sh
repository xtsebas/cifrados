#!/bin/bash
# MediSoft v2.1.0 Installer
# (c) MediSoft S.A. — Distribucion autorizada unicamente a hospitales certificados

set -e

INSTALL_DIR="/opt/medisoft"
SERVICE_NAME="medisoft"

echo "Instalando MediSoft v2.1.0..."
mkdir -p "$INSTALL_DIR"
cp -r ./lib "$INSTALL_DIR/"
cp config.ini "$INSTALL_DIR/"
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"
echo "Instalacion completada."
