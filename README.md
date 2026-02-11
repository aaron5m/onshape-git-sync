# onshape-git-sync

```
    ONSHAPE DOCUMENT <----cron------> AWS EC2 / LOCAL -------push------> GITHUB

           .                            __..--"""""""""""::|     #####################
          /=\\       A          __..--""          _..--""  |     # ################# #
         /===\ \   < + >      .:________________.:| |      |     # # Github Repo   # #
        /=====\' \   v        |       ______    ||| |    ()|     # #   README      # #
       /=======\'' \          | __===::::::===__||| |()    |     # #               # #
      /=========\ ' '\        ||\_______________||| |      |     # #     /\     |  # #
     /===========\' '' \      |  | '.'..''.'|    || |      |     # #    /  \    |  # #
    /=============\' ' ' \    |  |/""""""""";.   || |     .'     # #   /____\   |  # #
   /===============\  ' ' /   |  :   x       '.  || |   .'       # #            |  # #
  /=================\   '/    |  :   x:       :  || | .'         # ################# #
 /===================\' /     | ."   x:       ". || :'           #####################
/=====================\/      |_:______________:_|:'  
```


This project automates the synchronization of **official Onshape document versions** to a GitHub repository. It is designed to showcase:

- Versioned tracking of CAD documents.
- Branching and workflow discipline.
- Automated export and commit processes.
- Clear documentation of changes over time.

