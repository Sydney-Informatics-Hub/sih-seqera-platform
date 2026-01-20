# Setting up Seqera tower agent and workspace

## How to configure your Seqera Personal Access Token for Gadi

**Requirements:**

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

## How to prepare your tower agent on Gadi

**Requirements:**

- [ ] Access to a Gadi project 

The tower agent needs to be setup once per project. First, check that the agent exists in your project by running:

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

You have succesfully prepared a Gadi project to run the tower agent. Next, see "How to start the tower agent"

## How to start the automated tower agent `auto_tower` on Gadi

**Requirements:**

- [ ] Personal access token configured
- [ ] `sih-seqera-platform` repo available on `/g/data<project>`, or;
- [ ] "How to prepare your tower agent on Gadi" completed

**Steps:**

1. Navigate to the `sih-seqera-platform/auto-tower` repo in your project `/g/data`. For example `cd /g/data/er01/sih-seqera-platform/auto-tower`.
2. Run the tower agent 
2. Run the tower agent by running `./run_persistent_tower_agent.gadi.sh`. This will generate `.tower/` and `.tower/work/` directories and display the following message:

```console
Tower agent is running within the screen session 'tower' on the persistent session 'nf-tower.<user>.<project>.ps.gadi.nci.org.au'.
```


- On Seqera, set up tower agent credentials → Credentials tab → Add workspace credentials → Set name → Select "Tower Agent" in the "Provider" drop-down box → Copy the "Agent connection ID" to clipboard → set as a "Shared agent" → Add
- Create the file `.tower/connection_id` on Gadi and edit it with the agent connection ID copied from Seqera.
- Run `./run_persistent_tower_agent.gadi.sh` (can be run from any directory – add it to your PATH for extra points)