# TypeRacerWinner
A simple project that wins at TypeRacer. I wanted to see how far it would let me go before it deemed a cheater. Also, it's cool to see how easy it is to beat the "captcha" with Google's Vision API.

## Features
1. A way to fake typing errors to decrease accuracy and make it appear more human like
2. Supports Chrome and Firefox

## Limitations
1. Only supports Chrome and Firefox
2. Need to place the chromedriver.exe or the geckodriver.exe into the your computers PATH or working directory for this to execute properly.
3. Will need a Google Vision API key. Can be gotten for free from cloud.google.com

## Installation
```pip install requirements.txt
```

## Usage
```racer = Racer()
racer.open_browser(browser="Firefox")
racer.login_typeracer("username", "password")
racer.do_race(secs_between_keystrokes=.02, room_for_error=0)
racer.complete_captcha_challenge(api_key="Google_Vision_API_Key")
```

## License
[MIT](https://choosealicense.com/licenses/mit/)