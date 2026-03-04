# Security Toolkit: Password Analyzer

A Python desktop application designed to audit password security and promote better InfoSec habits.

## Key Features
- **Breach Check:** Uses k-anonymity to check passwords against the "Have I Been Pwned" API.
- **Brute-Force Estimator:** Calculates time-to-crack based on character set entropy.
- **SHA-256 Hashing:** Generates cryptographic fingerprints for demonstration.
- **Secure Generator:** Uses the `secrets` module for high-entropy password creation.

## Tech Stack
- **Language:** Python 3.x
- **Library:** Tkinter (GUI), Hashlib, Secrets

## How to Run
```bash
python parole.py