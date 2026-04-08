# Sopialis — Personal Assistant Agent

Sopialis is an OpenClaw-based personal assistant configured to manage calendars and perform automated web searches.

## Features

- 📅 **Google Calendar Sync** — Automated daily agenda checks from multiple calendars (pro + personal)
- 🔍 **Daily Search Monitoring** — Configurable automated web searches
- 💬 **Telegram Integration** — Direct notifications and agenda reminders
- 🔐 **Secure Service Account Auth** — OAuth via Google service accounts (no passwords needed)

## Setup

### 1. Prerequisites

- OpenClaw installed and running
- Google Cloud project with Calendar API enabled
- Python 3.7+

### 2. Google Calendar Configuration

1. Create a Google Cloud service account (see `SETUP_CALENDAR.md`)
2. Enable the Google Calendar API
3. Share your calendars with the service account email
4. Save credentials as `google-calendar-credentials.json` (not in git!)

**Use the template:**
```bash
cp credentials.example.json google-calendar-credentials.json
# Edit with your actual credentials
```

### 3. Install & Run

```bash
# Install Google libraries
pip install --break-system-packages google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Test calendar sync
python3 calendar-gateway-setup.py

# Start daily reminders (9 PM Paris time)
# Run via OpenClaw heartbeat or cron
```

## File Structure

```
.
├── SOUL.md                          # Agent personality & values
├── IDENTITY.md                      # Agent identity (name, vibe, emoji)
├── USER.md                          # User profile (Axel)
├── MEMORY.md                        # Long-term memory & decisions
├── HEARTBEAT.md                     # Periodic tasks & checks
├── TOOLS.md                         # Tool-specific config
├── CRON.md                          # Scheduled tasks
├── calendar-sync.py                 # Calendar sync script
├── calendar-gateway-setup.py        # Setup & test calendar connection
├── calendar-sync.sh                 # Bash-based calendar sync
├── credentials.example.json         # Template for service account
├── google-calendar-credentials.json # ⚠️ NEVER commit (in .gitignore)
└── README.md                        # This file
```

## Configuration

### Calendars

Currently monitoring:
- `axel.dhondt@sopial.fr` (Pro/Work)
- `dhondt.ax@gmail.com` (Personal)

Edit these in `TOOLS.md` and `HEARTBEAT.md`.

### Daily Reminder

- **Time:** 9 PM Paris time (20:00 UTC / 21:00 CEST)
- **Delivery:** Telegram message
- **Content:** Tomorrow's agenda from both calendars

Configure in `CRON.md`.

### Search Topics

Not yet configured. Edit `HEARTBEAT.md` to add topics for monitoring.

## Security Notes

🔒 **Credentials are never committed:**
- `google-calendar-credentials.json` is in `.gitignore`
- Service account has read-only access to calendars
- Store credentials securely in your workspace

🔐 **Token Management:**
- OAuth tokens are cached locally and auto-refreshed
- No passwords or 2FA codes needed

## Customization

Edit these files to customize Sopialis:

- **Personality:** `SOUL.md`
- **Daily checks:** `HEARTBEAT.md`
- **Calendars:** `TOOLS.md`, `HEARTBEAT.md`
- **Reminders:** `CRON.md`
- **Search topics:** `HEARTBEAT.md` (once configured)

## Troubleshooting

### Calendar sync fails

```bash
# Test the connection
export PATH="/data/.local/bin:$PATH"
python3 calendar-gateway-setup.py
```

### "ModuleNotFoundError: No module named 'google'"

Install the libraries:
```bash
pip install --break-system-packages google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Credentials not found

Make sure `google-calendar-credentials.json` exists and is readable:
```bash
ls -la google-calendar-credentials.json
```

## Future Enhancements

- [ ] Configure daily search topics
- [ ] Add email integration
- [ ] Calendar conflict detection
- [ ] Meeting prep automation
- [ ] Custom reminder triggers

## License

Private repo for Axel's personal use.

---

**Agent:** Sopialis  
**Last updated:** 2026-04-08  
**Status:** Calendar sync active, searches pending
