document.addEventListener("DOMContentLoaded", () => {
    const puzzle = document.getElementById("puzzle");
    const message = document.getElementById("message");
    const resetButton = document.getElementById("reset");
    const stepCountElement = document.getElementById("step-count");
    const timeElement = document.getElementById("time");
    const saveRecordDiv = document.getElementById("save-record");
    const nameInput = document.getElementById("name");
    const saveButton = document.getElementById("save");
    const leaderboardBody = document.querySelector("#leaderboard tbody");

    // 初始拼图布局
    let layout = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "_"]
    ];

    // 步数计数器
    let stepCount = 0;

    // 计时器
    let startTime = null;
    let timerInterval = null;

    // 初始化游戏
    function initGame() {
        shuffleLayout();
        while (!isSolvable(layout)) {
            shuffleLayout();
        }
        stepCount = 0; // 重置步数
        startTime = Date.now(); // 重置计时器
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(updateTime, 1000);
        updatePuzzle();
        updateStepCount();
        updateTime();
        message.textContent = "";
        saveRecordDiv.style.display = "none"; // 隐藏保存记录表单
    }

    // 打乱拼图布局
    function shuffleLayout() {
        let flatLayout = layout.flat().filter(cell => cell !== "_");
        for (let i = flatLayout.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [flatLayout[i], flatLayout[j]] = [flatLayout[j], flatLayout[i]];
        }
        flatLayout.push("_");
        layout = [];
        for (let i = 0; i < 3; i++) {
            layout.push(flatLayout.slice(i * 3, (i + 1) * 3));
        }
    }

    // 检查拼图是否有解
    function isSolvable(layout) {
        let flatLayout = layout.flat().filter(cell => cell !== "_");
        let inversions = 0;
        for (let i = 0; i < flatLayout.length; i++) {
            for (let j = i + 1; j < flatLayout.length; j++) {
                if (flatLayout[i] > flatLayout[j]) {
                    inversions++;
                }
            }
        }
        return inversions % 2 === 0;
    }

    // 检查是否胜利
    function checkWin() {
        const targetLayout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "_"]
        ];
        return JSON.stringify(layout) === JSON.stringify(targetLayout);
    }

    // 更新拼图界面
    function updatePuzzle() {
        puzzle.innerHTML = layout
            .map(
                (row, i) => `
                <div class="row">
                    ${row
                        .map(
                            (cell, j) => `
                            <div class="cell" data-row="${i}" data-col="${j}">
                                ${cell !== "_" ? cell : ""}
                            </div>
                        `
                        )
                        .join("")}
                </div>
            `
            )
            .join("");
    }

    // 更新步数显示
    function updateStepCount() {
        stepCountElement.textContent = stepCount;
    }

    // 更新时间显示
    function updateTime() {
        const currentTime = Math.floor((Date.now() - startTime) / 1000);
        timeElement.textContent = currentTime;
    }

    // 处理点击事件
    puzzle.addEventListener("click", (event) => {
        const cell = event.target;
        if (cell.classList.contains("cell")) {
            const row = parseInt(cell.getAttribute("data-row"));
            const col = parseInt(cell.getAttribute("data-col"));
            movePiece(row, col);
        }
    });

    // 移动拼图块
    function movePiece(row, col) {
        // 找到空格的位置
        let emptyRow = -1, emptyCol = -1;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (layout[i][j] === "_") {
                    emptyRow = i;
                    emptyCol = j;
                    break;
                }
            }
        }

        // 检查是否与空格相邻
        if (Math.abs(row - emptyRow) + Math.abs(col - emptyCol) === 1) {
            // 交换位置
            [layout[row][col], layout[emptyRow][emptyCol]] = [layout[emptyRow][emptyCol], layout[row][col]];
            stepCount++; // 增加步数
            updatePuzzle();
            updateStepCount();

            // 检查是否胜利
            if (checkWin()) {
                message.textContent = "恭喜你，胜利了！";
                clearInterval(timerInterval); // 停止计时器
                saveRecordDiv.style.display = "block"; // 显示保存记录表单
            }
        }
    }

    // 保存记录
    saveButton.addEventListener("click", () => {
        const name = nameInput.value.trim();
        const time = Math.floor((Date.now() - startTime) / 1000);
        if (name) {
            fetch("/records", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, steps: stepCount, time }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "success") {
                        loadLeaderboard(); // 刷新排行榜
                        saveRecordDiv.style.display = "none"; // 隐藏保存记录表单
                    }
                });
        }
    });

    // 加载排行榜
    function loadLeaderboard() {
        fetch("/records")
            .then((response) => response.json())
            .then((data) => {
                leaderboardBody.innerHTML = data
                    .map(
                        (record, index) => `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${record.name}</td>
                            <td>${record.steps}</td>
                            <td>${record.time}</td>
                        </tr>
                    `
                    )
                    .join("");
            });
    }

    // 重新开始游戏
    resetButton.addEventListener("click", initGame);

    // 初始化游戏
    initGame();
    loadLeaderboard(); // 加载排行榜
});