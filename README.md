# best-xi

## About
Best.XI is a college soccer analytics tool that allows coaching staffs to make unbiased, data centric decisions in recruiting and lineup selection. The tool leverages data from existing data providers (Wyscout, Statsbomb, etc.) and allows coaches to determine what metrics matter for their system. This enriches the existing data with program-specific context to make more aligned decisions.

## Demo
[![Best.XI Demo](https://img.youtube.com/vi/Y_WaIa2G1H8/0.jpg)](https://www.youtube.com/watch?v=Y_WaIa2G1H8)

## Development

* Build you virtual environment with uv:
```bash
uv sync
```

* Run the app.
```bash
uv run streamlit run app.py
```

* Make requisite edits.
    - Streamlit automatically updates live with edits, so no need to rerun app. 

## Deployment

* Download files from players of interest from Wyscout.com (must have an account)

* Launch [best-xi](https://best-xi.up.railway.app/).

* Enter password. During dev process, password is `PILOT26`

* Follow on-screen instructions.


## Origins & Change Log
### October 2023
This app started out as a [simple Jupyter notebook on Google Colab](https://colab.research.google.com/drive/19CWb7bVkXXvlHaNwo7HMbK3rfdwc2rMv). This was a product of my data analysis duties with the University of Vermont Men's Soccer program. The staff asked me to develop something that would allow them to compare players within their team by position to help with lineup decisions.

### January 2025
I converted the above notebook into a standalone app with Streamlit. I vibe coded [this](https://colab.research.google.com/drive/1XpVn_tG3W-F2ebAzWten4Mpy3IitPdd_). I sat down with my the UVM associate head coach, Brad Cole, and showed him this to see if their was any market-fit. He said he would easily pay $2k/yr for this because if they recruited 1 single player because of it, that would pay for itself.

### July 2025
After getting layed off from my MedTech start-up, I decided to give Best.XI a go. I spent a couple weeks vibe-coding a more formal app and doing cold outreach to coaches via email and cell. I didn't get much signal so began going in-person to local Boston universities and got positive signal but no sales.


### August 2025
With some singal I took to the road and traveled across the Northeast, Midwest and Quebec pitching this project in person to Harvard, Boston University, Boston College, Northeastern, the University of Vermont, Duquesne, the University of Pittsburgh, Penn State, Ohio State, Dayton, Butler, the University of Illinois-Chicago, Loyola Chicago, and Northwestern.

Received feedback that the most valuable additions would be direct integration with the NCAA transfer portal (to extract the names of available players) and with Wyscout (to automate downloading the data of these players). General sentiment was positive with most citing budgeting constrainst that would open up come Spring season.

### January 2026
- Cleaned up app.py by parameterizing data into modules and a config for constants. 
- Revised codebase architecture.
- Updated package management to use modern pyproject instead of requirements
- Updated Readme to have dev and deploy instructions as well as this change log.
- Added app repo to Railway to allow for the Streamlit app to be continuously hosted. Prior, streamlit would timeout after 12 hours. Railway keeps the app online. This is a temporary fix.
- Added unit tests.

### Future Changes
I have calls scheduled in January and early February with Northwestern, the University of Illinois-Chicago, and the University of Vermont. The purpose of these calls is to get access to their NCAA and Wyscout accounts so I can prototype integrations and to follow up to see if their needs changed as a result of a fast moving NCAA and NIL landscape. This discussions will drive infrastructure and feature decisions, but the current plan is to switch from Streamlit/Railway to Next.js (frontend), FastAPI (backend), PostgresSL (database), and Railway (deployment). I will also need to explore tools for webscrping and integrations.