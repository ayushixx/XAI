# 8BIT Workforce Intelligence Platform

## Architecture
The application is a Streamlit dashboard located in the `app/` directory.
It strictly consumes the `artifacts/` JSON files representing the validated Evidence Store.

## Running the App
```bash
streamlit run app/streamlit_app.py
```

## Pages
1. **Overview**: Landing page showing dataset metrics and the 8BIT framework.
2. **Market Intelligence**: Displays market demand signals.
3. **Capability Intelligence**: Displays validated JDS signals (e.g. Maths-Stats, Coding).
4. **Senior Success**: Displays validated SDS personality signals with strict disclaimers.
5. **8BIT Signal Map**: The fusion page demonstrating the distinction between Market, Capability, and Success.
6. **Evidence Explorer**: Full transparency table of odds ratios, p-values, and CV metrics.

## Design Decisions
- Dark mode enforced via `.streamlit/config.toml`.
- Persistent footer enforcing "No causal claims".
- Caching (`@st.cache_data`) used for JSON loads to ensure performance.
- Direct JSON parsing rather than reinventing the Signal Engine logic, maintaining truth alignment.
