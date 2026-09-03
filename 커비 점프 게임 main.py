<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>커비 점프 게임 (Kirby Jump Deluxe)</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 400px;
            overflow: hidden;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            background: linear-gradient(to bottom, #87CEEB, #E0F6FF);
            transition: background 2s ease;
        }

        /* 배경 테마 설정 */
        #game-container.sunset {
            background: linear-gradient(to bottom, #FD5E53, #FFC0CB);
        }

        #game-container.night {
            background: linear-gradient(to bottom, #0F2027, #203A43);
        }

        /* 바닥 땅 */
        #ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 60px;
            background: #5c940d;
            border-top: 6px solid #82c91e;
        }

        /* 커비 캐릭터 */
        #kirby {
            position: absolute;
            bottom: 60px;
            left: 80px;
            width: 50px;
            height: 50px;
            background-color: #ff9ebb;
            border: 3px solid #ff4081;
            border-radius: 50%;
            transition: height 0.1s, border-radius 0.1s;
        }

        /* 커비 눈 & 볼터치 디자인 */
        #kirby::before {
            content: '';
            position: absolute;
            top: 12px;
            left: 28px;
            width: 6px;
            height: 12px;
            background: #000;
            border-radius: 50%;
            box-shadow: -14px 0 0 #000;
        }

        #kirby::after {
            content: '';
            position: absolute;
            top: 24px;
            left: 32px;
            width: 8px;
            height: 6px;
            background: #ff1744;
            border-radius: 50%;
            box-shadow: -22px 0 0 #ff1744;
        }

        /* 커비 상태 연출 */
        .duck {
            height: 30px !important;
            border-radius: 20px !important;
        }

        .invincible {
            animation: rainbow 0.2s infinite;
        }

        .blink {
            opacity: 0.4;
        }

        @keyframes rainbow {
            0% { background-color: #ff9ebb; }
            33% { background-color: #fff176; }
            66% { background-color: #81d4fa; }
            100% { background-color: #ff9ebb; }
        }

        /* 장애물 & 아이템 공통 */
        .entity {
            position: absolute;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
        }

        .obstacle-ground {
            bottom: 60px;
            width: 35px;
            height: 45px;
            background-color: #795548;
            border-radius: 8px 8px 0 0;
        }

        .obstacle-air {
            bottom: 130px;
            width: 40px;
            height: 30px;
            background-color: #d32f2f;
            border-radius: 50%;
        }

        .item-candy {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #ff4081;
        }

        .item-star {
            width: 35px;
            height: 35px;
        }

        /* HUD 및 안내 화면 */
        #hud {
            position: absolute;
            top: 15px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
            z-index: 10;
        }

        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }

        #overlay h1 {
            font-size: 42px;
            color: #ff9ebb;
            margin-bottom: 15px;
            text-shadow: 2px 2px 5px #000;
        }

        #overlay p {
            font-size: 18px;
            margin-bottom: 25px;
            line-height: 1.6;
            text-align: center;
        }

        .btn {
            padding: 12px 30px;
            font-size: 20px;
            font-weight: bold;
            background-color: #ff4081;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: transform 0.1s, background-color 0.2s;
        }

        .btn:hover {
            transform: scale(1.05);
            background-color: #f50057;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="hud">
            <div>체력: <span id="lives">❤️❤️❤️</span></div>
            <div>점수: <span id="score">0</span> | 최고: <span id="high-score">0</span></div>
        </div>

        <div id="kirby"></div>
        <div id="ground"></div>

        <div id="overlay">
            <h1 id="overlay-title">커비 점프 디럭스</h1>
            <p id="overlay-desc">
                [Space] / [↑] : 점프 (공중 2단 점프 가능)<br>
                [↓] : 엎드리기 (공중 장애물 회피)
            </p>
            <button class="btn" id="start-btn" onclick="startGame()">게임 시작</button>
        </div>
    </div>

    <script>
        // Web Audio API 안전하게 초기화
        let audioCtx = null;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        }

        function playSound(type) {
            if (!audioCtx) return;

            try {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);

                const now = audioCtx.currentTime;

                if (type === 'jump') {
                    osc.frequency.setValueAtTime(300, now);
                    osc.frequency.exponentialRampToValueAtTime(600, now + 0.15);
                    gain.gain.setValueAtTime(0.2, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
                    osc.start(now);
                    osc.stop(now + 0.15);
                } else if (type === 'item') {
                    osc.frequency.setValueAtTime(523, now);
                    osc.frequency.setValueAtTime(659, now + 0.08);
                    osc.frequency.setValueAtTime(783, now + 0.16);
                    gain.gain.setValueAtTime(0.2, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
                    osc.start(now);
                    osc.stop(now + 0.25);
                } else if (type === 'hit') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, now);
                    osc.frequency.linearRampToValueAtTime(60, now + 0.2);
                    gain.gain.setValueAtTime(0.3, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
                    osc.start(now);
                    osc.stop(now + 0.2);
                }
            } catch (e) {
                console.warn("오디오 재생 실패:", e);
            }
        }

        // 게임 요소 선택
        const container = document.getElementById('game-container');
        const kirby = document.getElementById('kirby');
        const livesEl = document.getElementById('lives');
        const scoreEl = document.getElementById('score');
        const highScoreEl = document.getElementById('high-score');
        const overlay = document.getElementById('overlay');
        const overlayTitle = document.getElementById('overlay-title');
        const overlayDesc = document.getElementById('overlay-desc');

        // 게임 변수
        let isPlaying = false;
        let score = 0;
        let highScore = localStorage.getItem('kirby_high_score') || 0;
        highScoreEl.textContent = highScore;

        let lives = 3;
        let positionY = 0;
        let velocityY = 0;
        let gravity = 0.8;
        let jumpCount = 0;
        let isDucking = false;
        let isInvincible = false;
        let isBlinking = false;

        let entities = [];
        let gameLoopId = null;
        let spawnTimer = 0;

        // 키 상태 제어
        const keys = {};

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.code === 'ArrowUp') {
                e.preventDefault();
                if (isPlaying && jumpCount < 2 && !e.repeat) {
                    velocityY = 13;
                    jumpCount++;
                    playSound('jump');
                }
            }
            if (e.code === 'ArrowDown') {
                e.preventDefault();
                keys['ArrowDown'] = true;
            }
        });

        window.addEventListener('keyup', (e) => {
            if (e.code === 'ArrowDown') {
                keys['ArrowDown'] = false;
            }
        });

        function startGame() {
            initAudio(); // 브라우저 차단 정책 해제를 위해 버튼 클릭 시 오디오 활성화

            // 이전 애니메이션 루프 종료
            if (gameLoopId) cancelAnimationFrame(gameLoopId);

            // 데이터 초기화
            isPlaying = true;
            score = 0;
            lives = 3;
            positionY = 0;
            velocityY = 0;
            jumpCount = 0;
            isInvincible = false;
            isBlinking = false;
            
            entities.forEach(e => e.el.remove());
            entities = [];

            updateHUD();
            overlay.style.display = 'none';

            gameLoop();
        }

        function gameLoop() {
            if (!isPlaying) return;

            // 1. 커비 물리엔진 및 동작
            if (keys['ArrowDown'] && positionY === 0) {
                isDucking = true;
                kirby.classList.add('duck');
            } else {
                isDucking = false;
                kirby.classList.remove('duck');
            }

            velocityY -= gravity;
            positionY += velocityY;

            if (positionY <= 0) {
                positionY = 0;
                velocityY = 0;
                jumpCount = 0;
            }

            kirby.style.bottom = (60 + positionY) + 'px';

            // 2. 점수 증가 및 테마 스타일 변경
            score++;
            scoreEl.textContent = score;

            if (score > 1000) {
                container.className = 'night';
            } else if (score > 500) {
                container.className = 'sunset';
            } else {
                container.className = '';
            }

            // 3. 엔티티(장애물/아이템) 생성
            spawnTimer++;
            if (spawnTimer > 80 + Math.random() * 60) {
                spawnEntity();
                spawnTimer = 0;
            }

            // 4. 엔티티 이동 및 충돌 체크
            const kirbyRect = kirby.getBoundingClientRect();

            for (let i = entities.length - 1; i >= 0; i--) {
                const ent = entities[i];
                ent.x -= ent.speed;
                ent.el.style.left = ent.x + 'px';

                const entRect = ent.el.getBoundingClientRect();

                // 충돌 히트박스 보정
                const isColliding = !(
                    kirbyRect.right - 10 < entRect.left ||
                    kirbyRect.left + 10 > entRect.right ||
                    kirbyRect.bottom - 5 < entRect.top ||
                    kirbyRect.top + 5 > entRect.bottom
                );

                if (isColliding) {
                    if (ent.type === 'candy') {
                        score += 100;
                        playSound('item');
                        ent.el.remove();
                        entities.splice(i, 1);
                        continue;
                    } else if (ent.type === 'star') {
                        setInvincible(5000);
                        playSound('item');
                        ent.el.remove();
                        entities.splice(i, 1);
                        continue;
                    } else if (ent.type === 'obstacle') {
                        if (!isInvincible && !isBlinking) {
                            handleHit();
                        }
                    }
                }

                // 화면 왼쪽 밖으로 빠져나간 객체 삭제
                if (ent.x < -50) {
                    ent.el.remove();
                    entities.splice(i, 1);
                }
            }

            gameLoopId = requestAnimationFrame(gameLoop);
        }

        function spawnEntity() {
            const rand = Math.random();
            const el = document.createElement('div');
            el.className = 'entity';

            let type = 'obstacle';
            let speed = 6 + Math.min(score / 300, 6);

            if (rand < 0.4) {
                el.classList.add('obstacle-ground');
                el.textContent = '🌵';
            } else if (rand < 0.7) {
                el.classList.add('obstacle-air');
                el.textContent = '🦇';
            } else if (rand < 0.88) {
                type = 'candy';
                el.classList.add('item-candy');
                el.style.bottom = (80 + Math.random() * 80) + 'px';
                el.textContent = '🍬';
            } else {
                type = 'star';
                el.classList.add('item-star');
                el.style.bottom = (100 + Math.random() * 60) + 'px';
                el.textContent = '⭐';
            }

            el.style.left = '800px';
            container.appendChild(el);

            entities.push({ el, x: 800, speed, type });
        }

        function setInvincible(duration) {
            isInvincible = true;
            kirby.classList.add('invincible');
            setTimeout(() => {
                isInvincible = false;
                kirby.classList.remove('invincible');
            }, duration);
        }

        function handleHit() {
            lives--;
            playSound('hit');
            updateHUD();

            if (lives <= 0) {
                gameOver();
            } else {
                isBlinking = true;
                kirby.classList.add('blink');
                setTimeout(() => {
                    isBlinking = false;
                    kirby.classList.remove('blink');
                }, 1500);
            }
        }

        function updateHUD() {
            livesEl.textContent = '❤️'.repeat(Math.max(0, lives));
        }

        function gameOver() {
            isPlaying = false;
            if (gameLoopId) cancelAnimationFrame(gameLoopId);

            if (score > highScore) {
                highScore = score;
                localStorage.setItem('kirby_high_score', highScore);
                highScoreEl.textContent = highScore;
            }

            overlayTitle.textContent = '게임 오버!';
            overlayDesc.innerHTML = `최종 점수: <b>${score}</b>점<br>최고 점수: <b>${highScore}</b>점`;
            document.getElementById('start-btn').textContent = '다시 시작';
            overlay.style.display = 'flex';
        }
    </script>
</body>
</html>
