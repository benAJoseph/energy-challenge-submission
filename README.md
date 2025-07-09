# Energy Challenge Solution 

This repository contains my solution to the 3-phase motor energy analysis challenge.

---

## Results

```

Challenge 1 - Energy Consumption (kWh):
{'vampire': 4, 'idle': 0, 'normal': 72, 'overload': 0}

Challenge 2 - Duration Periods:
{'vampire': \[('00:00', '11:48'), ('12:39', '23:59')],
'idle': \[('11:48', '11:48')],
'overload': \[]}

Challenge 3 - Energy Costs (paise):
{'vampire': 3226, 'idle': 11}

````

---

## Implementation Highlights

### Motor Setup

- Equipment rating: **90 kW**
- Efficiency: **0.9**
- Derived motor rating: `90 / 0.9 = 100 kW`
- Service Factor: **1.2**

This means:
- **Vampire**: `0 < power ≤ 1%` of 100 kW (≤ 1 kW)
- **Idle**: `1% < power ≤ 30%` (≤ 30 kW)
- **Normal**: `30% < power ≤ 120%` (≤ 120 kW)
- **Overload**: `power > 120%` (> 120 kW)

---

## Challenge Breakdown

### Challenge 1: Energy Usage by Condition

Total energy consumption per condition was calculated by summing `energy` values in `energy.csv` after classifying each row by operating state.

**Energy values are converted from Wh → kWh** (rounded to nearest integer).

---

### Challenge 2: Continuous Operating Periods

Using `power.csv`, each timestamped power reading is mapped to an operating condition. Continuous blocks of each state are then grouped and labeled with start and end times.

### Motor State Timeline
![Motoe state timeline](img/motor%20state%20time%20line.png)

---

### Challenge 3: Cost of Inefficiency

Tariff-based cost calculations were applied on `energy.csv`, using time-based slab rates:

| Time Range  | Tariff (paise/kWh) |
| ----------- | ------------------ |
| 06:00–18:00 | 790                |
| 18:00–22:00 | 1185               |
| 22:00–06:00 | 593                |

Only **vampire** and **idle** states are considered for this challenge.



---

## How to Run

Ensure the following files are in your working directory:

* `main.py` — main script
* `tariff.py` — tariff function (returns slab-based tariff rates)
* `energy.csv` and `Power.csv` — input datasets

Then simply run: python main.py


## Assumptions

* Time fields are ISO-formatted and timezone-aware (e.g., `2023-07-08T14:45:55+00`).
* Power readings are in watts and summed over 3 phases.
* Energy values are in watt-hours.
* Missing rows or edge cases are skipped gracefully.
* Tariff logic is handled by `tariff.py`.

---

## AI Usage Disclaimer

This readme was partially structured and refined using **OpenAI ChatGPT (GPT-4)** to:

* Enhance readability
* Improve overall quality by using visualizations
* Suggest optimal visual formats



