# Setting up Seqera tower agent and workspace

**Getting started:**

1. Create a Personal Access Token
2. Create shared tower agent credentials
3. Initialise the tower agent
4. Run the custom SIH `auto_tower` agent
5. Add GitHub credentials
6. Set up a compute environment
7. Add a new pipeline to Seqera Platform
8. Run a pipeline

## How to configure your Seqera Personal Access Token for Gadi

**Prerequisites:**
- [ ] An account on Seqera Platforms in the BioCommons workspace
- [ ] Access to Gadi

This needs to be run once to configure your Seqera Platform account to run pipelines on Gadi.

**Steps:**
1. Open `https://seqera.services.biocommons.org.au/` on a browser and sign in with your USYD email.
2. Create an access token by going to the account menu (top right corner) and select **User tokens**.
3. Select **Add token**.
4. Enter a unique name for your token, then select **Add**.
5. Copy the token.
6. Store the access token on Gadi by creating the file `$HOME/.tower/token`
7. Edit the file `$HOME/.tower/token` and paste the access token. Save and exit the file.
8. Update the file permissions by running `chmod 600 $HOME/.tower/token` (`-rw --- ---`).

You have successfully configured your personal access token. Next, see "How to prepare your tower agent on Gadi".

## How to configure shared Tower Agent credentials

**Prerequisites:**
- [ ] An account on Seqera Platforms in the BioCommons workspace
- [ ] Access to a Gadi project 
- [ ] Personal access token configured 

This needs to be done once per Seqera Platform workspace. A shared account requires a designated account on Gadi to run the tower agent. 

Other users cannot start or run the tower agent, but can launch workflows whilst the agent is active.

Ideally a service account sets up the shared credential, that can be shared amongst workspace users. 

The following are steps to create a new shared credential, if required.

**Steps:**
1. Open `https://seqera.services.biocommons.org.au/` on a browser and sign in with your USYD email.
2. Create a new tower agent credentials by selecting **Add workspace credentials**.
3. Provide a unique **Name**.
4. For the **Provider**, select **Tower Agent**.
5. Enable **Shared agent**.

At this point, the tower agent needs to be configured on Gadi. The following steps document this process, and the credentials creation on Seqera Platforms will be finalised once the tower agent is running on Gadi.

6. Before adding the credential you will need to run the agent on Gadi. Check that the agent has been configured for the Gadi project by running the following:

```bash
stat /g/data/<project>/sih-seqera-platform/
```

If a similar output is displayed, **the tower agent may have already been configured by another user in the project**. 

```console
❯ stat /g/data/er01/sih-seqera-platform/
  File: /g/data/er01/sih-seqera-platform/
  Size: 4096            Blocks: 8          IO Block: 4096   directory
Device: 73cc7b8eh/1942780814d   Inode: 162137555779736542  Links: 5
Access: (2755/drwxr-sr-x)  Uid: (22573/  fj9712)   Gid: ( 7470/    er01)
Access: 2026-01-20 15:15:55.000000000 +1100
Modify: 2026-01-20 15:16:01.000000000 +1100
Change: 2026-01-20 15:16:01.000000000 +1100
 Birth: -
```

If so, check if the tower agent is already running.

7. Check the tower agent is running by executing the following command using `flock` and replace the `<project>`.

```bash
flock -n /g/data/<project>/sih-seqera-platform/auto_tower/.tower/.lockfile echo "No tower agent is running."
```

- If that command prints nothing, another agent is running and you'll need to get the owner to stop it or set up your agent in a different directory.
- Alternatively, if the tower agent was previously set up but is not running, **Skip to Step 14**.

8. If the following message is displayed, the directory has not been set up and you should proceed with the remaining set up instructions:

```console
stat: cannot statx '/g/data/er01/sih-seqera-platform': No such file or directory
```

9. To setup the tower agent, retrieve a copy of the `sih-seqera-platform` repository and navigate to the `auto_tower` folder. For example:

