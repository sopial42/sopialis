# Sopialis — Personal Assistant Agent

Sopialis is an OpenClaw-based personal assistant configured to manage calendars and perform automated web searches.

## Features

- 📅 **Google Calendar Sync** — Automated daily agenda checks from multiple calendars (pro + personal)
- 🔍 **Daily Search Monitoring** — Configurable automated web searches
- 💬 **Telegram Integration** — Direct notifications and agenda reminders
- 🔐 **Secure Service Account Auth** — OAuth via Google service accounts (no passwords needed)

## Quick Start

### For the Impatient

1. **Copy credentials:** `cp credentials.example.json google-calendar-credentials.json`
2. **Fill in your Google service account details**
3. **Test:** `export PATH="/data/.local/bin:$PATH" && python3 calendar-gateway-setup.py`
4. **Done.** Calendar reminders start at 9 PM Paris time automatically.

## Setup (Detailed)

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

## File Structure & Documentation

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

### Documentation Guide

#### Core Configuration Files

**SOUL.md** — *The Agent's Personality*
- Defines Sopialis' core values, approach, and boundaries
- How the agent should behave and interact
- Principles for handling external actions (emails, posts, etc.)
- Read this first to understand the agent's philosophy

**IDENTITY.md** — *Who Sopialis Is*
- Name: Sopialis
- Creature type: AI Assistant
- Vibe: Helpful, organized, resourceful
- Emoji: 🧭
- Avatar: (can be set to workspace-relative path or URL)

**USER.md** — *About You (Axel)*
- Your name, timezone, username
- Notes about your preferences and priorities
- Context about projects you're working on
- Updated as Sopialis learns more about you

**MEMORY.md** — *Long-Term Memory*
- Curated memories of important decisions and context
- NOT raw logs (those go in `memory/YYYY-MM-DD.md`)
- Only loaded in main session (not shared contexts)
- Updated periodically from daily notes
- Persists between sessions

#### Operational Files

**HEARTBEAT.md** — *Periodic Health Checks*
- Defines what tasks run during heartbeat polls
- Currently monitoring: Google Calendar (next 24-48h)
- Pending: Daily search topics
- Frequency: Every 30 minutes (or custom interval)
- Used to avoid constant polling; batches multiple checks

**CRON.md** — *Scheduled Tasks*
- Exact-time scheduled jobs (like Unix cron)
- Currently: Daily reminder at 9 PM Paris time
- Format: Time, frequency, what to do, where to send output
- Use when precise timing matters or isolation is needed

**TOOLS.md** — *Tool Configuration*
- Local, environment-specific settings
- Google Calendar IDs and service account info
- Voice preferences, device names, SSH hosts
- Skills are generic; TOOLS.md is unique to your setup

#### Scripts & Automation

**calendar-sync.py** — *Full Calendar Sync (Python)*
- Uses Google Calendar API directly
- Fetches events with full details (time, location, attendees)
- Requires Google libraries installed
- Used for testing and manual syncs

**calendar-gateway-setup.py** — *Setup & Test Gateway*
- Installs Google libraries
- Tests OAuth credentials
- Displays calendar events
- Run once to verify setup, then use calendar-sync.py

**calendar-sync.sh** — *Lightweight Sync (Bash)*
- Uses curl and standard tools
- Minimal dependencies
- Fallback when Python libraries unavailable
- Good for CI/CD or restricted environments

**calendar-reminder.sh** — *Daily Reminder Script*
- Fetches tomorrow's agenda
- Formats as readable message
- Called via CRON at 9 PM Paris time
- Sends to Telegram

#### Examples & Templates

**credentials.example.json** — *Service Account Template*
- Shows structure of Google service account credentials
- Copy this, fill in your values
- NEVER commit the real `google-calendar-credentials.json`
- Used by all calendar scripts

### How It All Works Together

#### Session Startup Sequence