Using this repository in tandem with your Onshape progress yields an automatically updated journal of snapshots for you or anyone on your team to see at:  
[https://github.com/your-username/onshape-git-sync/tree/main/snapshots](https://github.com/aaron5m/onshape-git-sync/tree/main/snapshots)

---

## Installation & Usage

Follow these steps to set up and run the Onshape snapshot automation:

0. **You will need**
  - [Docker](https://www.docker.com/get-started/) 
  - an onshape document id (the **alphanumeric** string, no slashes, in the url after document/ when you open your document)
  - an onshape API key and Secret key [Onshape API Keys](https://onshape-public.github.io/docs/auth/apikeys/)
  - a github classic personal access token [Github Classic Personal Access Token](https://medium.com/@mbohlip/how-to-generate-a-classic-personal-access-token-in-github-04985b5432c7) 

1. **Fork the repository in Github**   
then go to your own repo and continue https://github.com/your-username/onshape-git-sync

2. **Clone YOUR repository to your Local Machine or EC2
```   
git clone https://github.com/your-username/onshape-git-sync.git
cd onshape-git-sync
```

3. **Hide your environment variables from git**    
Rename your onsync.env.sample file to onsync.env
```
cp onsync.env.sample onsync.env
rm onsync.env.sample
```

4. **Set your environment variables**  
Edit your onsync.env file to include your secret information (not tracked by git)
```
ONSHAPE_DOC_ID=yourOnshapeDocId
ONSHAPE_API_KEY=yourAPIkey
ONSHAPE_SECRET_KEY=yourSecretKey
GITHUB_TOKEN=yourGithubToken
```

5. **Run the setup script**  
Execute the main shell script to build the Docker container, run it for the first time, and schedule hourly updates via cron:
```
bash start_onsync.sh
```

6. **See your utomated snapshots**  
  - The script will monitor your Onshape project for new official versions every hour.  
  - Each version is saved in the `snapshots` folder with metadata, elements, and images.  
  - Any changes are automatically pushed to your GitHub repository.
    - You, or anyone, can see them at https://github.com/your-username/onshape-git-sync/tree/main/snapshots
    - You can write an introduction above the first line in snapshots/README.md and the updater will leave your introduction alone.

---

## Drawbacks and Decisions

- **Hourly polling vs. webhooks:**  
  Currently, the pipeline uses a cron job to call the Onshape API every hour. While this approach is simple and aligns with DevOps-style CI/CD automation, it is not the most API-efficient method. Frequent polling can consume unnecessary API calls, especially for projects that update infrequently.

- **Future improvements:**  
  A more efficient approach would leverage Onshape webhooks to trigger updates only when new versions are created. This would reduce API usage and provide near real-time snapshots.  
- **Decision rationale:**  
  Using a cron-based workflow allows the project to demonstrate containerization, automated scheduling, and Git integration—core DevOps practices—while still providing a fully functional, automated snapshot pipeline. Webhook integration can be implemented in a future iteration without impacting the current functionality.

---

## Goals

1. **Mirror Official Versions**  
   Keep the GitHub repository updated only with officially released or versioned Onshape documents, not every minor change.

2. **Automate File Management**  
   Export CAD files (STEP, STL, PDF) from Onshape via the API and store them in the repository, eliminating manual intervention.

3. **Maintain Clear Commit History**  
   Include Onshape metadata in commit messages (version number, timestamp, notes) for easy traceability.

4. **Demonstrate Workflow Discipline**  
   Use branching, versioning, and automation to reflect real-world software engineering and DevOps practices.

---

## Architecture

1. **EC2 Instance**  
   - Holds a clone of the GitHub repository.
   - Runs a scheduled task (cron job) to check for new Onshape versions.

2. **Onshape API**  
   - Provides version listing and file export capabilities.
   - Returns metadata for each official version.

3. **Automation Script**  
   - Checks for new versions.
   - Downloads updated files.
   - Commits and pushes to GitHub with relevant metadata.

4. **GitHub Repository**  
   - Acts as a centralized repository for all exported files.
   - Maintains a clean history of official versions with descriptive commit messages.

---

## Planned Workflow

1. The cron job runs every hour on Local Machine or EC2 instance.
2. The script queries the Onshape API for the latest “official” version.
3. If a new version is detected:
   - Files are exported from Onshape.
   - The script commits the updates with metadata (version, timestamp, author, notes).
   - Changes are pushed to GitHub.
4. The repository reflects only official design milestones, with a clear, automated history.

---

## Directory Structure (Proposed)

```
onshape-git-sync/
├── exports/ # Exported STEP, STL, PDF files from Onshape
├── snapshots/ # Version metadata and screen-grabs from OnShape saved versions
├── scripts/ # Automation scripts (Python)
├── logs/ # Log files for cron job runs
├── CHANGELOG.md
└── README.md
```

---

## Current Functionality

This project now implements a full Onshape-to-local archive and automation pipeline:

- Fetches all versions of a specified Onshape document via the Onshape API
- Archives each API response in `logs/<timestamp>.json`
- Creates timestamped snapshot folders for each version in `snapshots/`
- Writes version information and metadata into `snapshots/<version_timestamp>/snapshot.json`
- Discovers assembly elements for each version and stores them in `snapshots/<version_timestamp>/elements.json`
- Generates shaded images for each assembly element and stores them in `snapshots/<version_timestamp>/img/`
- Writes a human-readable Markdown summary (`README.md`) into snapshots folder, including the name, description, and images of the version
- Supports offline mode, allowing the pipeline to continue from the last successful log
- Designed to be idempotent, deterministic, and observable for DevOps-style workflows
- Fully containerized with Docker for consistent execution across Linux and macOS
- Includes `start_onsync.sh` to build and run the Docker container and initialize the pipeline
- Automated cron job runs hourly to monitor the Onshape project for new official versions
- Automatic Git integration pushes new snapshots and updates to the GitHub repository whenever a new version is detected


---

## Next Steps

- Configure EC2 environment with Python, Git, and required libraries.
- Develop the automation script for fetching and committing new versions.
- Schedule the cron job for periodic syncs.

---

## References

- [Docker](https://www.docker.com/get-started/) 
- [Onshape REST API Documentation](https://onshape-public.github.io/docs/)
- [Onshape API Keys](https://onshape-public.github.io/docs/auth/apikeys/)
- [GitHub Documentation](https://docs.github.com/en)
- [Github Classic Personal Access Token](https://medium.com/@mbohlip/how-to-generate-a-classic-personal-access-token-in-github-04985b5432c7) 

