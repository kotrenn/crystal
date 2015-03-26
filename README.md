Timeline:  Summer 2014


A roguelike game project based around a novel spell system.

Half of the project's focus was on practicing development of roguelike games.  I needed a project to do towards the end of summer 2014, and initially began with nothing.  Eventually the project gained momentum and began taking shape.  Unfortunately school responsibilities halted progress.

The main interesting component was the spell system.  Rather than having players collect pre-defined spells such as "Fireball II" or "Ice Storm IV," I put in a system of allowing players to design their own spells.  This was accomplished by giving each spell a "Spell Grid," which is a hex grid that players can configure a layout of crystals.  Random crystals can be collected throughout the game which provide a variety of effects.  Additionally, each crystal had a set of "pipes" for the flow of an unnamed magical source.  The spell grid then turned into a game of arranging crystals so they form various valid flows, similar in a way to Pipe Dream derived games.

Outside of the spell grid, there was an effort to make a crafting system.  The big goal was to develop a simple language for describing various types of recipes, including their inputs, outputs, and how the outputs are formed.  Basically a simple scripting language.  Examples of this can be found in crystal/recipes.txt while the bulk of the code is found under crystal/recipe.

Finally, there were some experiments with procedural generation of a world.  I began by creating a random set of points that were "uniformly" distributed, but pushed from pure uniform to produce a more even spread for aesthetic and playability.  The process used was Bridson's algorithm for Poisson-disc sampling.  A great explanation of this algorithm can be found at http://bost.ocks.org/mike/algorithms/.  Next, the random points were connected into a graph by building up the Relative Neighborhood Network (http://www.passagesoftware.net/webhelp/Introduction.htm#Relative_Neighborhood_Network.htm).  This was chosen for the amount of connections between nodes being at a healthy level of control for gameplay, while also providing enough variety in alternate paths.

Later plans included limiting the regions of points being generated so as to form continents.  Additionally, a world with multiple fantasy races reached early concept stages, but currently only exist in personal notes.

There is a roguelike movement engine for moving between the different regions.  The initial development was first to just generate rectangular regions with trees lining the edges.  Gaps exist to match up with adjacent regions, and were placed to make the pathways realistic in a sense.  This also provided players with a sense of direction.

The engine additionally supports basic combat, including a functioning version of the spell system in action.  A simple A* module was provided for monsters and potential advanced features later on.  Additionally, an energy based system for scheduling is implemented, based on Robert Nystrom's article on the subject:  http://journal.stuffwithstuff.com/2014/07/15/a-turn-based-game-loop/.

The code base is *not* well documented.  The primary purpose of the project was to get the developer (kotrenn) out of a creative slump at the time.  As such, the focus was more on getting something out rather than on legibility for others.  Yet it was also a project to learn about Git and GitHub.  Efforts were made to commit small, incremental changes with notes to get practice organizing my coding.
