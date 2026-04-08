# CRON.md - Scheduled Tasks

## Daily Calendar Reminder

**Task:** Send Axel tomorrow's agenda summary  
**Schedule:** Every day at 9 PM Paris time (20:00 UTC / 21:00 CEST)  
**Time:** Exact, no drift  
**Output:** Direct message to Axel (Telegram)

**Command:**
```
0 20 * * * /data/.openclaw/workspace/calendar-reminder.sh
```

**What it does:**
- Fetches tomorrow's events from both calendars
- Sends a clean summary: time, title, location
- No message if calendar is empty

---

### Implementation Notes

- Uses Google Calendar API with service account auth
- Handles timezone conversion automatically (Paris → UTC)
- Batches both calendars in one message to avoid spam
- Runs at exact time; no polling needed
