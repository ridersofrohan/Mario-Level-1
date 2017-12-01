# Reinforcement Learning for Super Mario Level 1

---
<div id="installation"></div>Installation
============

Uses (https://github.com/koltafrickenfer/gym-super-mario)

```shell
source env/bin/activate
pip install -r requrements.txt
```

 To load and run the environments, run

```python
import gym
env = gym.make('SuperMarioBros-1-1-v0')
observation = env.reset()
for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)
```
