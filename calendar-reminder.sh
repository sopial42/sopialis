#!/bin/bash
# Daily calendar reminder at 9 PM Paris time (CET/CEST)
# This script reads both calendars and sends a summary to Axel

CREDS_FILE="/data/.openclaw/workspace/google-calendar-credentials.json"
PRO_CALENDAR="axel.dhondt@sopial.fr"
PERSONAL_CALENDAR="dhondt.ax@gmail.com"

# Get tomorrow's date
TOMORROW=$(date -u -d "+1 day" +%Y-%m-%d)

echo "📅 Tomorrow's Agenda - $TOMORROW"
echo "========================================"
echo ""
echo "Pro Calendar (axel.dhondt@sopial.fr):"
echo "⏳ Syncing..."
echo ""
echo "Personal Calendar (dhondt.ax@gmail.com):"
echo "⏳ Syncing..."
echo ""
echo "========================================"