```bash
cd /g/data/er01 && \
`git clone git@github.com:Sydney-Informatics-Hub/sih-seqera-platform.git`
```

10. Allow other users in the project to run the agent by updating the file permissions with `chmod 774 -R sih-seqera-platform/`. 
11. Navigate to the `auto_tower` directory by running `cd sih-seqera-platform/auto_tower`.
12. Create the tower directory by running `mkdir -p .tower`
13. Create the file `.tower/connection_id` and open for editing.
14. Retrieve the tower agent **Connection ID** from Seqera Platform by copying the ID in the credentials interface.
15. Return to the terminal (Gadi) and paste the Connection ID in `.tower/connection_id`. Save and exit the file.
16. Run the tower agent and connect to Seqera Platforms by running `./run_tower_agent.sh`. You should see a similar output as:

```
Creating work directory...
Work directory created!
Downloading tw-agent...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0   0     0    0     0    0     0      0      0   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 20 87.1M   20 17.6M    0     0  14.4M      0  66 87.1M   66 57.8M    0     0  26.0M      0 100 87.1M  100 87.1M    0     0  28.0M      0  0:00:03  0:00:03 --:--:-- 36.8M
17:36:38.781 INFO - Established active environments: [cli]
17:36:38.801 INFO - TOWER AGENT v0.5.3
17:36:38.801 INFO - Compatible with TOWER API v1.8
17:36:38.801 INFO - Connecting as user 'fj9712' with default work directory '/g/data/er01/sih-seqera-platform/auto_tower/.tower/work'
17:36:39.095 INFO - Connecting to Tower
17:36:39.200 INFO - Connection to Tower established
```

17. Back in the Seqera interface, click `Add` to save your credential.
18. Optionally, terminate the process running the tower agent.

You have succesfully prepared a Gadi project to run the tower agent and connect to Seqera Platforms!

**References**
- https://docs.seqera.io/platform-enterprise/credentials/agent_credentials
- https://australianbiocommons.github.io/nextflow-seqera/user-guide/compute-env.html#configuring-hpc-on-the-australian-nextflow-seqera-service 

## How to start the automated tower agent `auto_tower` on Gadi

**Prerequisites:**

- [ ] Personal access token configured
- [ ] `sih-seqera-platform` repo available on `/g/data<project>`, or;
- [ ] "How to configure shared Tower Agent credentials" completed

**Steps:**
1. Navigate to the `sih-seqera-platform/auto-tower` repo in your project `/g/data`. For example `cd /g/data/er01/sih-seqera-platform/auto-tower`.
2. Start the tower agent in a persistent session by running `./run_persistent_tower_agent.gadi.sh`. You should see the following message:

```console
Tower agent is running within the screen session 'tower' on the persistent session 'nf-tower.<user>.<project>.ps.gadi.nci.org.au'.
```

3. Optionally, you can add `/g/data/er01/sih-seqera-platform/auto-tower` to your `$PATH` to avoid changing directories.
4. Connect to the persistent session by running `ssh nf-tower.<user>.<project>.ps.gadi.org.au`. Ensure `<user>` and `<project>` are replaced with the correct values.
5. Connect to the screen session with `screen -r`. A similar output should be displayed:

```
15:57:12.720 INFO - Sending heartbeat 
15:57:13.630 INFO - Received heartbeat
15:57:58.151 INFO - Sending heartbeat
15:57:58.406 INFO - Received heartbeat
```

6. To detach from the screen session and keep the tower running, press `ctrl+a` `ctrl+d`.

You have successfully started the automated tower agent on Gadi!

**References:**
- https://devhints.io/screen

## How to configure GitHub credentials

GitHub credentials should be added to the workspace to avoid hitting API limit errors. Only one GitHub credential needs to be added per workspace. 

This sections steps through how to add one.

