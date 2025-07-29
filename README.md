# YAML to Prob2Trace Converter

This script converts `.yaml` simulation output files into `.prob2trace`, **Prob2Trace**-compatible format, applying necessary **calculations and transformations** based on deceleration test scenarios.

The `.yaml` input files are generated from simulation experiments using **Autoware with AWSIM**, specifically in **deceleration scenarios**. While the script has not been tested on other JAMA framework scenarios (e.g., cut-in, cut-out), it may still be compatible.

---

## What Can It Do?

- Automatically converts all `.yaml` files inside the `/Input` folder
- Modifies and calculates relevant values
- Saves converted traces into the `/Output` folder in `.prob2trace` format

---

## Repository Structure

```
.
├── Input/                  # Place your raw YAML files here
├── Output/                 # Converted Prob2Trace-compatible files will be saved here
├── yamlToProb2trace.py     # Main script for conversion logic
```

---

## How to Run

> Make sure your `.yaml` files are inside the `./Input` folder.

Then run:
```bash
python yamlToProb2trace.py
```

> All converted files will be automatically written to `./Output`.

---

## Dependencies

This script uses only the Python standard library:

- `pathlib`

> No additional packages required.

---

## 📘 License

This project is released under a **custom fair-use license**:

> You are free to use, modify, and build upon this work for educational or research purposes. However, **citation of this repository is required** if any significant part of the idea or code is reused in derivative works. Commercial use or direct copying without attribution is not allowed.

---

## Notes

- The system is currently tailored for **deceleration scenario** outputs from AWSIM + Autoware.
- Other JAMA driving test patterns (e.g., cut-in/cut-out) have not yet been verified.
- Contributions and test reports on other scenarios are welcome!

---

## Acknowledgements

- Autoware & AWSIM simulation toolchain
- JAMA framework for autonomous driving testing

