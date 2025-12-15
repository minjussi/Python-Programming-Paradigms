# Parameter Binding, Closure, User-defined Overloaded Operators

**1. Parameter Binding**

- Positional, Key-word only

```python
def register(username, password, *, pin, **kwargs):
  # ...
  return userid
```

**2. Closure**

```python
def training_policy(divider):
    current_divider = divider
    def train(minutes):
        nonlocal current_divider
        level = int(minutes / current_divider)
        current_divider += 1
        return level
    return train

TRAINING_POLICIES = {
    "hunting": training_policy(10),
    "herbology": training_policy(10),
    "cooking": training_policy(10),
    "swimming": training_policy(10),
    "fishing": training_policy(10)
}
```

**3. User-defined Overloaded Operators**

```python
class XP:
    def __init__(self, xp = 0):
        self.value = int(xp)
    def __add__(self, amount):
        return XP(self.value + amount)
    def __ge__(self, amount):
        return self.value >= amount

class Loot:
    def __init__(self, items):
        self.items = items
    def __add__(self, loots):
        items_copy = self.items.copy() # current inventory items
        for loot, count in loots.items.items():
            items_copy[loot] = items_copy.get(loot, 0) + count
        return Loot(items_copy)
    def __sub__(self, loots):
        items_copy = self.items.copy() # current inventory items
        for loot, count in loots.items.items():
            if items_copy.get(loot, 0) < count:
                raise ValueError(f"There is no items; Necessary items:{loots.items}")
            items_copy[loot] -= count
            if items_copy[loot] == 0:
                del items_copy[loot]
        return Loot(items_copy)
```
