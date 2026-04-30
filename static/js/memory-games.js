// Визуальная память - запоминание цветов
class ColorMemoryGame {
    constructor(colors, onComplete) {
        this.colors = colors;
        this.onComplete = onComplete;
        this.targetColor = colors[Math.floor(Math.random() * colors.length)];
        this.init();
    }
    
    init() {
        const container = document.getElementById('game-container');
        container.innerHTML = `
            <div class="text-center">
                <h4>Запомните этот цвет!</h4>
                <div class="color-display my-4" style="width: 200px; height: 200px; margin: 0 auto; background-color: ${this.targetColor}; border-radius: 10px;"></div>
                <p class="text-muted">У вас есть 3 секунды...</p>
                <div id="countdown" class="display-4">3</div>
            </div>
        `;
        
        let seconds = 3;
        const countdown = setInterval(() => {
            seconds--;
            document.getElementById('countdown').textContent = seconds;
            if (seconds <= 0) {
                clearInterval(countdown);
                this.showQuestion();
            }
        }, 1000);
    }
    
    showQuestion() {
        const container = document.getElementById('game-container');
        const shuffled = [...this.colors].sort(() => Math.random() - 0.5);
        
        container.innerHTML = `
            <div class="text-center">
                <h4>Какой цвет был показан?</h4>
                <div class="row mt-4">
                    ${shuffled.map(color => `
                        <div class="col-md-3 mb-3">
                            <button class="btn btn-lg w-100" style="background-color: ${color}; height: 100px;" onclick="window.currentGame.checkAnswer('${color}')"></button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    checkAnswer(selectedColor) {
        const isCorrect = selectedColor === this.targetColor;
        this.onComplete(isCorrect);
    }
}

// Числовая память - запоминание последовательности
class NumberMemoryGame {
    constructor(numbers, onComplete) {
        this.numbers = numbers;
        this.onComplete = onComplete;
        this.userInput = [];
        this.init();
    }
    
    init() {
        const container = document.getElementById('game-container');
        container.innerHTML = `
            <div class="text-center">
                <h4>Запомните последовательность чисел!</h4>
                <div class="numbers-display my-4">
                    ${this.numbers.map(n => `<span class="badge bg-primary fs-2 mx-2">${n}</span>`).join('')}
                </div>
                <p class="text-muted">У вас есть 5 секунд...</p>
                <div id="countdown" class="display-4">5</div>
            </div>
        `;
        
        let seconds = 5;
        const countdown = setInterval(() => {
            seconds--;
            document.getElementById('countdown').textContent = seconds;
            if (seconds <= 0) {
                clearInterval(countdown);
                this.showQuestion();
            }
        }, 1000);
    }
    
    showQuestion() {
        const container = document.getElementById('game-container');
        container.innerHTML = `
            <div class="text-center">
                <h4>Введите последовательность чисел через запятую</h4>
                <div class="mt-4">
                    <input type="text" id="user-sequence" class="form-control form-control-lg w-50 mx-auto" placeholder="Пример: 1,2,3,4,5">
                    <button class="btn btn-primary btn-lg mt-3" onclick="window.currentGame.checkAnswer()">Проверить</button>
                </div>
            </div>
        `;
    }
    
    checkAnswer() {
        const userInput = document.getElementById('user-sequence').value;
        const userNumbers = userInput.split(',').map(n => parseInt(n.trim()));
        const isCorrect = JSON.stringify(userNumbers) === JSON.stringify(this.numbers);
        this.onComplete(isCorrect);
    }
}

// Текстовая память - запоминание слов
class TextMemoryGame {
    constructor(words, onComplete) {
        this.words = words;
        this.onComplete = onComplete;
        this.init();
    }
    
    init() {
        const container = document.getElementById('game-container');
        container.innerHTML = `
            <div class="text-center">
                <h4>Запомните эти слова!</h4>
                <div class="words-display my-4">
                    ${this.words.map(word => `<span class="badge bg-success fs-4 mx-2">${word}</span>`).join('')}
                </div>
                <p class="text-muted">У вас есть 10 секунд...</p>
                <div id="countdown" class="display-4">10</div>
            </div>
        `;
        
        let seconds = 10;
        const countdown = setInterval(() => {
            seconds--;
            document.getElementById('countdown').textContent = seconds;
            if (seconds <= 0) {
                clearInterval(countdown);
                this.showQuestion();
            }
        }, 1000);
    }
    
