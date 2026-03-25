# Architecture

## Overview
A simple desktop calculator built with PyQt6, structured to separate
UI concerns from business logic.

## Project Structure
The source code lives in `src/calculator/`. The entry point is `main.py`,
the UI is in `view.py`, and all arithmetic logic is in `model.py` with
no PyQt6 dependencies. Tests live in `tests/`.

## Key Design Decision: Separation of Concerns

`model.py` contains zero PyQt6 imports. All arithmetic and state
management lives there. `view.py` owns the UI and delegates all
calculation work to `CalculatorLogic`.

This means:
- `model.py` can be unit tested without launching a GUI
- The UI can be replaced without touching the arithmetic code

## Data Flow
```
User clicks button
view.py receives signal
model.py processes input, returns display string
view.py updates QLineEdit display
```