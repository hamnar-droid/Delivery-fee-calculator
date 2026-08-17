# 📮 Parcel Waybill — Delivery Fee Calculator

A Streamlit app styled like a parcel shipping label, built for the *Practical Task: Delivery Fee Calculator* assignment. Every calculation gets stamped with a tracking number and a postmark, like a real waybill receipt.

🔗 **Live app:** https://delivery-fee-calculator-dpg9pipt8iwd4k266w7mes.streamlit.app/

## What it does

Enter a customer's package details and the app stamps out a waybill receipt with a tracking number, an itemized cost breakdown, and a postmark for the total. Every parcel calculated in a session is added to a running manifest table with a running total.

**Inputs:**
- Customer
- Weight (kg)
- Distance (km)
- Fragile? (Yes/No)

**Pricing logic:**
```
Base Cost = $5 flat fee + (weight × $2) + (distance × $0.5)
Surcharge = $5 if distance > 10km OR package is fragile
Final Bill = Base Cost + Surcharge
```

## Design

Styled around the vernacular of shipping and postage rather than a generic form:

- Kraft-paper background with a typewriter display face (Special Elite) and monospace data fields (JetBrains Mono)
- A dashed perforation line under the input form, like a tear-off ticket
- A tilted "FRAGILE" stamp badge when the package is marked fragile
- Auto-incrementing tracking numbers (`PW-00042`, `PW-00043`, ...)
- A rotated postmark stamp over the final total, dated to the day the parcel was calculated

## Features

- 📮 Waybill-style form with validation (no empty names, no zero/negative weight or distance)
- 🧾 Receipt-style card for the most recently calculated parcel
- 📋 Session manifest table of every parcel calculated, with a running total collected
- 🗑️ "Clear manifest" button to reset the session

## Tech stack

- [Streamlit](https://streamlit.io/) — UI and app framework
- [pandas](https://pandas.pydata.org/) — session manifest table

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Theme colors matching the waybill design |

## About

This app is a Streamlit front end for a console-based delivery fee calculator originally written in Python, using a function and an input loop to handle multiple customers. Built as the bonus (+5) portion of the assignment.
