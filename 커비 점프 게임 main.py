import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="스트림릿 커비 점프 게임",
    page_icon="⭐",
    layout="centered"
)

st.title("⭐ 커비 점프 게임")
st.caption("스페이스바(Space) 또는 위쪽 화살표(↑) 키를 눌러 점프하세요!")

# HTML/JS 기반 커비 게임 코드
kirby_game_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: monospace;
            user-select: none;
        }
        
        /* --- 배경 및 게임 컨테이너 설정 (푸른 초원) --- */
        #game-container {
            position: relative;
            width: 600px;
            height: 200px;
            /* 푸른 하늘 그라데이션 */
            background: linear-gradient(to bottom, #70c5ce 0%, #b1e5eb 70%, #d8f3f5 100%);
            border: 2px solid #3a7d44;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }

        /* 배경 구름 */
        .cloud {
            position: absolute;
            background: #ffffff;
            border-radius: 20px;
            opacity: 0.8;
        }
        .cloud::before, .cloud::after {
            content: '';
            position: absolute;
            background: #ffffff;
            border-radius: 50%;
        }
        .cloud-1 {
            top: 20px; left: 80px; width: 60px; height: 18px;
        }
        .cloud-1::before { width: 25px; height: 25px; top: -10px; left: 10px; }
        .cloud-1::after { width: 20px; height: 20px; top: -6px; left: 28px; }

        .cloud-2 {
            top: 35px; left: 380px; width: 80px; height: 22px;
        }
        .cloud-2::before { width: 32px; height: 32px; top: -14px; left: 15px; }
        .cloud-2::after { width: 24px; height: 24px; top: -8px; left: 38px; }

        /* 멀리 보이는 언덕/산 */
        .hill {
            position: absolute;
            bottom: 15px;
            width: 200px;
            height: 60px;
            background-color: #8ed172;
            border-radius: 50% 50% 0 0;
            z-index: 1;
        }
        .hill-1 { left: -30px; }
        .hill-2 { left: 220px; width: 280px; height: 80px; background-color: #7bc45f; }
        .hill-3 { left: 450px; }

        /* 바닥 (잔디밭) */
        #ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 16px;
            background-color: #5bb343; /* 풀밭 녹색 */
            border-top: 3px solid #3e8e2b; /* 짙은 잔디 테두리 */
            z-index: 5;
        }
        
        /* --- 커비(Kirby) 디자인 --- */
        #kirby {
            position: absolute;
            bottom: 16px;
            left: 50px;
            width: 40px;
            height: 40px;
            background-color: #ffb6c1;
            border-radius: 50%;
            border: 2px solid #e0738d;
            box-sizing: border-box;
            z-index: 10;
        }
        #kirby::before, #kirby::after {
            content: '';
            position: absolute;
            top: 8px;
            width: 4px;
            height: 10px;
            background-color: #2b3a42;
            border-radius: 2px;
        }
        #kirby::before { left: 20px; }
        #kirby::after { left: 28px; }
        
        .blush {
            position: absolute;
            top: 20px;
            width: 6px;
            height: 4px;
            background-color: #ff69b4;
            border-radius: 50%;
        }
        .blush-left { left: 16px; }
        .blush-right { left: 31px; }

        .feet {
            position: absolute;
            bottom: -4px;
            left: 6px;
            width: 24px;
            height: 8px;
            background-color: #d11a45;
            border-radius: 10px;
            z-index: -1;
        }

        /* --- 장애물 디자인 --- */
        .obstacle {
            position: absolute;
            box-sizing: border-box;
            z-index: 10;
        }
        
        /* 지상 장애물 (버섯) */
        .ground-obstacle {
            bottom: 16px;
            width: 30px;
            height: 30px;
            background-color: #f00;
            border-radius: 50% 50% 10% 10%;
            border: 2px solid #a00;
        }
        .ground-obstacle::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 7px;
            width: 12px;
            height: 12px;
            background-color: #fff;
            border: 2px solid #ccc;
            border-radius: 2px;
        }
        .ground-obstacle::before {
            content: '';
            position: absolute;
            top: 5px;
            left: 7px;
            width: 12px;
            height: 12px;
            background-color: #fff;
            border-radius: 50%;
        }
        
        /* 공중 장애물 (드래곤) */
        .air-obstacle {
            bottom: 80px;
            width: 40px;
            height: 30px;
            background-color: #444;
            border: 2px solid #222;
            border-radius: 10% 10% 50% 50%;
        }
        .air-obstacle::after {
            content: '';
            position: absolute;
            top: -10px;
            left: 5px;
            width: 15px;
            height: 15px;
            background-color: #f00;
            border-radius: 50%;
        }
        .air-obstacle::before {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 10px;
            width: 20px;
            height: 5px;
            background-color: #444;
            border-radius: 2px;
        }

        #score-board {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 16px;
            font-weight: bold;
            color: #2d5a27;
            z-index: 20;
        }
        #heart-board {
            position: absolute;
            top: 10px;
            left: 15px;
            font-size: 20px;
            color: #f00;
            z-index: 20;
        }
        #game-over {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #2d5a27;
            z-index: 30;
            background-color: rgba(255, 255, 255, 0.85);
            padding: 15px 25px;
            border-radius: 8px;
            border: 2px solid #2d5a27;
        }
        #game-over h2 {
            margin: 0 0 10px 0;
            font-size: 20px;
        }
        #game-over p {
            margin: 0;
            font-size: 12px;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- 초원 배경 요소들 -->
    <div class="cloud cloud-1"></div>
    <div class="cloud cloud-2"></div>
    <div class="hill hill-1"></div>
    <div class="hill hill-2"></div>
    <div class="hill hill-3"></div>

    <!-- 인터페이스 및 캐릭터 -->
    <div id="heart-board"><span id="hearts">❤️❤️</span></div>
    <div id="score-board">SCORE: <span id="score">0</span></div>
    
    <div id="kirby">
        <div class="blush blush-left"></div>
        <div class="blush blush-right"></div>
        <div class="feet"></div>
    </div>
    
    <div id="obstacle" class="obstacle ground-obstacle"></div>
    <div id="ground"></div>
    <div id="game-over">
        <h2>G A M E  O V E R</h2>
        <p>스페이스바를 눌러 다시 시작하세요</p>
    </div>
