# Key Implementation Concepts

**1. Parameter Binding**

- **Positional & Keyword Arguments:** Basic user info (`username`, `password`).
- **Keyword-Only Arguments (`*`):** Enforces explicit naming for sensitive data like `pin` to prevent input errors.
- **Variable Keyword Arguments (`**kwargs`):** Allows capturing additional, optional user details without changing the function signature.

```python
def register(username, password, *, pin, **kwargs):
  # ...
  return userid
```

**2. Closure**

- The training_policy function retains the current_divider state even after execution finishes.
- Uses the nonlocal keyword to modify the enclosed variable. As the player trains more, current_divider increases, making it harder to level up

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

Customizes standard Python operators (+, -, >=) to handle game objects intuitively.

- **XP Class (Experience System)**
  - __add__: Allows syntax like current_xp + 100 to increase experience points directly.
  - __ge__: Enables direct comparison (xp >= 1000) to check for level-up eligibility.

- **Loot Class (Inventory System)**
  - __add__: Merges two dictionaries of items. If an item exists, counts are summed; if not, it's added.
  - __sub__: It safely subtracts item counts and raises a ValueError if insufficient items are present.
  - Auto-Cleanup: Automatically deletes keys from the dictionary when the item count reaches 0.

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
