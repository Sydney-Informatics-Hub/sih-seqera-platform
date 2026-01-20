# Setting up Seqera tower agent and workspace

**Getting started:**

1. Create a Personal Access Token
2. Create shared tower agent credentials
3. Initialise the tower agent
4. Run the custom SIH `auto_tower` agent

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

This needs to be done once per Seqera Platform workspace.

**Steps:**
1. Open `https://seqera.services.biocommons.org.au/` on a browser and sign in with your USYD email.
2. Go to the **Credentials** tab and check for shared credentials (e.g. **`NCI-shared`**). If it exists, skip the rest of this section.
4. If it does not exist, create new tower agent credentials by selecting **Add workspace credentials**.
5. Provide a unique **Name**.
6. For the **Provider**, select **Tower Agent**.
7. Enable **Shared agent**.
7. Select **Add**.

**References**
- https://docs.seqera.io/platform-enterprise/credentials/agent_credentials
- https://australianbiocommons.github.io/nextflow-seqera/user-guide/compute-env.html#configuring-hpc-on-the-australian-nextflow-seqera-service 

## How to prepare the automated tower agent on Gadi

**Prerequisites:**
- [ ] Access to a Gadi project 
- [ ] Personal access token configured 
- [ ] Seqera Tower Agent credentials configured 

The tower agent needs to be setup once per Gadi project. First, check that the agent exists in your project by running:

```bash
stat /g/data/<project>/sih-seqera-platform/
```

If a similar output is displayed, **the tower agent has already been configured for this project - skip the remainder of this section**:
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

If a similar output is displayed, **the tower agent has not been configured and the remainder of the steps in this section must be run**:

```console
stat: cannot statx '/g/data/er01/blah': No such file or directory
```

**Steps:**
1. To setup the tower agent, retrieve a copy of the `sih-seqera-platform` repository and navigate to the `auto_tower` folder. For example:

```bash
cd /g/data/er01 && \
`git clone git@github.com:Sydney-Informatics-Hub/sih-seqera-platform.git`
```

2. Allow other users in the project to run the agent by updating the file permissions with `chmod 774 -R sih-seqera-platform/`. 
3. Navigate to the `auto_tower` directory by running `cd sih-seqera-platform/auto_tower`.
4. Create the tower directory by running `mkdir -p .tower`
5. Create the file `.tower/connection_id` and open for editing.
6. Retrieve the tower agent Connection ID from Seqera Platform by navigating to **Credentials -> Workspace credentials**. Locate the correct shared workspace credentials (e.g. `NCI-shared-2`) and copy the **Connection ID** to your clipboard.
7. Return to the terminal (Gadi) and paste the Connection ID in `.tower/connection_id`. Save and exit the file.
8. Run the tower agent and connect to Seqera Platforms by running `./run_tower_agent.sh`. You should see a similar output as:

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

9. Terminate the process.

You have succesfully prepared a Gadi project to run the tower agent and connect to Seqera Platforms!

## How to start the automated tower agent `auto_tower` on Gadi

**Prerequisites:**

- [ ] Personal access token configured
- [ ] `sih-seqera-platform` repo available on `/g/data<project>`, or;
- [ ] "How to prepare your tower agent on Gadi" completed

**Steps:**
1. Navigate to the `sih-seqera-platform/auto-tower` repo in your project `/g/data`. For example `cd /g/data/er01/sih-seqera-platform/auto-tower`.
2. Start the tower agent in a persistent session by running `run_persistent_tower_agent.gadi.sh`. You should see the following message:

```console
Tower agent is running within the screen session 'tower' on the persistent session 'nf-tower.<user>.<project>.ps.gadi.nci.org.au'.
```

TODO:
- connect to persistent-session, open screen

## How to add a new pipeline

TODO

## How to run a pipeline

TODO