1. **Agent starts** → Reads `SOUL.md` (who am I?)
2. **Session type determined** → Main session? Read `MEMORY.md` (avoid in group chats)
3. **Check daily context** → Read `memory/YYYY-MM-DD.md` (what happened today?)
4. **Read user profile** → `USER.md` (who am I helping?)
5. **Ready to assist** → Follow SOUL.md principles and HEARTBEAT.md tasks

#### Heartbeat Flow (every 30 min)

1. **HEARTBEAT.md is read** strictly (no inference, no old tasks)
2. **Active tasks executed:**
   - Check Google Calendar (next 24-48h)
   - Run daily searches (once configured)
3. **Report format:** Clean summary if something's urgent, otherwise silent
4. **Batches multiple checks** to reduce API calls and messages

#### Daily Reminder Flow (9 PM Paris)

1. **CRON task triggers** at exact time
2. **calendar-reminder.sh runs:**
   - Fetches TOMORROW's events
   - Formats as readable message
   - Sends to Telegram
3. **Both calendars combined** in one message (pro + personal)
4. **Runs automatically** every evening

#### Memory Update Flow (periodic)

1. **During heartbeat:** Review `memory/YYYY-MM-DD.md` files
2. **Extract key moments:** Important decisions, lessons, context
3. **Update MEMORY.md:** Add to long-term memory
4. **Clean up old entries:** Remove things no longer relevant
5. **Persist between sessions:** Memory survives agent restarts

### File Ownership & Editing Rules

| File | Who Edits | When | Impact |
|------|-----------|------|--------|
| SOUL.md | Axel | When values/principles change | Agent behavior |
| IDENTITY.md | Sopialis | On setup | How agent presents itself |
| USER.md | Sopialis | Learns over time | Personalization |
| MEMORY.md | Sopialis | Periodically (heartbeat) | Long-term continuity |
| HEARTBEAT.md | Axel | To add/remove checks | What runs automatically |
| TOOLS.md | Sopialis | As needed | Tool configuration |
| CRON.md | Axel | To change timing | When tasks run |
| Daily notes | Sopialis | Every session | Raw logs (not committed) |

### Integration with OpenClaw

**Heartbeat Plugin** — Runs HEARTBEAT.md tasks every 30 minutes
- Calls `memory_search` to find relevant context
- Executes active tasks (calendar sync, searches)
- Reports urgent items, stays silent otherwise

**Cron/Scheduler** — Runs exact-time jobs
- 9 PM Paris: Daily calendar reminder
- Isolated from main session (no memory pollution)
- Direct output to Telegram

**Channel Integration** — Routes to Telegram
- Messages sent via OpenClaw's message tool
- Works with configured account
- Supports reactions, inline buttons, etc.

### Updating This Documentation

When Sopialis makes significant changes:
1. Edit the relevant `.md` file
2. Update version date in footer
3. Commit to git
4. Push to GitHub

If adding new features:
1. Create new `.md` file or update existing
2. Update file structure section above
3. Document in integration section
4. Add to HEARTBEAT.md or CRON.md if it's a task

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

## Examples & Real Usage

### Example 1: What Happens at 9 PM

Every evening at 9 PM Paris time:

```
📅 Tomorrow's Agenda - Thursday, April 09, 2026
==================================================

Pro Calendar (axel.dhondt@sopial.fr):
  • 10:00 - Team standup 📍 Zoom
  • 14:30 - Client call 📍 Microsoft Teams
  • 16:00 - Project review

Personal Calendar (dhondt.ax@gmail.com):
  • 19:00 - Dinner with friends 📍 Le Petit Bistro, 33000 Bordeaux

==================================================
```

This message appears in Telegram automatically. No action needed.

### Example 2: Adding a New Search Topic

When Axel provides 2-3 search topics:

1. **Update HEARTBEAT.md:**
   ```markdown
   ## Active Tasks
   - **Google Calendar sync** — ✅
   - **Daily searches** — Check: AI news, French startups, tech jobs
   ```

