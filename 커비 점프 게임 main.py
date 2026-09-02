import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="스트림릿 커비 점프 게임",
    page_icon="⭐",
    layout="centered"
)

st.title("⭐ 커비 점프 게임 (수정 버전)")
st.caption("스페이스바(Space) 또는 위쪽 화살표(↑) 키를 눌러 점프하세요!")

# HTML/JS 기반 커비 게임 코드
kirby_game_html = """
<!DOCTYPE html>
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
        #game-container {
            position: relative;
            width: 600px;
            height: 200px;
            background-color: #fff;
            border: 2px solid #535353;
            overflow: hidden;
            border-radius: 8px;
        }
        
        /* --- 커비(Kirby) 디자인 --- */
        #kirby {
            position: absolute;
            bottom: 10px;
            left: 50px;
            width: 40px;
            height: 40px;
            background-color: #ffb6c1; /* 핑크색 몸통 */
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
        }
        
        /* 지상 장애물 (버섯) */
        .ground-obstacle {
            bottom: 10px;
            width: 30px;
            height: 30px;
            background-color: #f00; /* 빨간색 갓 */
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
            background-color: #fff; /* 흰색 기둥 */
            border: 2px solid #ccc;
            border-radius: 2px;
        }
        .ground-obstacle::before {
            content: '';
            position: absolute;
            top: 5px;
            left: 7
