# NDALE
Non-Deterministic Animation Looping Engine


Loosely inspired by In Flight Simulator: https://inflightsimulator.com/ , Next Train: https://ride.nexttrain.london/, and those 14-hour scenic videos my dentist plays on the waiting room TV, NDALE is a software for making animations that loop forever, taking a different route every time. You must bring your own .gifs, but some are provided in `demos` folder so you can see how it works. 

This is a PRE-PRE-ALPHA Software. It certainly works for a small number of 64x64 gifs. With larger amounts of files, more frames, or higher resolution it will probably be slow/buggy. 

## How to use

Run `editor.py` . Click the load button and pick a folder (e.g `demos/demo`). You'll be taken to the editor pane. From here you can match gifs using the two lists. You pick a gif in the left list (e.g `start`) and and/all that come after it in the right list (e.g 'L' and 'R').  You **MUST** ensure that you create a cycle (e.g at some point you must pick a gif on the left and link it back to `start`). Click the "save matching" button to save each pair in the RAM. "Save to disk" saves every pair in RAM to a JSON file. Load from disk lets you pick a JSON file to load. 

After this, click "view animation" and then click "play". The video *should* play. If it doesn't, check your python console. A `KeyError` means your matchings aren't valid (e.g there's a dead end somewhere). If you need to start fresh, close and reopen the application. The export button doesn't currently do anything. 

## Roadmap (not in order)

* Dynamic size scaling
* Exporting video
* Ability to delete matches
* Undo button
* Loading files in a background thread so they don't slow down the program
* UI Improvements

