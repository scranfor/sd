For Raspberry Pi, requires RPi.GPIO - https://pypi.python.org/pypi/RPi.GPIO

Most examples of step and direction stepper motor control in Python I've seen follow the
naive assumption that the code that twiddles the GPIO pins takes no time to execute,
and that sleep() resumes execution at the perfectly precise value requested. 

This means that the time between step pulses varies slightly, and (almost?) always 
greater than the time passed to sleep(). 

This sd class allows for step pulses to be generated so that the rising edges of each
pulse is more precisely what the user intends. 

Compounding errors are eliminated by slightly varying how long we sleep between each 
step pulse based on whether we are early or late to the "perfect" time. Thus entire 
sequence of steps actually completes very closely to a computable time.

Acceleration/deceleration is not accounted for.
