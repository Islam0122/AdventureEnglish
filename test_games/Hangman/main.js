window.onload = async () => {
  let startTimer = new Date();
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split("");
  const string = document.querySelector('.string');
  const image = document.querySelector('img');
  const ulKeyboard = document.querySelector('ul');
  const categoryDisplay = document.querySelector('.category');

  let password = [];
  let hint = "";
  let counter = 0;

  // Получаем слова через API
  async function getHangmanWords() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/games/hangman-words/");
      const data = await response.json();
      return data.map(item => ({
        word: item.word.toUpperCase(),
        hint: item.hint
      }));
    } catch (err) {
      console.error("Ошибка загрузки слов:", err);
      return [];
    }
  }

  // Инициализация игры
  async function startGame() {
    const words = await getHangmanWords();
    if (!words.length) return alert("Нет слов для игры!");

    const randomIndex = Math.floor(Math.random() * words.length);
    password = words[randomIndex].word.split('');
    hint = words[randomIndex].hint;

    counter = 0;
    string.textContent = "";
    ulKeyboard.innerHTML = "";
    categoryDisplay.textContent = hint;
    image.src = "img/s0.png";

    for (let i = 0; i < password.length; i++) {
      string.textContent += password[i] === " " ? " " : "_";
    }

    alphabet.forEach(letter => {
      const btn = document.createElement('li');
      btn.textContent = letter;
      btn.addEventListener('click', letterCheck);
      ulKeyboard.appendChild(btn);
    });
  }

  String.prototype.replaceAt = function (index, replacement) {
    return this.substr(0, index) + replacement + this.substr(index + replacement.length);
  }

  function letterCheck(e) {
    const letter = e.target.textContent;
    let check = false;

    password.forEach((char, i) => {
      if (char === letter) {
        string.textContent = string.textContent.replaceAt(i, letter);
        check = true;
      }
    });

    if (check) e.target.classList.add('clicked');
    else if (!e.target.classList.contains('clicked')) {
      counter++;
      e.target.classList.add('clicked');
      image.src = `img/s${counter}.png`;
    }

    if (string.textContent === password.join('')) {
      endGame(true);
    } else if (counter >= 7) {
      endGame(false);
    }
  }

  async function endGame(won) {
    image.src = won ? "img/s8.png" : image.src;
    const stopTimer = new Date();
    const durationSec = Math.floor((stopTimer - startTimer) / 1000);
    const minutes = Math.floor(durationSec / 60);
    const seconds = durationSec % 60;

    ulKeyboard.innerHTML = won
      ? `You won! Time: ${minutes}min ${seconds}s<br/><div class="reset"><img class="tryAgain" src="img/spin.png"/></div>`
      : `You're dead! Word: <span style="color:red">${password.join('')}</span><br/><div class="reset"><img class="tryAgain" src="img/spin.png"/></div>`;

    document.querySelector('.tryAgain').addEventListener('click', startGame);

    // Отправляем результат на API
    const score = won ? 100 : 0; // пример
    const accuracy = won ? 100 : 0;
    await sendGameResult(score, 100, accuracy, durationSec);
  }

  async function sendGameResult(score, max_score, accuracy, duration) {
    try {
      await fetch("http://127.0.0.1:8000/api/games/game-results/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("access") // если JWT
        },
        body: JSON.stringify({
          game: 1, // ID Hangman
          score,
          max_score,
          accuracy,
          duration,
          meta: { hintUsed: hint }
        })
      });
    } catch (err) {
      console.error("Ошибка отправки результата:", err);
    }
  }

  document.querySelector('.reroll').addEventListener('click', startGame);
  await startGame();
}
