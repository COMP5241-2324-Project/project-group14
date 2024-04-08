[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=13745467)
# Project repository
This project utilizes the GitHub API to monitor the development progress of selected repositories, including members, task completion status, code modifications, etc. Additionally, AI is used to assist in analyzing the contributions of individual developers. The files with an index of zero or one constitute the core of the project, which is based on Redis. The files with an index of two are the development files that utilize Webhooks during the development process.

### First start the redis
`docker start project-redis`

### Second start the project
`python app.py`