# ffmpeg

## Recipes
Below are a few commonly-used recipes.  I find it hard to memorize these options, so listing them here helps.

### Automatic Detection
Automatically detect input and output type based on provided extensions and file data.
```sh
ffmpeg -i A_Movie.mp4 audio_only.mp3
```

### Trim Start and End
1. Set the __start time offset__ using the `-ss time_off` option.
    ```sh
    ffmpeg -i $INPUT -codec copy -ss HH:MM:SS.SSSS $OUTPUT
    ```
1. Set the __record (or transcode) "duration"__ seconds of audio/video using the `-t duration` option.
    ```sh
    ffmpeg -i $INPUT -codec copy -t HH:MM:SS.SSSS $OUTPUT
    ```
1. Combine __start time__ and __duration__ options to get the desired middle section.
    ```sh
    ffmpeg -i $INPUT -codec copy -ss HH:MM:SS.SSSS -t HH:MM:SS.SSSS $OUTPUT
    ```
    Recall: `duration = end_time - start_time`.

In the examples above, `copy` avoids the quality degradation that comes with re-encoding. However, trimming encoded video may leave some visual garbage at the beginning before you hit the next keyframe.

### Delay Video or Audio
Set the `-itsoffset delay` option to delay an input stream.
You can specify the same input file twice, one with a time delay. Then pick the corresponding streams to get the delay on the stream you want.

Below, we delay the second input stream (1:x).

#### Delay Audio
The `-map X:X` options select video from the first/un-delayed file (0:v) and audio from the second/delayed file (1:a).
```sh
ffmpeg -i $INPUT -itsoffset $AUDIO_DELAY -i $INPUT -map 0:v -map 1:a -codec copy $OUTPUT
```

#### Delay Video
The `-map X:X` options select video from the second/delayed file (1:v) and audio from the first/un-delayed file (0:a).
```sh
ffmpeg -i $INPUT -itsoffset $VIDEO_DELAY -i $INPUT -map 1:v -map 0:a -codec copy $OUTPUT
```

Source: [superuser answer](https://superuser.com/a/983153/1131203)


<!--
## Next Steps [OR] Related

* INTRODUCE [CONTENT](../PATH_TO/FILE.md)
-->

[Homepage](../README.md)
