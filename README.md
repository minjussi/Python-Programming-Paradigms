# Python-Programming-Paradigms

2025 Fall SKKU - Programming Language class

This repository contains assignment codes implemented in Python based on the concepts learned in the Programming Language lecture.

## 1. Adventurer's Guild System Game
> **Key Concepts:** Parameter Binding, Closure, User-defined Overloaded Operators

This project implements a text-based RPG game system to demonstrate advanced function handling and operator customization in Python.
* **Parameter Binding & Closure:** utilized to maintain the state of character stats and inventory securely within function scopes, preventing unwanted global access.
* **Operator Overloading:** Custom behaviors for operators (e.g., `+`, `-`) are defined to handle interactions intuitively, such as equipping items or battling monsters directly through syntax like `hero + sword`.

## 2. Parse Tree & Expression Evaluator
> **Key Concepts:** Recursion, Tree Data Structure, Parsing

This assignment focuses on implementing a Parse Tree to evaluate mathematical expressions recursively.
* **Recursive Parsing:** The program breaks down a mathematical expression string into tokens and constructs a tree structure where leaves are operands (numbers) and internal nodes are operators.
* **Evaluation Process:** It traverses the constructed tree from the bottom up. Each node recursively evaluates its children—calculating the left and right sub-trees—and applies its operator to return the final result.
* *(Note: Currently debugging an issue with edge cases in the recursion depth.)*

## 3. Printing Receipt System
> **Key Concepts:** OOP (Object-Oriented Programming), Encapsulation, Polymorphism

A receipt generation system designed to practice the core principles of the Object-Oriented Paradigm.
* **Encapsulation:** Sensitive data (like pricing logic or tax rates) is protected using private attributes (e.g., `__variable`), accessible only through specific methods.
* **Polymorphism & Constructor:** The system uses `self` and `__init__` to instantiate different types of products. Polymorphism ensures that different items (e.g., tax-free vs. taxable goods) calculate their final prices differently while sharing a common interface for printing.

## 4. LISP Interpreter in Python
> **Key Concepts:** Functional Programming, List Processing, Recursion

This project involves implementing a subset of the LISP language syntax and semantics using Python.
* **Functional Paradigm:** Instead of loops, this implementation relies heavily on recursion and pure functions to process lists, mimicking LISP's core philosophy.
* **List Operations:** Implements fundamental LISP primitives such as `CAR`, `CDR`, `CONS`, and handles nested list structures to demonstrate how functional languages manage memory and data.
