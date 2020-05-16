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
    # for video
    ffmpeg -i $INPUT -vcodec copy -acodec copy -ss HH:MM:SS.SSSS $OUTPUT

    # for audio only
    ffmpeg -i $INPUT -acodec copy -ss HH:MM:SS.SSSS $OUTPUT
    ```
1. Set the __record (or transcode) "duration"__ seconds of audio/video using the `-t duration` option.
    ```sh
    ffmpeg -i $INPUT -vcodec copy -acodec copy -t HH:MM:SS.SSSS $OUTPUT
    ```
1. Combine __start time__ and __duration__ options to get the desired middle section.
    ```sh
    ffmpeg -i $INPUT -vcodec copy -acodec copy -ss HH:MM:SS.SSSS -t HH:MM:SS.SSSS $OUTPUT
    ```
    Recall: `duration = end_time - start_time`.

When trimming audio, the `-vcodec copy` option should be omitted.
```sh
# for video
ffmpeg -i $INPUT -vcodec copy -acodec copy [OPTIONS] $OUTPUT

# for audio only
ffmpeg -i $INPUT -acodec copy [OPTIONS] $OUTPUT
```

In the examples above, `copy` avoids the quality degradation that comes with re-encoding. However, trimming encoded video may leave some visual garbage at the beginning before you hit the next keyframe.


<!--
## Next Steps [OR] Related

* INTRODUCE [CONTENT](../PATH_TO/FILE.md)
-->

[Homepage](../README.md)
