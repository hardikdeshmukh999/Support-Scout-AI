# Support Scout AI

**An intelligent ticket router** that reads messy customer messages, understands intent, and maps each case to the right **sub-department and human owner**—using your org chart as the single source of truth.

---

## The idea in one breath

Traditional queues dump everything into one inbox. **Support Scout** sits in the middle: it uses a fast LLM to **classify** each ticket (with urgency and a short summary), but it is **not allowed to invent teams**. It must pick from the sub-departments defined in your **company directory**. That choice is then joined to real **names and emails**, so routing stays grounded in data you control.

---

## Why it matters

| Principle | What it does |
|-----------|----------------|
| **Constrained AI** | The model only outputs labels that exist in your directory—no hallucinated departments. |
| **CSV-first** | Departments, sub-departments, and owners live in plain data; swap rows, not code, to reorganize. |
| **Structured output** | JSON from the API gives `sub_department`, `urgency`, and `summary` for dashboards or ticketing tools later. |
| **Fast & cheap to try** | Runs on [Groq](https://console.groq.com/) with **Llama 3.1 8B** (`llama-3.1-8b-instant`), ideal for prototyping. |

---

## How it works

1. **Build** a company directory and a ticket queue (written to `data/` as CSVs on each run).
2. **Analyze** each ticket: the LLM returns JSON aligned with your sub-department list.
3. **Route** by matching that sub-department to the right row in the directory and printing the assigned agent and email.

If the model returns an unknown label, the flow falls back to a general queue owner.

---

## Example

**Input** (one row from the ticket queue—the “customer message”):

```text
Excel keeps crashing every time I try to run a VLOOKUP macro. It's totally broken on Windows 11.
```

**Output** (terminal—abbreviated):

```text
------------------------------------------------------------
🎫 TICKET ID: T-101
💬 CUSTOMER: 'Excel keeps crashing every time I try to run a VLOOKUP macro...'
🤖 AI THINKS: [Urgency: High] | Excel crashes with VLOOKUP macro
🎯 ROUTING TO: Dave in Technical Support -> Software Bugs
✉️ ACTION: Ticket forwarded to dave@msoffice.com
------------------------------------------------------------
```

The LLM’s JSON is the bridge; the **directory CSV** turns the chosen sub-department into a real person.

---

## Setup

1. Clone the repo and enter the folder.
2. Python **3.10+** recommended.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root (you can copy `.env.example` and rename):

   ```bash
   GROQ_API_KEY=your_key_here
   ```

   Get a free key at [Groq Console](https://console.groq.com/).

5. Run:

   ```bash
   python support_scout_v2.py
   ```

Output prints in the terminal. Generated files go to `data/` (ignored by git so you don’t commit local runs).

---

## Project layout

| File | Role |
|------|------|
| `support_scout_v2.py` | Generates sample data, calls Groq, routes tickets |
| `requirements.txt` | `groq`, `pandas`, `python-dotenv` |
| `.env` | Your API key (local only—never commit) |

---

## Customize

- Edit **`create_company_directory()`** to change departments, sub-departments, agents, and emails.
- Edit **`create_ticket_dataset()`** to add or change sample tickets.
- On Windows, the script sets UTF-8 stdout so emoji in logs render correctly in the terminal.

---

## Docs

- https://docs.google.com/document/d/13EEcwAFOGzy2d7xyfgbY75H9Ju7E3NokDSVkdA7xYIg/edit?pli=1&tab=t.0


---

## License

Use and modify freely for learning and prototyping.
