from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'tech_x_espadas_elwa_secret_key_2024'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# AI API Configuration
# Set your Anthropic API key as environment variable: export ANTHROPIC_API_KEY=your_key
# Or set it here (not recommended for production)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')  # Add your API key here
USE_AI_API = bool(ANTHROPIC_API_KEY)  # Enable AI if API key is set

# In-memory database (replace with actual database in production)
users_db = {}
learning_progress = {}
quiz_attempts = {}
leaderboard_data = {}

# Python learning content structure
LEARNING_CONTENT = {
    "basics": {
        "title": "Python Basics",
        "topics": [
            {
                "id": "intro",
                "name": "Introduction to Python",
                "duration": "30 min",
                "video": "https://www.youtube.com/embed/kqtD5dpn9C8",
                "description": "Learn what Python is, why it's popular, and write your first program.",
                "content": "Python is a high-level, interpreted language created by Guido van Rossum in 1991. Known for clean syntax and readability.",
                "code": """# Hello World
print("Hello, World!")

# Variables
name = "Python"
year = 1991
print(f"{name} was created in {year}")

# Comments
# This is a single-line comment
\"\"\"
This is a
multi-line comment
\"\"\""""
            },
            {
                "id": "variables",
                "name": "Variables and Data Types",
                "duration": "45 min",
                "video": "https://www.youtube.com/embed/Z1Yd7upQsXY",
                "description": "Master variables, data types (int, float, str, bool), and type conversion.",
                "content": "Variables store data. Python has dynamic typing - no need to declare types.",
                "code": """# Variables
name = "Alice"
age = 25
height = 5.9
is_student = True

# Type checking
print(type(age))  # <class 'int'>

# Type conversion
num_str = "100"
num = int(num_str)
print(num + 50)  # 150

# F-strings
print(f"{name} is {age} years old")"""
            },
            {
                "id": "operators",
                "name": "Operators",
                "duration": "40 min",
                "video": "https://www.youtube.com/embed/v5MR5JnKcZI",
                "description": "Arithmetic (+, -, *, /), comparison (==, !=, <, >), and logical operators (and, or, not).",
                "content": "Operators perform operations on variables and values.",
                "code": """# Arithmetic
x = 10
y = 3
print(x + y)   # 13
print(x / y)   # 3.333
print(x // y)  # 3 (floor division)
print(x ** y)  # 1000 (power)

# Comparison
print(x == y)  # False
print(x > y)   # True

# Logical
age = 25
has_license = True
can_drive = age >= 18 and has_license
print(can_drive)  # True"""
            },
            {
                "id": "input_output",
                "name": "Input/Output",
                "duration": "35 min",
                "video": "https://www.youtube.com/embed/Iq3YwdBN0P8",
                "description": "Get user input with input() and display output with print().",
                "content": "Interact with users through input and output functions.",
                "code": """# Output
print("Hello!")
print("Name:", "Alice", "Age:", 25)

# Input
name = input("Enter your name: ")
print(f"Hello, {name}!")

# Convert input
age = int(input("Enter age: "))
next_age = age + 1
print(f"Next year you'll be {next_age}")"""
            }
        ]
    },
    "control_flow": {
        "title": "Control Flow",
        "topics": [
            {
                "id": "conditionals",
                "name": "If-Else Statements",
                "duration": "40 min",
                "video": "https://www.youtube.com/embed/DZwmZ8Usvnk",
                "description": "Make decisions with if, elif, and else statements.",
                "content": "Control program flow based on conditions.",
                "code": """# If-else
age = 18
if age >= 18:
    print("Adult")
else:
    print("Minor")

# If-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print(f"Grade: {grade}")

# Multiple conditions
age = 25
has_license = True
if age >= 18 and has_license:
    print("Can drive")"""
            },
            {
                "id": "loops",
                "name": "For and While Loops",
                "duration": "50 min",
                "video": "https://www.youtube.com/embed/6TEGxJaLoDo",
                "description": "Repeat code with for and while loops. Learn iteration techniques.",
                "content": "Loops execute code repeatedly until a condition is met.",
                "code": """# For loop
for i in range(5):
    print(i)  # 0 to 4

# Loop through list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")"""
            },
            {
                "id": "break_continue",
                "name": "Break and Continue",
                "duration": "30 min",
                "video": "https://www.youtube.com/embed/yCZBnjF4_tU",
                "description": "Control loop execution with break (exit) and continue (skip).",
                "content": "Break exits loop early, continue skips current iteration.",
                "code": """# Break - exit loop
for i in range(10):
    if i == 5:
        break
    print(i)  # 0 to 4

# Continue - skip iteration
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0,1,3,4 (skips 2)

# Practical: find number
for num in range(1, 20):
    if num % 7 == 0:
        print(f"Found: {num}")
        break"""
            }
        ]
    },
    "data_structures": {
        "title": "Data Structures",
        "topics": [
            {
                "id": "lists",
                "name": "Lists",
                "duration": "50 min",
                "video": "https://www.youtube.com/embed/ohCDWZgNIU0",
                "description": "Ordered, mutable collections. Learn list methods and operations.",
                "content": "Lists store multiple items in order. Can be modified after creation.",
                "code": """# Create list
fruits = ["apple", "banana", "cherry"]

# Access
print(fruits[0])  # apple
print(fruits[-1]) # cherry (last)

# Modify
fruits[0] = "orange"
fruits.append("mango")

# Methods
fruits.sort()
fruits.reverse()
print(len(fruits))

# Slicing
print(fruits[1:3])

# List comprehension
squares = [x**2 for x in range(5)]
print(squares)  # [0,1,4,9,16]"""
            },
            {
                "id": "tuples",
                "name": "Tuples",
                "duration": "35 min",
                "video": "https://www.youtube.com/embed/NI26dqhs2Rk",
                "description": "Immutable ordered collections. Cannot be changed after creation.",
                "content": "Tuples are like lists but immutable - faster and safer.",
                "code": """# Create tuple
point = (10, 20)
colors = ("red", "green", "blue")

# Access
print(point[0])  # 10

# Cannot modify!
# point[0] = 15  # ERROR!

# Unpacking
x, y = point
print(f"x={x}, y={y}")

# Multiple returns
def get_user():
    return "Alice", 25
name, age = get_user()"""
            },
            {
                "id": "dictionaries",
                "name": "Dictionaries",
                "duration": "45 min",
                "video": "https://www.youtube.com/embed/XCcpzWs-CI4",
                "description": "Key-value pairs for fast lookups. Like real dictionaries.",
                "content": "Dictionaries map keys to values for efficient data retrieval.",
                "code": """# Create dict
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A"
}

# Access
print(student["name"])
print(student.get("age"))

# Modify
student["age"] = 21
student["email"] = "alice@email.com"

# Iterate
for key, value in student.items():
    print(f"{key}: {value}")

# Dict comprehension
squares = {x: x**2 for x in range(5)}"""
            },
            {
                "id": "sets",
                "name": "Sets",
                "duration": "40 min",
                "video": "https://www.youtube.com/embed/sBvaPopWOmQ",
                "description": "Unordered collections of unique elements. No duplicates allowed.",
                "content": "Sets automatically remove duplicates and support mathematical operations.",
                "code": """# Create set
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}

# Add
fruits.add("orange")

# Remove duplicates
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)  # {1, 2, 3}

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)  # Union
print(a & b)  # Intersection
print(a - b)  # Difference"""
            },
            {
                "id": "arrays",
                "name": "Arrays (NumPy)",
                "duration": "45 min",
                "video": "https://www.youtube.com/embed/QUT1VHiLmmI",
                "description": "Numerical arrays with NumPy. Essential for data science and ML.",
                "content": "NumPy arrays are faster and more efficient than lists for numerical data.",
                "code": """# Install: pip install numpy
import numpy as np

# Create array
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1,2], [3,4]])

# Operations (vectorized)
print(arr * 2)    # [2,4,6,8,10]
print(arr + 10)   # [11,12,13,14,15]

# Math functions
print(np.sqrt(arr))
print(arr.mean())
print(arr.sum())

# Create arrays
zeros = np.zeros(5)
ones = np.ones((3,3))
range_arr = np.arange(0, 10, 2)"""
            }
        ]
    },
    "functions": {
        "title": "Functions",
        "topics": [
            {
                "id": "defining_functions",
                "name": "Defining Functions",
                "duration": "45 min",
                "video": "https://www.youtube.com/embed/NE97ylAnrz4",
                "description": "Create reusable code blocks. Learn def, return, and parameters.",
                "content": "Functions group code for reuse and better organization.",
                "code": """# Basic function
def greet():
    print("Hello!")
greet()

# With parameters
def greet_person(name):
    print(f"Hello, {name}!")
greet_person("Alice")

# Return value
def add(a, b):
    return a + b
result = add(5, 3)

# Multiple returns
def get_stats(nums):
    return min(nums), max(nums)
min_val, max_val = get_stats([1,5,3])

# Default parameters
def power(x, n=2):
    return x ** n
print(power(5))     # 25
print(power(5, 3))  # 125"""
            },
            {
                "id": "parameters",
                "name": "Parameters and Arguments",
                "duration": "40 min",
                "video": "https://www.youtube.com/embed/ijXMGpoMkhQ",
                "description": "Master positional, keyword, *args, and **kwargs parameters.",
                "content": "Different ways to pass data to functions.",
                "code": """# Positional
def greet(first, last):
    print(f"Hello {first} {last}")
greet("John", "Doe")

# Keyword
greet(last="Doe", first="John")

# Default
def make_profile(name, age=18):
    print(f"{name}, {age}")
make_profile("Alice")

# *args (variable arguments)
def sum_all(*numbers):
    return sum(numbers)
print(sum_all(1, 2, 3, 4))

# **kwargs (keyword arguments)
def print_info(**info):
    for k, v in info.items():
        print(f"{k}: {v}")
print_info(name="Alice", age=25)"""
            },
            {
                "id": "lambda",
                "name": "Lambda Functions",
                "duration": "35 min",
                "video": "https://www.youtube.com/embed/Ob9rY6PQMfI",
                "description": "Anonymous one-line functions. Useful for simple operations.",
                "content": "Lambda functions are compact alternatives to def for simple functions.",
                "code": """# Lambda syntax
square = lambda x: x ** 2
print(square(5))  # 25

# Multiple arguments
add = lambda a, b: a + b
print(add(3, 5))  # 8

# With map()
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
print(squared)

# With filter()
evens = list(filter(lambda x: x%2==0, nums))
print(evens)

# With sorted()
students = [("Alice", 85), ("Bob", 92)]
sorted_students = sorted(
    students,
    key=lambda x: x[1]
)"""
            }
        ]
    },
    "advanced": {
        "title": "Advanced Concepts",
        "topics": [
            {
                "id": "oop",
                "name": "Object-Oriented Programming",
                "duration": "90 min",
                "video": "https://www.youtube.com/embed/Ej_02ICOIgs",
                "description": "Classes, objects, inheritance, encapsulation, polymorphism.",
                "content": "OOP organizes code into objects with properties and methods.",
                "code": """# Basic class
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says Woof!"

dog = Dog("Buddy", 3)
print(dog.bark())

# Inheritance
class Animal:
    def __init__(self, name):
        self.name = name

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

cat = Cat("Whiskers")
print(cat.speak())

# Properties
class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @property
    def area(self):
        return 3.14 * self.radius ** 2

c = Circle(5)
print(c.area)"""
            },
            {
                "id": "file_handling",
                "name": "File Handling",
                "duration": "50 min",
                "video": "https://www.youtube.com/embed/Uh2ebFW8OYM",
                "description": "Read from and write to files. Work with CSV, JSON, and text files.",
                "content": "Files store data permanently. Python makes file operations easy.",
                "code": """# Write to file
with open('data.txt', 'w') as f:
    f.write("Hello, World!\\n")
    f.write("Python is great!")

# Read file
with open('data.txt', 'r') as f:
    content = f.read()
    print(content)

# Read lines
with open('data.txt', 'r') as f:
    for line in f:
        print(line.strip())

# JSON
import json
data = {"name": "Alice", "age": 25}
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# Read JSON
with open('data.json', 'r') as f:
    loaded = json.load(f)"""
            },
            {
                "id": "exception_handling",
                "name": "Exception Handling",
                "duration": "45 min",
                "video": "https://www.youtube.com/embed/6SPDvPK38tw",
                "description": "Handle errors gracefully with try-except-finally blocks.",
                "content": "Exceptions prevent crashes and provide user-friendly error messages.",
                "code": """# Basic try-except
try:
    x = int(input("Enter number: "))
    print(10 / x)
except ValueError:
    print("Invalid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Try-except-else-finally
try:
    file = open('data.txt', 'r')
    content = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("Success!")
finally:
    try:
        file.close()
    except:
        pass

# Raise exceptions
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b"""
            },
            {
                "id": "modules",
                "name": "Modules and Packages",
                "duration": "55 min",
                "video": "https://www.youtube.com/embed/GxCXiSkm6no",
                "description": "Organize code with modules. Use Python's standard library.",
                "content": "Modules group related code. Packages organize multiple modules.",
                "code": """# Import module
import math
print(math.pi)
print(math.sqrt(16))

# Import specific items
from math import pi, sqrt
print(pi)

# Import with alias
import numpy as np

# Standard library
import random
print(random.randint(1, 10))
print(random.choice(['a', 'b', 'c']))

from datetime import datetime
print(datetime.now())

import os
print(os.getcwd())
print(os.listdir('.'))

# Your own module
# mymodule.py:
# def greet(name):
#     return f"Hello, {name}!"
#
# import mymodule
# print(mymodule.greet("Alice"))"""
            }
        ]
    },
    "domains": {
        "title": "Python Domains & Applications",
        "topics": [
            {
                "id": "ml",
                "name": "Machine Learning with Python",
                "duration": "120 min",
                "video": "https://www.youtube.com/embed/7eh4d6sabA0",
                "description": "Introduction to ML with scikit-learn. Build predictive models.",
                "content": "Machine Learning lets computers learn from data without explicit programming.",
                "code": """# Install: pip install scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
print(predictions)

# Classification
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
# clf.fit(X_train, y_train)
# accuracy = clf.score(X_test, y_test)"""
            },
            {
                "id": "ai",
                "name": "Artificial Intelligence",
                "duration": "120 min",
                "video": "https://www.youtube.com/embed/aircAruvnKk",
                "description": "Deep learning with neural networks. TensorFlow and Keras.",
                "content": "AI includes neural networks, computer vision, NLP, and more.",
                "code": """# Install: pip install tensorflow
from tensorflow import keras
from tensorflow.keras import layers

# Build neural network
model = keras.Sequential([
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
# model.fit(X_train, y_train, epochs=10)

# Image classification
from tensorflow.keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train / 255.0"""
            },
            {
                "id": "blockchain",
                "name": "Blockchain Development",
                "duration": "90 min",
                "video": "https://www.youtube.com/embed/_160oMzblY8",
                "description": "Build blockchain and smart contracts. Learn Web3.py.",
                "content": "Blockchain is a distributed, immutable ledger for secure transactions.",
                "code": """# Simple blockchain
import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.new_block(proof=100, previous_hash='1')
    
    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

blockchain = Blockchain()"""
            },
            {
                "id": "web_dev",
                "name": "Web Development (Flask/Django)",
                "duration": "100 min",
                "video": "https://www.youtube.com/embed/Z1RJmh_OqeA",
                "description": "Build web apps with Flask or Django. Create APIs and websites.",
                "content": "Flask and Django are powerful web frameworks for building applications.",
                "code": """# Flask web app
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/user/<name>')
def user(name):
    return f"Hello, {name}!"

@app.route('/api/data')
def api():
    return {"message": "Hello API"}

# if __name__ == '__main__':
#     app.run(debug=True)

# Django (more features)
# django-admin startproject mysite
# python manage.py startapp myapp
# python manage.py runserver"""
            },
            {
                "id": "data_science",
                "name": "Data Science and Analytics",
                "duration": "110 min",
                "video": "https://www.youtube.com/embed/vmEHCJofslg",
                "description": "Pandas, NumPy, Matplotlib. Analyze and visualize data.",
                "content": "Data science uses statistics and ML to extract insights from data.",
                "code": """# Install: pip install pandas matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85, 90, 95]
}
df = pd.DataFrame(data)

# Analyze
print(df.describe())
print(df.mean())
print(df[df['age'] > 25])

# Visualize
df.plot(x='name', y='score', kind='bar')
# plt.show()

# Read CSV
# df = pd.read_csv('data.csv')
# df.to_csv('output.csv', index=False)"""
            }
        ]
    }
}