    showQuestion() {
        const container = document.getElementById('game-container');
        const shuffled = [...this.words].sort(() => Math.random() - 0.5);
        
        container.innerHTML = `
            <div class="text-center">
                <h4>Какие слова были показаны?</h4>
                <div class="mt-4">
                    ${shuffled.map(word => `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="${word}" id="word-${word}">
                            <label class="form-check-label" for="word-${word}">${word}</label>
                        </div>
                    `).join('')}
                    <button class="btn btn-primary btn-lg mt-3" onclick="window.currentGame.checkAnswer()">Проверить</button>
                </div>
            </div>
        `;
    }
    
    checkAnswer() {
        const selected = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(cb => cb.value);
        const isCorrect = selected.length === this.words.length && 
                         selected.every(word => this.words.includes(word));
        this.onComplete(isCorrect);
    }
}

// Паттерны - запоминание сетки
class PatternMemoryGame {
    constructor(gridSize, pattern, onComplete) {
        this.gridSize = gridSize;
        this.pattern = pattern;
        this.onComplete = onComplete;
        this.userPattern = [];
        this.init();
    }
    
    init() {
        const container = document.getElementById('game-container');
        const totalCells = this.gridSize * this.gridSize;
        
        // Создаём сетку для показа
        let gridHtml = '<div class="pattern-grid" style="display: grid; grid-template-columns: repeat(' + this.gridSize + ', 80px); gap: 10px; justify-content: center;">';
        
        for (let i = 0; i < totalCells; i++) {
            const isActive = this.pattern.includes(i);
            const bgColor = isActive ? '#28a745' : '#f0f0f0';
            gridHtml += `<div style="width: 80px; height: 80px; background-color: ${bgColor}; border: 2px solid #ddd; border-radius: 5px;"></div>`;
        }
        gridHtml += '</div>';
        
        container.innerHTML = `
            <div class="text-center">
                <h4>Запомните расположение зелёных клеток!</h4>
                ${gridHtml}
                <p class="text-muted mt-3">У вас есть 5 секунд...</p>
                <div id="countdown" class="display-4">5</div>
            </div>
        `;
        
        let seconds = 5;
        const countdown = setInterval(() => {
            seconds--;
            document.getElementById('countdown').textContent = seconds;
            if (seconds <= 0) {
                clearInterval(countdown);
                this.showQuestion();
            }
        }, 1000);
    }
    
    showQuestion() {
        const container = document.getElementById('game-container');
        const totalCells = this.gridSize * this.gridSize;
        
        let gridHtml = '<div class="pattern-grid" style="display: grid; grid-template-columns: repeat(' + this.gridSize + ', 80px); gap: 10px; justify-content: center;">';
        
        for (let i = 0; i < totalCells; i++) {
            gridHtml += `
                <div class="pattern-cell" 
                     style="width: 80px; height: 80px; background-color: #f0f0f0; border: 2px solid #ddd; border-radius: 5px; cursor: pointer; transition: all 0.3s;"
                     data-cell="${i}"
                     onclick="window.currentGame.toggleCell(${i})">
                </div>
            `;
        }
        gridHtml += '</div>';
        
        container.innerHTML = `
            <div class="text-center">
                <h4>Повторите расположение зелёных клеток</h4>
                ${gridHtml}
                <button class="btn btn-primary btn-lg mt-4" onclick="window.currentGame.checkAnswer()">Проверить</button>
            </div>
        `;
        
        // Добавляем стили для активных клеток
        const style = document.createElement('style');
        style.textContent = `
            .pattern-cell.active {
                background-color: #28a745 !important;
                transform: scale(0.95);
            }
        `;
        document.head.appendChild(style);
    }
    
    toggleCell(cellIndex) {
        const cell = document.querySelector(`.pattern-cell[data-cell="${cellIndex}"]`);
        if (this.userPattern.includes(cellIndex)) {
            // Убираем клетку
            this.userPattern = this.userPattern.filter(i => i !== cellIndex);
            cell.classList.remove('active');
        } else {
            // Добавляем клетку
            this.userPattern.push(cellIndex);
            cell.classList.add('active');
        }
    }
    
    checkAnswer() {
        // Сортируем массивы для сравнения
        const userPatternSorted = [...this.userPattern].sort((a, b) => a - b);
        const patternSorted = [...this.pattern].sort((a, b) => a - b);
        
        // Сравниваем
        const isCorrect = userPatternSorted.length === patternSorted.length &&
                         userPatternSorted.every((val, index) => val === patternSorted[index]);
        
        this.onComplete(isCorrect);
    }
}