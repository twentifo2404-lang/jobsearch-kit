# Tutorial: let Claude apply for jobs for you

This guide is for complete beginners. You don't need to know anything about coding, Claude Code or GitHub. Follow the steps in order. The first time takes about **30–45 minutes**. After that, starting a new batch of applications takes one sentence.

---

## What you're setting up

There are four pieces. Each step below sets up one of them.

| Piece | What it is | Why you need it |
|---|---|---|
| **A Claude subscription** | A paid Claude account | The free plan can't run the tools this kit uses |
| **The Claude desktop app** | The Claude program on your computer | Its **Code** tab is where Claude works with the files on your computer |
| **Claude in Chrome** | An add-on for the Google Chrome browser | Lets Claude open job sites and fill in forms in your own browser |
| **The Job Search Kit** | A folder you download (this project) | Holds your CVs, your answers and the list of jobs already applied to |

> **How it works, in one sentence:** you tell Claude "apply for 10 jobs", and it searches job sites in your Chrome, fills in each form using answers you've already confirmed, and writes every application into a log so it never applies to the same job twice. You stay in charge of passwords, consent boxes and anything you'd want to check first.

---

## Step 1: Subscribe to Claude

1. Go to **https://claude.ai** and click **Sign up**. Use the email you want to keep using (Google sign-in is fine).
2. Once you're in, open the menu at the bottom-left (your name or initials) → **Settings** → **Billing**, or go to **https://claude.ai/upgrade**.
3. Choose **Pro**. That's the cheapest paid plan and is enough to start. Check **https://claude.com/pricing** for the current price in your currency.
   - If you later find Claude says you've hit your usage limit too often in a day, you can move up to a **Max** plan. Most people start with Pro.
4. Pay with your card. **You** type the card details. Never paste card details into a chat with Claude.

✅ **Done when:** your account page shows the **Pro** plan.

---

## Step 2: Install the Claude desktop app

1. Go to **https://claude.ai/download** and download the app for your computer (**Mac** or **Windows**).
2. Install it:
   - **Mac:** open the downloaded file and drag **Claude** into **Applications**. Then open it from Applications.
   - **Windows:** open the downloaded installer and follow the prompts.
3. Open the app and **sign in** with the same account as Step 1.
4. At the top of the app you'll see tabs such as **Chat** and **Code**. You'll use the **Code** tab. (If you don't see it, make sure the app is up to date and you're on a paid plan.)

✅ **Done when:** you can click the **Code** tab while signed in.

---

## Step 3: Install Google Chrome and Claude in Chrome

Claude fills in job applications inside Chrome, so this step matters.

1. If you don't have **Google Chrome**, download it from **https://www.google.com/chrome** and install it.
2. In Chrome, go to the **Chrome Web Store** and search for **Claude** (the extension published by **Anthropic**). Click **Add to Chrome**.
   - Check that the publisher is **Anthropic**. Ignore look-alike extensions.
3. Click the puzzle-piece icon at the top-right of Chrome and **pin** Claude so it's always visible.
4. Click the Claude icon and **sign in** with the same Claude account.
5. In the same Chrome, **sign in to your job sites**: LinkedIn, JobStreet, Indeed, whatever you use. Claude uses whatever account is signed in there.

> ⚠️ **Sharing a computer?** If someone else's LinkedIn or email is also signed in on this Chrome, use a separate Chrome profile for yourself (Chrome menu → **Profiles** → **Add**) so Claude never applies from the wrong account.

✅ **Done when:** the Claude icon is pinned in Chrome and you're signed in to your job sites.

---

## Step 4: Download the Job Search Kit

You **don't** need a GitHub account for this.

1. Click this link to download the kit as a ZIP file:
   **https://github.com/twentifo2404-lang/jobsearch-kit/archive/refs/heads/main.zip**
2. Open your **Downloads** folder and **unzip** it:
   - **Mac:** double-click the ZIP.
   - **Windows:** right-click the ZIP → **Extract All…** → **Extract**.
3. You'll get a folder called **`jobsearch-kit-main`**. Rename it to **`jobsearch`** if you like, and **move it to your Desktop** (or Documents) so it's easy to find. Don't leave it in Downloads.

<details>
<summary>Already use GitHub? (optional)</summary>

Open https://github.com/twentifo2404-lang/jobsearch-kit, click **Use this template** → **Create a new repository**, set it to **Private**, then clone your copy. Your personal files are git-ignored, so they won't be uploaded.
</details>

✅ **Done when:** you have a `jobsearch` folder on your Desktop with files like `README.md`, `jobs.py` and a `cv` folder.

---

## Step 5: Put your CVs in the kit

1. Open the `jobsearch` folder, then the **`cv`** folder inside it.
2. Copy your CV **PDFs** into `cv/`. If you have different CVs for different kinds of jobs (for example, an engineering one and a business one), put them all in.
3. Give them clear names, like `Sam_Lee_Engineering_CV.pdf`.

> Your CVs stay on your computer. Nothing in this folder gets uploaded anywhere unless Claude attaches it to a job application you asked for.

---

## Step 6: Open the kit in Claude and set yourself up