# Quiz questions pool
QUIZ_QUESTIONS = [
    {
        "question": "What is a loop in programming?",
        "options": [
            "A structure that repeats a block of code",
            "A type of variable",
            "A function that returns values",
            "A way to store data"
        ],
        "correct": 0,
        "difficulty": "beginner"
    },
    {
        "question": "What is a variable?",
        "options": [
            "A fixed value in code",
            "A container for storing data values",
            "A type of loop",
            "A programming language"
        ],
        "correct": 1,
        "difficulty": "beginner"
    },
    {
        "question": "What is HTML?",
        "options": [
            "A programming language",
            "A markup language for creating web pages",
            "A database system",
            "A Python framework"
        ],
        "correct": 1,
        "difficulty": "beginner"
    },
    {
        "question": "What is a stack data structure?",
        "options": [
            "A linear data structure following FIFO principle",
            "A linear data structure following LIFO principle",
            "A tree-based structure",
            "A type of array"
        ],
        "correct": 1,
        "difficulty": "intermediate"
    },
    {
        "question": "What are pointers?",
        "options": [
            "Variables that store memory addresses",
            "Functions in Python",
            "Types of loops",
            "Data visualization tools"
        ],
        "correct": 0,
        "difficulty": "intermediate"
    },
    {
        "question": "What is an array?",
        "options": [
            "A function",
            "A collection of elements of the same type stored in contiguous memory",
            "A type of loop",
            "A conditional statement"
        ],
        "correct": 1,
        "difficulty": "beginner"
    },
    {
        "question": "What does OOP stand for?",
        "options": [
            "Object-Oriented Programming",
            "Only One Program",
            "Operational Output Process",
            "Optional Oriented Protocol"
        ],
        "correct": 0,
        "difficulty": "intermediate"
    },
    {
        "question": "What is the purpose of a function?",
        "options": [
            "To store data",
            "To create loops",
            "To group reusable code",
            "To define variables"
        ],
        "correct": 2,
        "difficulty": "beginner"
    },
    {
        "question": "What is recursion?",
        "options": [
            "A loop structure",
            "A function calling itself",
            "A data type",
            "An operator"
        ],
        "correct": 1,
        "difficulty": "advanced"
    },
    {
        "question": "What is the difference between list and tuple in Python?",
        "options": [
            "Lists are immutable, tuples are mutable",
            "Lists are mutable, tuples are immutable",
            "They are the same",
            "Tuples can only store numbers"
        ],
        "correct": 1,
        "difficulty": "intermediate"
    },
    {
        "question": "What is a dictionary in Python?",
        "options": [
            "A list of words",
            "A key-value pair data structure",
            "A type of loop",
            "A function"
        ],
        "correct": 1,
        "difficulty": "intermediate"
    },
    {
        "question": "What does 'def' keyword do in Python?",
        "options": [
            "Defines a variable",
            "Defines a function",
            "Deletes a file",
            "Defines a class"
        ],
        "correct": 1,
        "difficulty": "beginner"
    }
]

