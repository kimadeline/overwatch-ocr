# Decoding the narrative in competitive Overwatch broadcasts

Code for the PyCon US 2020 presentation `Decoding bias and narrative in competitive video games broadcasts with video analysis`.

✨ Slides: https://aka.ms/pycon2020-overwatch

🗓 PyCon US schedule description: https://us.pycon.org/2020/schedule/presentation/107/

Changing something here for the sake of a PR.

## Installation 🏗

What you will need:

- VS Code + [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Python 3.X
- An Azure subcription with a Computer Vision resource ([documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/python-sdk#create-a-computer-vision-azure-resource))

```sh
> git clone git@github.com:kimadeline/overwatch-ocr.git
> cd overwatch-ocr
> python -m venv .venv
> source .venv/bin/activate
> python -m pip install -r requirements.txt
```

## Manual work to be done (sorry) ✍️

- A list of video files for the games you want to parse, preferably without the breaks between maps. It's easier now that the OWL is on YT Gaming, otherwise [here's](https://www.youtube.com/watch?v=DrPyUcNo1HI) the full USA vs China OWWC match, now go have fun trimming it;
- A JSON reference file mapping player names, team names and shorthand names, look at [`static/owwc_teams.json`](https://github.com/kimadeline/overwatch-ocr/blob/master/static/owwc_teams.json) for an example.

- Create the following folders at the workspace root (siblings of `src`):
  - `input`: Where you'll put your video files
  - `output`: Where the algorithm will split the frames and crop them
  - `data`: Where we will store JSON files containing player names extracted from each frame, and also the reference teams file

## Usage ⚒

### Quickstart with existing OWL results data (PyCon 2020)

To visualize graphs for the OWL matches I used to compute the stats in my PyCon talk:

- Pull the `owl_2020` branch of this repo
- Copy the `owl_results/*_pov.json` files to the `data` folder
- Update the arguments of the `display_dashboard` function in `main.py`
- ✨ `python main.py` ✨

### Other OW broadcasts

- Copy your video files to the `input` folder
- Update the `GAMES_LIST` variable in `src/__init__.py` to be the list of the videos you want to parse (don't include the extension, but if it's not an mp4 file update L.12 of `filename.py`)
- Save your Azure subscription key and endpoint somewhere:
  - Option 1: Add your subscription key and your endpoint to a `.env` file at the root of the repo
  - Option 1: Write them directly in `ocr.py`
- Run everything (this might take a while because I make unoptimized, throttled Azure OCR calls)
  - If you followed option 1 from above, launch the `Python: Main script` configuration (you can't use the run button because of [this issue](https://github.com/microsoft/vscode-python/issues/11174))
  - Otherwise, use the run button in the top-right corner, or call `python main.py` directly
- _⚠️ Make sure your computer doesn't go to sleep_
- Profit 🥳

You should end up with something like this:

![Overwatch World Cup USA vs China finals analysis](https://raw.githubusercontent.com/kimadeline/overwatch-ocr/master/static/readme_screenshot.png)
