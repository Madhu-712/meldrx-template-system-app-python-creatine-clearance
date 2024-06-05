# MeldRx Template System App in Python +Streamlit
Diabetes Risk Score

## Getting Started
Before launching the app ensure the following configuration steps have been followed:

- app secret is set
  - in `.env` file
  - set the `MELDRX_CLIENT_SECRET` value
  - to reset your secret, go to `Apps` -> your app -> `Manage Secrets`
- workspace configuration
  - system applications require special permissions to workspaces
    - go to `Workspaces` -> your workspace -> `Settings` -> `Apps` -> press `Add Workspace App`
    - add your app as Administartor
  - if the workspace is `standalone`
    - you will want to seed it with a patient that you can select to view in this app.
    - go to https://app.meldrx.com/ccda?sample=sample1
    - copy paste the ccda xml in to a new file such as `ccda.xml`
    - go to `Workspaces` -> your workspace -> `Patients` -> click on `Import Data`
    - select the `ccda.xml` file
  - if the workspace is `linked` (to Epic or Cerner etc...)
    - you will want to ignore MeldRx storage, and only use external.
    - go to `Workspaces` -> your workspace -> `Settings` -> `Data Rules`
    - in the `Bulk Updates` section, fill out the form to:
      - `Trigger Action`: `Read`
      - `Resource Type`: `Select All`
      - `Target`: `External`
      - press `Update Rules`

#### Setup/Install

1. setup virtualenv: `python -m venv venv`
2. activate virtualenv: `source venv/bin/activate`
3. install dependencies: `pip install -r requirements.txt`

#### Run Locally
`streamlit run main.py`