1. On Seqera Platform, navigate to the workspace **Credentials** tab.
2. Select **Add workspace credentials**.
3. Provide a descriptive name, ideally that informs the workspace and provided. For example `sih-github`.
4. In the **Provider** drop down, **select GitHub**.
5. Enter your GitHub username in **Username**.
6. Create a GitHub personal access token by navigating to [https://github.com/settings/apps](https://github.com/settings/apps).
7. Select the **Personal access tokens** dropdown, select **Fine-grained tokens**.
8. Select **Generate a new token**.
9. In **Token name** denote the workspace group and the platform e.g. `sih-seqera`.
10. Under **Resource owner**, select the GitHub organisation e.g. `Sydney-Informatics-Hub`.
11. Optionally, change the expiration for the token.
12. Optionally, change the repository access.
13. Copy the personal access token.
14. Navigate back to Seqera Platform and paste into **Access token**.
15. Select **Add** to finalise.

You have successfully configured your GitHub credentials!

## How to set up a compute environment

Setting the compute environment is configured on Seqera Platform and only needs to be done once per Seqera workspace, and Gadi project.

Note: Currently, Seqera Platform does not support running Nextflow head jobs locally, or on the head node (e.g. persistent-sessions). The Gadi `copyq` queue will be used in the meantime to submit Nextflow head jobs that can be completed within 10 hours.

1. On https://seqera.services.biocommons.org.au, navigate to the **Compute Environments** tab.
2. Check if a compute environment has been configured yet for the Gadi project. For example, `Gadi-er01`. If it exists, skip the remainder of the sections.
3. To add a new compute environment, select **Add compute environment**.
4. Provide a meaningful which includes the system you are running it on, and the project code e.g. `Gadi-er01`.
5. For the **Platform**, select **Altair PBS Pro** to reflect the scheduler for Gadi.
6. Select the **Credentials** that was either identified, or newly created, in "How to configure shared Tower Agent Credentials". This should be a shared credential so other users in the project can re-use it. e.g. `NCI-shared`.
7. Enter `$TW_AGENT_WORK` for the **Work directory** and **Launch directory**.
8. Leave the **Head queue name** and **Compute queue name** blank.
9. Under **Staging options -> Pre-run script**, enter `module load nextflow/26.04.6 singularity`.
10. Under **Advanced options**, add the following details:
  - **Nextflow queue size**: 300
  - **Head job submit options**: `-P <project> -q copyq -lwalltime=96:00:00,ncpus=1,mem=8G,storage=scratch/<project>+gdata/<project>,wd `. Ensure you update the options to suit the project storage and resources required.
11. Keep the option `Apply head job submit options to compute jobs` off, as this will be handled by `Nextflow config`
12. Select **Add**.

You have successfully set up a compute environment for Gadi!

## How to add a new pipeline

1. On https://seqera.services.biocommons.org.au, navigate to the **Launchpad** tab.
2. Select **Add pipeline**.
3. Enter the **Name** of the pipeline.
4. Select the **Compute environment** for the correct infrastructure and code. e.g. `Gadi-er01`.
5. In **Pipeline to launch**, copy and paste the link to the GitHub repository for the pipeline. For example, `https://github.com/Sydney-Informatics-Hub/Parabricks-Genomics-nf`.
6. If you need to run a version of the pipeline that is not committed to the `main` branch, specify the correct branch or version under the **Revision number** dropdown.
7. Leave the **Work directory** default of `$TW_AGENT_WORK`
8. In **Config profiles**, select the profiles required to run the pipeline. e.g. `gadi`.
9. Select **Add**.

You have successfully added a new pipeline to the Seqera Platform workspace!

## How to run a pipeline

1. Ensure the tower agent is running on Gadi. See "How to start the automated tower agent `auto_tower` on Gadi".
2. On https://seqera.services.biocommons.org.au, navigate to the **Launchpad** tab.
3. For the pipeline to run, select **Launch**.
4. Input all the required options.