2. **Sopialis adds a search script** that runs during heartbeat

3. **Results appear in periodic summaries** (or urgent alerts if relevant)

### Example 3: Updating Your Profile

If Axel changes priorities:

1. **Edit USER.md:** Update notes, timezone, etc.
2. **Edit SOUL.md:** If values/principles change
3. **Commit & push:** `git add . && git commit -m "Update profile" && git push`

Sopialis will read these on next session and adapt behavior.

### Example 4: Memory Persistence

**Day 1:** Axel mentions "I'm working on Project X, very important"
- Sopialis logs it to `memory/2026-04-08.md`

**Day 3:** Sopialis reviews daily files and updates MEMORY.md
- Adds: "Project X is a priority. Mentioned: 2026-04-08"

**Month 2:** Even though daily file is old, MEMORY.md still has it
- Sopialis remembers without reading 30+ daily files
- Uses memory to prioritize updates

### Example 5: Manual Calendar Check

Anytime Axel wants to manually check calendars:

```bash
export PATH="/data/.local/bin:$PATH"
python3 calendar-gateway-setup.py
```

Output shows today + next 48 hours formatted nicely.

## Common Tasks

### Change Calendar Reminder Time

Edit `CRON.md`:
```markdown
**Schedule:** Every day at 10 PM Paris time (21:00 UTC / 22:00 CEST)
```

Then restart the cron job.

### Add a New Calendar

1. **Share it with:** `calendar@sopialis.iam.gserviceaccount.com`
2. **Update TOOLS.md:** Add new calendar ID
3. **Update HEARTBEAT.md:** Add to "Calendars" section
4. **Test:** Run `python3 calendar-gateway-setup.py`

### Disable Daily Reminders

Edit `HEARTBEAT.md` and comment out the calendar sync task:
```markdown
# - **Google Calendar sync** — Check upcoming events
```

### Export Agenda to Calendar File

Use Google Calendar's export feature directly (Settings → Import & Export).

## Architecture Notes

### Why Service Accounts?

- ✅ No password needed (secure)
- ✅ No 2FA (automation-friendly)
- ✅ Read-only access (safe)
- ✅ Automatic token rotation (no maintenance)
- ❌ Only calendar access (can't sync other Google services)

### Why Separate Files?

- **SOUL.md** = Philosophy (rarely changes)
- **MEMORY.md** = Learned context (evolves slowly)
- **HEARTBEAT.md** = Active tasks (changes per session)
- **CRON.md** = Scheduled jobs (changes per deployment)
- **TOOLS.md** = Environment config (unique per setup)

Each file has a clear purpose. Mixing them would make the agent harder to control.

### Why Not One Config File?

A single `config.json` would be:
- Hard to diff in git (SOUL changes look like TOOLS changes)
- Unclear which parts run when (heartbeat vs cron vs startup)
- Risky (editing one field could break everything)

Separate files = clear ownership, easier debugging, safer updates.

## Troubleshooting by Symptom

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "No events found" | Calendar not shared | Add SA email as Viewer |
| "ModuleNotFoundError: google" | Libraries not installed | `pip install --break-system-packages ...` |
| "Token expired" | OAuth cache issue | Delete `.cache/gcal-token` and retry |
| "9 PM reminder never fires" | CRON not running | Check OpenClaw cron service |
| "Calendar sync is slow" | Too many events | Filter by date range in script |

## Future Enhancements

- [ ] Configure daily search topics
- [ ] Add email integration (Himalaya CLI)
- [ ] Calendar conflict detection
- [ ] Meeting prep automation
- [ ] Custom reminder triggers
- [ ] Slack/Discord integration
- [ ] Weekly digest (instead of daily)
- [ ] Calendar analytics (busy vs free time)

## License

Private repo for Axel's personal use.

---

**Agent:** Sopialis  
**Last updated:** 2026-04-08  
**Status:** ✅ Calendar sync active, 🔄 searches pending, 📅 reminders at 9 PM Paris time
