# Reinforcement Learning for Super Mario Level 1

---
<div id="installation"></div>Installation
============

Uses (https://github.com/koltafrickenfer/gym-super-mario)

```shell
brew install fceux

virtualenv env
source env/bin/activate

pip install -r requrements.txt

cp -r mario_env/envs/kolta_gym_super_mario env/lib/python3.6/site-packages/gym/envs/
cp -r mario_env/envs/__init__.py env/lib/python3.6/site-packages/gym/envs/__init__.py
cp -r mario_env/scoreboard/__init__.py env/lib/python3.6/site-packages/gym/scoreboard/__init__.py
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
