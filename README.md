# RazerChromaVideo
Play videos on your razer setup (linux only)

I was bored
# Requirements
[ffmpeg](https://ffmpeg.org)<br/>
[pygame](https://pygame.org)<br/>
[openrazer](https://openrazer.github.io)
# Usage
Put a video you want to play in the scripts location and name it `vid.mp4` then run the script using `python3 main.py` it works with every razer chroma device that has rgb (this script works only on linux). When the script is running you can see a message `I can't keep up with drawing!` it's an information that drawing one frame takes longer than expected if you get that message too many times and you notice lag you should unplug some devices or change video resolution to a smaller one.
# How does this black magic work???
It's way simpler than you think, first the script extracts frames & audio from a video using ffmpeg and then it gets all of the devices using openrazer and scales the frames so that they fit onto the device. Audio is handled by pygame.