def analyze_quiz_score(score, total):
    """AI-based analysis of quiz performance"""
    percentage = (score / total) * 100
    
    if percentage < 40:
        level = "Beginner"
        recommendations = {
            "level": "beginner",
            "content_type": "Easy",
            "focus_areas": ["Python Basics", "Variables and Data Types", "Basic Operators"],
            "suggested_topics": [
                "Start with Introduction to Python",
                "Learn about Variables and Data Types",
                "Practice simple Input/Output operations",
                "Understand basic operators"
            ],
            "practice_exercises": "Simple exercises and video tutorials",
            "message": "Don't worry! Everyone starts here. Focus on building a strong foundation."
        }
    elif percentage <= 70:
        level = "Intermediate"
        recommendations = {
            "level": "intermediate",
            "content_type": "Medium",
            "focus_areas": ["Control Flow", "Data Structures", "Functions"],
            "suggested_topics": [
                "Master loops and conditionals",
                "Deep dive into Lists and Dictionaries",
                "Learn about Functions and Parameters",
                "Practice problem-solving"
            ],
            "practice_exercises": "Practice problems and concept revision",
            "message": "You're making good progress! Time to strengthen your skills."
        }
    else:
        level = "Advanced"
        recommendations = {
            "level": "advanced",
            "content_type": "Hard",
            "focus_areas": ["OOP", "Advanced Concepts", "Python Domains"],
            "suggested_topics": [
                "Master Object-Oriented Programming",
                "Explore Machine Learning with Python",
                "Learn about AI and Blockchain",
                "Work on real-world projects"
            ],
            "practice_exercises": "Advanced projects and challenges",
            "message": "Excellent work! You're ready for advanced topics and projects."
        }
    
    recommendations["score"] = score
    recommendations["total"] = total
    recommendations["percentage"] = percentage
    recommendations["level_name"] = level
    
    # If AI API is enabled, enhance recommendations
    if USE_AI_API:
        try:
            ai_enhanced = get_ai_enhanced_recommendations(score, total, percentage, level)
            if ai_enhanced:
                recommendations["ai_insights"] = ai_enhanced
        except Exception as e:
            print(f"AI API Error: {e}")
            # Continue with rule-based recommendations
    
    return recommendations