</div>

<script>
    const kirby = document.getElementById("kirby");
    const obstacle = document.getElementById("obstacle");
    const scoreElement = document.getElementById("score");
    const heartsElement = document.getElementById("hearts");
    const gameOverElement = document.getElementById("game-over");

    let isJumping = false;
    let isGameOver = false;
    let score = 0;
    let hearts = 2;
    let gameSpeed = 5;
    let obstaclePosition = 600;
    let gameLoop;

    function jump() {
        if (isJumping || isGameOver) return;
        isJumping = true;
        let jumpHeight = 0;
        
        let upInterval = setInterval(function() {
            if (jumpHeight >= 110) {
                clearInterval(upInterval);
                let downInterval = setInterval(function() {
                    if (jumpHeight <= 0) {
                        clearInterval(downInterval);
                        isJumping = false;
                    }
                    jumpHeight -= 5;
                    kirby.style.bottom = (16 + jumpHeight) + "px";
                }, 12);
            }
            jumpHeight += 6;
            kirby.style.bottom = (16 + jumpHeight) + "px";
        }, 12);
    }

    function respawnObstacle() {
        obstaclePosition = 600 + Math.random() * 150;
        const isAir = Math.random() > 0.5;
        if (isAir) {
            obstacle.className = "obstacle air-obstacle";
        } else {
            obstacle.className = "obstacle ground-obstacle";
        }
    }

    function checkCollision() {
        const kirbyRect = kirby.getBoundingClientRect();
        const obstacleRect = obstacle.getBoundingClientRect();
        const margin = 5; 
        return !(
            kirbyRect.right - margin < obstacleRect.left ||
            kirbyRect.left + margin > obstacleRect.right ||
            kirbyRect.bottom - margin < obstacleRect.top ||
            kirbyRect.top + margin > obstacleRect.bottom
        );
    }

    function updateGame() {
        if (isGameOver) return;

        if (gameSpeed < 16) {
            gameSpeed += 0.003;
        }

        obstaclePosition -= gameSpeed;
        if (obstaclePosition < -40) {
            respawnObstacle();
            score += 10;
            scoreElement.innerText = Math.floor(score);
        }
        obstacle.style.right = (600 - obstaclePosition) + "px";

        if (checkCollision()) {
            hearts--;
            heartsElement.innerText = "❤️".repeat(hearts);
            if (hearts <= 0) {
                endGame();
            } else {
                respawnObstacle();
            }
        }
    }

    function endGame() {
        isGameOver = true;
        gameOverElement.style.display = "block";
        clearInterval(gameLoop);
    }

    function resetGame() {
        isGameOver = false;
        score = 0;
        hearts = 2;
        gameSpeed = 5;
        scoreElement.innerText = score;
        heartsElement.innerText = "❤️❤️";
        gameOverElement.style.display = "none";
        kirby.style.bottom = "16px";
        respawnObstacle();
        gameLoop = setInterval(updateGame, 20);
    }

    document.addEventListener("keydown", function(event) {
        if (event.code === "Space" || event.code === "ArrowUp") {
            event.preventDefault();
            if (isGameOver) {
                resetGame();
            } else {
                jump();
            }
        }
    });

    gameLoop = setInterval(updateGame, 20);
</script>

</body>
</html>"""

# 스트림릿 화면에 HTML 컴포넌트 임베딩
components.html(kirby_game_html, height=250)

st.markdown("---")
st.markdown("""
**🎮 게임 조작 및 규칙:**
- **점프 / 게임 시작**: `Space` 키 또는 `↑` 방향키
- **시간 지남에 따른 가속**: 게임 진행 시간에 따라 난이도가 상승합니다.
- **체력(하트)**: 장애물 충돌 시 하트(❤️)가 1개 차감되며 부활합니다.
- **장애물**: 지상(마리오 버섯), 공중(드래곤) 무작위 등장
""")
