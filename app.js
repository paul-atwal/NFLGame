const newGameButton = document.querySelector("#newGameButton");
const newGuessButton = document.querySelector("#newGuess");
const feedbackMessage = document.querySelector("#feedbackMessage");
const qbNameDisplay = document.querySelector("#qbNameDisplay");
const guessBadge = document.querySelector(".badge");
const numSimilarQBs = 5;
const qbGuessInput = document.querySelector("#qbGuess");
const suggestionsContainer = document.querySelector("#suggestions");

let incorrectGuesses = 0;
let correctGuesses = [];

newGameButton.addEventListener("click", startNewGame);
newGuessButton.addEventListener("click", checkGuess);
qbGuessInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    checkGuess();
  }
});

qbGuessInput.addEventListener("input", () => {
  const userInput = qbGuessInput.value.toLowerCase();

  // Fetch the list of QB names from backend
  fetch("http://localhost:5001/qb-names")
    .then((response) => response.json())
    .then((qbNames) => {
      // Filter QB names based on input value
      const filteredNames = qbNames.filter((name) =>
        name.toLowerCase().startsWith(userInput)
      );

      // Clear previous suggestions
      suggestionsContainer.innerHTML = "";

      // Display new suggestions
      filteredNames.forEach((name) => {
        const suggestionElement = document.createElement("div");
        suggestionElement.textContent = name;
        suggestionElement.className = "suggestion";
        suggestionElement.addEventListener("click", () => {
          qbGuessInput.value = name;
          suggestionsContainer.innerHTML = "";
        });
        suggestionsContainer.appendChild(suggestionElement);
      });
    })
    .catch((error) => console.error("Error:", error));
});

function startNewGame() {
  fetch("http://localhost:5001/random-qb")
    .then((response) => response.json())
    .then((data) => {
      qbNameDisplay.textContent = data;
      incorrectGuesses = 0;
      correctGuesses = [];
      clearFeedback();
      guessBadge.textContent = incorrectGuesses;
      clearCards();
    })
    .catch((error) => console.error("Error:", error));
}

function clearCards() {
  const cards = document.querySelectorAll(".card-title");
  cards.forEach((card, index) => {
    card.textContent = "#" + (index + 1);
  });
}

function clearFeedback() {
  const feedbackMessage = document.querySelector("#feedbackMessage");
  feedbackMessage.textContent = "";
}

const newGuess = document.querySelector("#newGuess");
newGuess.addEventListener("click", checkGuess);

function checkGuess() {
  const qbNameDisplay = document.querySelector("#qbNameDisplay");
  const qbGuess = document.querySelector("#qbGuess").value;
  const feedbackMessage = document.querySelector("#feedbackMessage");

  const qbName = qbNameDisplay.textContent;

  fetch(`http://localhost:5001/similar-qbs/${qbName}`)
    .then((response) => response.json())
    .then((similarQbList) => {
      const guessedIndex = similarQbList.indexOf(qbGuess);

      if (correctGuesses.includes(qbGuess)) {
        feedbackMessage.textContent = "Already correctly guessed.";
      } else if (guessedIndex !== -1) {
        correctGuesses.push(qbGuess);
        feedbackMessage.textContent = "Correct!";
        document.querySelector(`#card${guessedIndex + 1}`).textContent =
          qbGuess;
      } else {
        feedbackMessage.textContent = "Incorrect!";
        incorrectGuesses++;
        document.querySelector(".badge").textContent = incorrectGuesses;
      }
      document.querySelector("#qbGuess").value = "";

      isGameOver();
    })
    .catch((error) => {
      console.error("Error:", error);
      feedbackMessage.textContent = "An error occurred. Please try again.";
    });
}

function isGameOver() {
  if (correctGuesses.length === numSimilarQBs) {
    feedbackMessage.textContent =
      "Congratulations! You've found all similar QBs!";
    // Disable the guess input and button to prevent further guesses
  } else if (incorrectGuesses >= 3) {
    feedbackMessage.textContent =
      "Game over! You've made too many incorrect guesses.";
    // Fetch and reveal the remaining QBs and disable further guesses
    fetch(`http://localhost:5001/similar-qbs/${qbNameDisplay.textContent}`)
      .then((response) => response.json())
      .then(revealAnswers)
      .catch((error) => console.error("Error:", error));
  }
}

function revealAnswers(similarQbList) {
  similarQbList.forEach((qb, index) => {
    document.querySelector(`#card${index + 1}`).textContent = qb;
  });
}
