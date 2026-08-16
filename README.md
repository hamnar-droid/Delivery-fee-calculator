# 🚚 Delivery Fee Calculator

A cute Streamlit app that calculates delivery fees based on package weight, delivery distance, and fragility — built for the *Practical Task: Delivery Fee Calculator* assignment.

🔗 **Live app:** _add your Streamlit link here_

## What it does

Enter a customer's package details and instantly get a delivery bill. Every customer calculated in a session is added to a running table so you can see the full order history and total revenue.

**Inputs:**
- Customer Name
- Package Weight (kg)
- Delivery Distance (km)
- Fragile? (Yes/No)

**Pricing logic:**
```
Base Cost = $5 flat fee + (weight × $2) + (distance × $0.5)
Surcharge = $5 if distance > 10km OR package is fragile
Final Bill = Base Cost + Surcharge
```

## Features

- 📋 Form-based input with validation (no empty names, no zero/negative weight or distance)
- 🧾 Styled bill card for the most recent customer
- 📊 Session table of all customers calculated, with a running total
- 🔄 "Start Over" button to clear the session

## Tech stack

- [Streamlit](https://streamlit.io/) — UI and app framework
- [pandas](https://pandas.pydata.org/) — session history table

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

## About

This app is a Streamlit front end for a console-based delivery fee calculator originally written in Python, using a function + input loop to handle multiple customers. Built as the bonus (+5) portion of the assignment.
