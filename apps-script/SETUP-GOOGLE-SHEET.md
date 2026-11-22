# Set up the score Google Sheet (about 10 minutes)

Do these steps once. You need your Google account.

1. Go to **sheets.google.com** and click **Blank spreadsheet** (the big +).
2. Click "Untitled spreadsheet" at the top left and name it **P6 Maths Scores**.
3. In the menu, click **Extensions**, then **Apps Script**. A new tab opens.
4. In the new tab, delete everything in the code box.
5. Open the file `apps-script/Code.gs` from the website folder. Copy all of it and paste it into the code box.
6. Click the **💾 Save** icon.
7. Click the blue **Deploy** button (top right), then **New deployment**.
8. Click the **⚙️ gear** next to "Select type" and choose **Web app**.
9. Fill in:
   - Description: `scores`
   - Execute as: **Me**
   - Who has access: **Anyone**
10. Click **Deploy**.
11. Google asks for permission. Click **Authorize access**, then pick your account.
    - If you see "Google hasn't verified this app": click **Advanced**, then **Go to (project name) (unsafe)**. This is safe because it is your own script.
    - Click **Allow**.
12. Copy the **Web app URL** (it starts with `https://script.google.com/macros/s/` and ends with `/exec`).
13. Open `js/config.js` in the website folder. Paste the URL between the quotes:
    `const SHEET_URL = "https://script.google.com/macros/s/....../exec";`
    Save the file. (Or just send me the URL and I will paste it in for you.)

## Check it works
- Paste the web app URL into your browser. You should see: **T. Roy score receiver is working ✅**
- Play one Speed Quiz on the website. A new tab called **Scores** appears in your sheet with one row.

## Leaderboard
The same web app also feeds the 🏅 Leaderboard page. Nothing extra to set up. Once the URL is in `js/config.js`, the leaderboard shows every class's Unit Test results.

## Good to know
- Columns: Date and time, Name, Class, Unit, Section, Activity, Score, Total, Time taken (s).
- Speed Quiz: Score = number correct out of 10. Match Game: Score = pairs matched. Unit Test: Score = number correct out of 20. Time is always in seconds.
- If a student has no internet, the score waits in their browser and is sent next time they open the site.
- If you change Code.gs later: Deploy > **Manage deployments** > ✏️ edit > Version: **New version** > Deploy. The URL stays the same.

## Update to code v5: class lists and teacher PIN
Do this once. It takes about 5 minutes.

1. Open your sheet **P6 Maths Scores**, then **Extensions > Apps Script**.
2. Delete everything in the code box. Paste the new `apps-script/Code.gs`. Click **💾 Save**.
3. Set your teacher PIN (it is never written in the code or on GitHub):
   - Click the **⚙️ Project Settings** (gear on the left).
   - Scroll to **Script properties**, click **Add script property**.
   - Property: `TEACHER_PIN` · Value: your PIN (for example 6 digits only you know).
   - Click **Save script properties**.
4. Click **Deploy > Manage deployments**, click ✏️ (edit), set **Version: New version**, click **Deploy**. The link stays the same.
5. Check: open the web app link. It should say **(code v5)**.

## The Students tab
- Column A class, B class number, C nickname. Column D is worked out for you: it adds "(No. 3)" when 2 students in one class share a nickname.
- To fix a spelling or add a new student, edit columns A to C. The website picks up the change the next time a student opens it.

## Teacher login
- On the website, type **teacher** or **Lawrence** in the name box (or click "Teacher login"), then your PIN.
- Google checks the PIN. After 5 wrong tries it pauses for 10 minutes.
- The PIN is remembered only until the browser is closed.
