# NFL Quarterback Similarity Web Game

## Overview

This interactive web game allows users to identify NFL quarterbacks with similar playing styles based on historical performance data. The application is built using Flask for the backend, with a frontend utilizing HTML, CSS, and JavaScript.

## Prerequisites

Before running the application, ensure you have Python installed on your system. The application requires certain Python libraries such as Flask, pandas, and sklearn, which can be installed using pip.

## Setup

To set up the application, follow these steps:

- Clone the Repository
- Install Dependencies
- Execute setup.py to fetch and prepare the initial dataset:

- Run setup.py and qbdata.py to process the data and generate the required CSV file.
- Ensure that the generated CSV file is in the same directory as the Flask application for it to function correctly.

- Running the Application
- Start the Flask server by running app.py. This will start the backend server on localhost:5001.

- Navigate to the directory containing index.html.
- Open index.html in a web browser to interact with the game.

## Usage

Click "New Game" to start the game and receive the name of a random NFL quarterback.
Enter your guesses of similar quarterbacks in the input field and submit.
The game will reveal how closely your guesses match the data-driven similarity analysis.