1. Open the **Claude desktop app** → **Code** tab.
2. Start a new session and **choose your `jobsearch` folder** as the folder to work in. If the app asks whether you **trust** this folder, say yes. It's your own folder.
3. In the message box, type:

   > **set me up**

4. Claude will:
   - check your computer has **Python** (a small free program the kit needs). If it's missing, Claude tells you how to install it:
     - **Mac:** a pop-up may offer to install "command line developer tools". Click **Install** and wait for it to finish.
     - **Windows:** install it from **https://www.python.org/downloads/**. On the first installer screen, **tick "Add python.exe to PATH"** before clicking Install.
   - **read your CVs** and show you what it found (name, degree, experience, skills). Correct anything that's wrong.
   - **ask you questions** in small batches: what jobs you want, which cities, your salary, what you won't do (industries, languages, years of experience), and the usual form questions (notice period, driving licence, work rights…).
5. Answer honestly. **If you're not sure, say "ask me each time".** Claude will never make up an answer.
6. At the end Claude writes everything into a file called **`HANDOFF.md`**. Open it and read it once. **Everything Claude puts on a form comes from this file or your CV.**

✅ **Done when:** Claude says setup is finished and `HANDOFF.md` exists in your folder.

---

## Step 7: Your first batch of applications

1. Make sure **Chrome is open** with the Claude extension signed in.
2. In the same Code session (or a new one in the same folder), type something like:

   > **apply for jobs: 5 from LinkedIn, posted in the last 3 days**

   Start small (5 jobs) the first time so you can watch how it works.
3. Claude will:
   1. search the job site in your Chrome
   2. read each ad and skip the ones that break your rules (and note why)
   3. show you a **shortlist** and wait for your OK
   4. apply one by one, picking the right CV and filling in the answers from `HANDOFF.md`
   5. write every application, skip and failure into `application_log.csv`
4. You can watch it work in Chrome. You can type in the chat at any time ("skip this one", "stop", "use my business CV instead").

---

## What Claude will ask *you* to do

Claude is set up to hand these to you. This is normal and is there to protect you:

| When this comes up | What you do |
|---|---|
| **A password or sign-in** | Click into Chrome and type it yourself. Then tell Claude "done". |
| **A new account on a company's careers site** | Claude fills in the form; **you** type the password. |
| **"I agree to the terms / privacy policy" boxes** | Claude asks first. Read it, then tick it yourself or tell Claude it's OK. |
| **A question your file doesn't cover** | Answer in the chat. Claude saves the answer to `HANDOFF.md` so it won't ask again. |
| **IC / passport / bank numbers** | Always you. Claude won't type them. |
| **Messages to recruiters** | Claude shows you the draft and only sends after you say yes. |
| **Online tests and video interviews** | These are for you to take. Claude will remind you of deadlines. |
| **The app asks "Allow Claude to …?"** | That's the app checking with you before Claude runs something or opens a site. Read it and click **Allow** if it matches what you asked for. |

---

## Every time after that

Open the Claude app → **Code** → your `jobsearch` folder, and say one of these:

- **"apply for 10 jobs from JobStreet and LinkedIn, last 3 days"**
- **"apply to this job: <paste the link>"**
- **"show me what you applied to this week"**
- **"I want to add remote jobs to my search"** (Claude updates `HANDOFF.md`)
- **"check my email for interview invites or rejections"** (if you've connected your email to Claude)

Tip: a fresh search every 2–3 days works better than one huge batch. New jobs get posted all the time.

---

## Two people on one computer

Say:

> **set up a second person called sam**

Their CVs, answers and log go into `candidates/sam/`, completely separate from yours. When it's their turn, say **"apply for jobs for sam"**.

---

## Troubleshooting

**Claude says it can't control the browser / Chrome isn't connected**
Make sure Chrome is open, the Claude extension is installed and signed in with the **same account** as the desktop app. Then try again.

**"python3: command not found" (or "python is not recognized")**
Python isn't installed yet, or wasn't added to PATH. See Step 6. On Windows, reinstall it and tick **"Add python.exe to PATH"**. Then close and reopen the Claude app.

**Claude applied from the wrong LinkedIn account**
Sign out of the other account in Chrome, or use your own Chrome profile (Step 3). Tell Claude, so it notes it in `HANDOFF.md`.

**"You've reached your usage limit"**
Pro plans have a usage limit that resets after a few hours. Wait, or move up to a Max plan if it keeps happening.

**A job site asks "are you a robot?"**
Solve it yourself, then tell Claude to carry on. Claude won't solve these.

**LinkedIn warns about unusual activity**
Slow down: smaller batches, spread across the day. Job sites don't like accounts that apply very fast.

**I want to start over**
Delete `HANDOFF.md` and say "set me up" again. Your log of past applications stays, so nothing gets applied to twice.

---

## Good habits

- **Check the first few applications yourself**: open the job site's "Applied jobs" page and make sure the answers look right.
- **Keep `HANDOFF.md` honest and up to date.** It's your voice on every form.
- **Don't apply to everything.** Ten good-fit applications beat fifty random ones.
- **Back up the folder** now and then (copy it to a USB drive or cloud storage). The log is your record of where you applied.
