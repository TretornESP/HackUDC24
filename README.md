# HackUDC24 - Codeegenerates :)
## Modifications before execution
For execution you need three files created:
 - `certs` folder with certificates for nginx
 - `secret.env` for holding keys

You must change the `docker-compose.yml` and the `master/master.cfg` configuration files because of weird edge cases which are very time-consuming to solve inside the latter file.
### docker-compose.yml
You must manually get and set the `GITHUB_SECRET` token. To change the repo that it demoes against, you must change `TARGET_REPO`and `TARGET_BRANCH` lines. Finally, the `REPORT_URL` should indicate where the report would be generated. While the full implementation of this last feature has not been completed due to prioritized tasks, it does not impact the effectiveness of this demo.
### master/master.cfg
In line 93 as of the current commit, you must paste the URL that the reports will be saved to.

## Deployment
You will need Docker. It is as easy as executing 
```bash
docker compose up --build
```
Everything should be working now if you have followed the steps precisely!

## Execution
When pushing to the tracked branch on the tracked repository, an automated CI build will start. When finished, click on the checkmark next to the github commit. The CI title is the link to the full report.

## License
MIT License. Read LICENSE for more information.
