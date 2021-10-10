# I-am-a-robot
A simple python library that solves "I'm not a robot" captcha using selenium

It is a work in progress but it works.

I plan on including other types of captcha in the future too so stay tuned.

## How does it work?

For a demo on how it works refer to `try.py`

1. Import `iamarobot.py`
2. Declare a `Docaptcha` object with the driver of the browser where the captcha is as the first argument and the xpath of lowest-level iframe of the captcha as the second argument
3. Call the method `solve` on the object.
4. Enjoy whatever you are using it for