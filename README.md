# onshape-git-sync

A small-scale automation project demonstrating version tracking and workflow automation for Onshape CAD documents. This repository mirrors official Onshape versions into GitHub, providing a clear history of design milestones and automated management of exported files.

---

## Project Overview

This project automates the synchronization of **official Onshape document versions** to a GitHub repository. It is designed to showcase:

- Versioned tracking of CAD documents.
- Branching and workflow discipline.
- Automated export and commit processes.
- Clear documentation of changes over time.

The repository serves as a single source of truth for exported Onshape assets, with each milestone captured and labeled programmatically.

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

1. The cron job runs every 20 minutes on the EC2 instance.
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
├── scripts/ # Automation scripts (Python)
├── cron.log # Log file for cron job runs
└── README.md
```

---

## Next Steps

- Configure EC2 environment with Python, Git, and required libraries.
- Develop the automation script for fetching and committing new versions.
- Schedule the cron job for periodic syncs.

---

## References

- [Onshape REST API Documentation](https://onshape-public.github.io/docs/)
- [GitHub Documentation](https://docs.github.com/en)
- [GitPython Documentation](https://gitpython.readthedocs.io/en/stable/)
