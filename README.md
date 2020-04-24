# Decoding the narrative in competitive Overwatch broadcasts

Code for the PyCon US 2020 presentation `Decoding bias and narrative in competitive video games broadcasts with video analysis`. 

✨ Slides: https://aka.ms/pycon2020-overwatch

🗓 PyCon US schedule description: https://us.pycon.org/2020/schedule/presentation/107/ 

## Installation 🏗

What you'll need:

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

- Copy your video files to the `input` folder
- Update the `GAMES_LIST` variable in `src/__init__.py` to be the list of the videos you want to parse (don't include the extension)
- `python main.py` (this might take a while because I make unoptimized, throttled Azure OCR calls)
- _⚠️ Make sure your computer doesn't go to sleep_
- Profit 🥳

You should end up with something like this:

![Overwatch World Cup USA vs China finals analysis](https://raw.githubusercontent.com/kimadeline/overwatch-ocr/master/static/readme_screenshot.png)
