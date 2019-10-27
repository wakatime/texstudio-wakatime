texstudio-wakatime
==================

Metrics, insights, and time tracking automatically generated from your TeXstudio usage.


Installation
------------

1. Install the [wakatime](https://github.com/wakatime/wakatime#installation) python command line tool.

2. Create a `~/.wakatime.cfg` file with contents:

        [settings]
        api_key = XXXX
    
  Replace `XXXX` with your actual [api key](https://wakatime.com/settings#apikey).

3. Run `install.py`

  ```Be sure to have python 2.7 installed```

  **Mac and Linux**

  `curl -fsSL https://raw.githubusercontent.com/wakatime/texstudio-wakatime/master/install.py | python`

  **Windows**

  Download and extract [texstudio-wakatime-master.zip](https://github.com/wakatime/texstudio-wakatime/archive/master.zip), then double click `install.py`.

4. Use TeXstudio like you normally do and your time will be tracked for you automatically.

5. Visit https://wakatime.com/dashboard to see your logged time.


Screen Shots
------------

![Project Overview](https://wakatime.com/static/img/ScreenShots/Screen-Shot-2016-03-21.png)


Troubleshooting
---------------

Do you have [Python](https://www.python.org/downloads/) installed?

Do you have [wakatime](https://github.com/wakatime/wakatime#installation) installed and available in your PATH?

For more general troubleshooting information, see [wakatime/wakatime#troubleshooting](https://github.com/wakatime/wakatime#troubleshooting).
