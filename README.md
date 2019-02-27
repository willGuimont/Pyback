# Pyback
Record and replay action. Record a sequence of inputs (mouse &amp; keyboard) then replay it. Python librairy

# Example

```python
import time
from composer import Composer
from actor import Actor


if __name__ == '__main__':
    # File where actions will be stored
    actions = "actions.act"
    # Composer that will record inputs for 5 seconds
    cp = Composer(actions, time=5)
    print("**Composing**")
    # Start composing
    cp.record()
    while cp.is_running():
        cp.update()
        time.sleep(0.1)
        # Do other stuff here...

    # Actor that will play the act
    ac = Actor(actions)
    print("\n**Acting**")
    # Start acting
    ac.act()
```
