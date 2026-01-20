# Setting up Seqera tower agent and workspace

- Setting up Seqera tower agent and Seqera workspace
- On Seqera platform, set up your personal access token
→ Account menu (top right corner) → User tokens → Add Token → Unique name → Add → Copy token to clipboard → Close
- On Gadi, create the file `$HOME/.tower/token` and give it 600 permissions (`~ ---- ---`)
- Edit `$HOME/.tower/token` and place your access token in the file then save
- On Gadi, navigate to location where tower agent should run, e.g. `/scratch/er01/`
- Clone `sih-seqera-platform repo`: `git clone git@github.com:Sydney-Informatics-Hub/sih-seqera-platform.git`
- Navigate to `auto_tower/` folder
- Run `./run_tower_agent.sh`. This will fail, but will generate the `.tower/` and `.tower/work/` directories.
- On Seqera, set up tower agent credentials → Credentials tab → Add workspace credentials → Set name → Select "Tower Agent" in the "Provider" drop-down box → Copy the "Agent connection ID" to clipboard → set as a "Shared agent" → Add
- Create the file `.tower/connection_id` on Gadi and edit it with the agent connection ID copied from Seqera.
- Run `./run_persistent_tower_agent.gadi.sh` (can be run from any directory – add it to your PATH for extra points)