def get_ai_enhanced_recommendations(score, total, percentage, level):
    """Get enhanced recommendations from Claude AI API"""
    if not ANTHROPIC_API_KEY:
        return None
    
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        prompt = f"""You are an expert Python programming tutor analyzing a student's quiz performance.

Quiz Results:
- Score: {score}/{total} ({percentage:.1f}%)
- Level: {level}

Based on this performance, provide:
1. A personalized learning path (3-4 specific next steps)
2. Key concepts they should focus on
3. One specific project idea matching their level
4. Motivational advice

Keep the response concise, practical, and encouraging. Format as a JSON object with keys: learning_path, focus_concepts, project_idea, motivation."""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract text content from response
        response_text = message.content[0].text
        
        # Try to parse as JSON, otherwise return as text
        try:
            import json
            return json.loads(response_text)
        except:
            return {"ai_advice": response_text}
    
    except Exception as e:
        print(f"AI Enhancement Error: {e}")
        return None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
        else:
            data = request.form
        
        username = data.get('username')
        password = data.get('password')
        
        # Simple authentication (replace with proper auth in production)
        if username and password:
            user_id = username.lower()
            
            if user_id not in users_db:
                # New user registration
                users_db[user_id] = {
                    'username': username,
                    'password': password,
                    'created_at': datetime.now().isoformat()
                }
                learning_progress[user_id] = {
                    'completed_topics': [],
                    'current_topic': None,
                    'total_time': 0,
                    'streak_days': 0,
                    'last_active': datetime.now().isoformat()
                }
                quiz_attempts[user_id] = []
                leaderboard_data[user_id] = {
                    'username': username,
                    'total_score': 0,
                    'quizzes_taken': 0,
                    'streak': 0
                }
            
            session['user_id'] = user_id
            session['username'] = username
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return redirect(url_for('home'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
        else:
            return redirect(url_for('index'))
    
    # GET request
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    progress = learning_progress.get(user_id, {})
    
    return render_template('home.html', 
                         username=session.get('username'),
                         progress=progress)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    user_data = users_db.get(user_id, {})
    
    return render_template('profile.html', 
                         username=session.get('username'),
                         user_data=user_data)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.json
    user_id = session['user_id']
    
    if user_id in users_db:
        users_db[user_id].update({
            'full_name': data.get('name'),
            'education': data.get('education'),
            'dob': data.get('dob'),
            'mobile': data.get('mobile')
        })
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    
    return jsonify({'success': False, 'message': 'User not found'})

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('quiz.html', username=session.get('username'))

@app.route('/get_quiz_questions')
def get_quiz_questions():
    # Randomly select 10 questions and shuffle them
    selected_questions = random.sample(QUIZ_QUESTIONS, min(10, len(QUIZ_QUESTIONS)))
    
    # Shuffle options for each question
    quiz_data = []
    for q in selected_questions:
        shuffled_q = q.copy()
        options = shuffled_q['options'].copy()
        correct_answer = options[shuffled_q['correct']]
        
        random.shuffle(options)
        new_correct_index = options.index(correct_answer)
        
        shuffled_q['options'] = options
        shuffled_q['correct'] = new_correct_index
        quiz_data.append(shuffled_q)
    
    random.shuffle(quiz_data)
    
    # Remove correct answers before sending to client
    client_quiz = []
    for q in quiz_data:
        client_quiz.append({
            'question': q['question'],
            'options': q['options'],
            'difficulty': q['difficulty']
        })
    
    # Store correct answers in session
    session['current_quiz'] = quiz_data
    
    return jsonify(client_quiz)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.json
    answers = data.get('answers', [])
    current_quiz = session.get('current_quiz', [])
    
    if not current_quiz:
        return jsonify({'success': False, 'message': 'No active quiz'})
    
    # Calculate score
    score = 0
    for i, answer in enumerate(answers):
        if i < len(current_quiz) and answer == current_quiz[i]['correct']:
            score += 1
    
    total = len(current_quiz)
    
    # Analyze and get recommendations
    recommendations = analyze_quiz_score(score, total)
    
    # Save quiz attempt
    user_id = session['user_id']
    if user_id not in quiz_attempts:
        quiz_attempts[user_id] = []
    
    quiz_attempts[user_id].append({
        'date': datetime.now().isoformat(),
        'score': score,
        'total': total,
        'percentage': recommendations['percentage'],
        'level': recommendations['level_name']
    })
    
    # Update leaderboard
    if user_id in leaderboard_data:
        leaderboard_data[user_id]['total_score'] += score
        leaderboard_data[user_id]['quizzes_taken'] += 1
    
    return jsonify({
        'success': True,
        'score': score,
        'total': total,
        'recommendations': recommendations
    })

@app.route('/ai_suggestions')
def ai_suggestions():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    attempts = quiz_attempts.get(user_id, [])
    
    # Get latest recommendations
    latest_recommendation = None
    if attempts:
        latest = attempts[-1]
        latest_recommendation = analyze_quiz_score(latest['score'], latest['total'])
    
    return render_template('ai_suggestions.html', 
                         username=session.get('username'),
                         recommendation=latest_recommendation,
                         attempts=attempts)

@app.route('/learning_content')
def learning_content():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    progress = learning_progress.get(user_id, {})
    completed = progress.get('completed_topics', [])
    
    return render_template('learning_content.html', 
                         username=session.get('username'),
                         content=LEARNING_CONTENT,
                         completed_topics=completed)

@app.route('/my_learning')
def my_learning():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    progress = learning_progress.get(user_id, {})
    attempts = quiz_attempts.get(user_id, [])
    
    return render_template('my_learning.html', 
                         username=session.get('username'),
                         progress=progress,
                         attempts=attempts)

@app.route('/mark_complete', methods=['POST'])
def mark_complete():
    if 'user_id' not in session:
        return jsonify({'success': False})
    
    data = request.json
    topic_id = data.get('topic_id')
    user_id = session['user_id']
    
    if user_id in learning_progress:
        if topic_id not in learning_progress[user_id]['completed_topics']:
            learning_progress[user_id]['completed_topics'].append(topic_id)
            learning_progress[user_id]['last_active'] = datetime.now().isoformat()
        return jsonify({'success': True})
    
    return jsonify({'success': False})

@app.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Sort leaderboard by total score
    sorted_leaderboard = sorted(
        leaderboard_data.items(),
        key=lambda x: x[1]['total_score'],
        reverse=True
    )
    
    return render_template('leaderboard.html', 
                         username=session.get('username'),
                         leaderboard=sorted_leaderboard,
                         current_user=session['user_id'])

@app.route('/ai_tutor', methods=['POST'])
def ai_tutor():
    """Simple AI tutor using rule-based responses"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.json
    message = data.get('message', '').lower()
    
    # Rule-based responses
    response = ""
    
    if any(word in message for word in ['loop', 'loops', 'iteration']):
        response = "Loops are used to repeat a block of code. Python has 'for' loops (for iterating over sequences) and 'while' loops (for repeating while a condition is true). Would you like to see examples?"
    elif any(word in message for word in ['variable', 'variables']):
        response = "Variables are containers for storing data values. In Python, you create a variable by assigning a value to it: x = 5. Python automatically determines the data type!"
    elif any(word in message for word in ['function', 'functions']):
        response = "Functions are reusable blocks of code. Define them with 'def' keyword: def my_function(): ... They help organize code and avoid repetition."
    elif any(word in message for word in ['list', 'lists', 'array']):
        response = "Lists in Python store multiple items in a single variable. Create them with square brackets: my_list = [1, 2, 3]. Lists are mutable and can contain different data types!"
    elif any(word in message for word in ['dictionary', 'dict']):
        response = "Dictionaries store key-value pairs. Create them with curly braces: my_dict = {'name': 'John', 'age': 25}. Access values using keys: my_dict['name']"
    elif any(word in message for word in ['help', 'stuck', 'confused']):
        response = "I'm here to help! Try breaking down the problem into smaller steps. Review the learning materials, and don't hesitate to retake the quiz to reinforce your understanding."
    elif any(word in message for word in ['beginner', 'start', 'new']):
        response = "Great that you're starting! Begin with Python Basics - learn about variables, data types, and basic operators. Take it step by step, and practice with simple exercises."
    else:
        response = "I'm your AI tutor! I can help you with Python concepts like loops, variables, functions, lists, dictionaries, and more. What would you like to learn about?"
    
    return jsonify({
        'success': True,
        'response': response
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("ELWA - E-Learning Web Application")
    print("By Tech X Espadas")
    print("="*60)
    print("\nServer starting...")
    print("Access the application at: http://localhost:5000")
    print("Press CTRL+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
