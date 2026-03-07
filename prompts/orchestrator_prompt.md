# Orchestrator Prompt

I need you to implement this feature. Now, this is really important. I don't want you to write any code yourself. Your role is to coordinate the efforts between unix-coder and code-reviewer Agents.
Have a look at this implementation plan, and I want you to create different tracks. Have a look at any phases or tasks that can be implemented in parallel. Find any phases or tasks that do not have a dependency on each other, and then create different tracks.
Then for each track, kick off a unix-coder to implement the changes for that track. You need to use the unix-coder for this. Once the coding agent completes its work, you need to hand over the solution to the code-review agent and then let the code-review agent provide feedback back to the unix-coder.
The cycle should continue until all changes have been fully implemented.
Again, I do not want you to implement anything yourself. You need to keep your context window as lean as possible. Coordinate all the different efforts between the tracks, the unix-coder, and code-review agents.

be sure to create a separate worktree per feature that is being worked on to avoid merge conflicts, and ensure that any and all merge conflicts are managed so no work is lost.

# Orchestrator Prompt

I need you to implement this feature. Now, this is really important. I don't want you to write any code yourself. Your role is to coordinate the efforts between unix-coder and code-reviewer Agents.
Have a look at this implementation plan, and I want you to create different tracks. Have a look at any phases or tasks that can be implemented in parallel. Find any phases or tasks that do not have a dependency on each other, and then create different tracks.
Then for each track, kick off a unix-coder to implement the changes for that track. You need to use the unix-coder for this. Once the coding agent completes its work, you need to hand over the solution to the code-review agent and then let the code-review agent provide feedback back to the unix-coder.
The cycle should continue until all changes have been fully implemented.
Again, I do not want you to implement anything yourself. You need to keep your context window as lean as possible. Coordinate all the different efforts between the tracks, the unix-coder, and code-review agents.
Be sure to create a separate worktree per feature that is being worked on to avoid merge conflicts, and ensure that any and all merge conflicts are managed so no work is lost.

# Implementation Plan

1. Use /plugin-genrator:generate plugin to make a plugin for claude-code that will breakout sub-agents (local agents) into separate zellij panes. This will allow us to have multiple agents working in parallel, _transparently_ without interfering with each other, allowing the user to interact in realtime with each agent in their own pane. there should be the option to split out local-agents by the user, as it could be possible to spawn so many local-agents that splitting them all into separate panes could compromise the performance of the machine. However, also create logic that if there are less than 4 local agents, they should be automatically split into separate panes, and if there are more than 4 local agents, only the first 4 should be split into separate panes, and the rest should be grouped together in a single pane. This will allow us to have a good balance between performance and usability. The user should also have the option to manually move local agents between panes as needed.

2. Create a new sub-agent called "track-manager" that will be responsible for managing the different tracks of work. This agent will keep track of which tracks are active, which agents are working on which tracks, and the status of each track.

3. Create a new sub-agent called "dependency-manager" that will be responsible for managing the dependencies between the different tracks. This agent will ensure that any tracks that have dependencies on other tracks are not started until their dependencies are completed.

4. Create a new sub-agent called "merge-manager" that will be responsible for managing merge conflicts between the different tracks. This agent will ensure that any merge conflicts are resolved in a timely manner and that no work is lost.
