import streamlit as st

st.set_page_config(page_title="Python Calculator", page_icon="🔢", layout="centered")

st.title("🔢 Astrid's calculator")
st.caption("My first python project")

if "display" not in st.session_state:
    st.session_state.display = "0"
if "prev" not in st.session_state:
    st.session_state.prev = None
if "operator" not in st.session_state:
    st.session_state.operator = None
if "waiting" not in st.session_state:
    st.session_state.waiting = False
if "expression" not in st.session_state:
    st.session_state.expression = ""

def input_digit(d):
    if st.session_state.waiting:
        st.session_state.display = str(d)
        st.session_state.waiting = False
    else:
        if st.session_state.display == "0":
            st.session_state.display = str(d)
        else:
            st.session_state.display += str(d)

def input_decimal():
    if st.session_state.waiting:
        st.session_state.display = "0."
        st.session_state.waiting = False
        return
    if "." not in st.session_state.display:
        st.session_state.display += "."

def clear_all():
    st.session_state.display = "0"
    st.session_state.prev = None
    st.session_state.operator = None
    st.session_state.waiting = False
    st.session_state.expression = ""

def negate():
    val = float(st.session_state.display)
    if val != 0:
        result = -val
        st.session_state.display = str(int(result)) if result == int(result) else str(result)

def percent():
    val = float(st.session_state.display)
    result = val / 100
    st.session_state.display = str(int(result)) if result == int(result) else str(result)

def square():
    val = float(st.session_state.display)
    result = val ** 2
    st.session_state.expression = str(st.session_state.display) + "² ="
    st.session_state.display = str(int(result)) if result == int(result) else str(result)
    st.session_state.waiting = True

OP_LABELS = {"+": "+", "-": "−", "*": "×", "/": "÷"}

def calculate(a, b, op):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return None if b == 0 else a / b
    return b

def set_operator(op):
    current = float(st.session_state.display)
    if st.session_state.prev is not None and st.session_state.operator and not st.session_state.waiting:
        result = calculate(float(st.session_state.prev), current, st.session_state.operator)
        if result is None:
            st.session_state.display = "Error"
            st.session_state.prev = None
            st.session_state.operator = None
            st.session_state.expression = ""
            st.session_state.waiting = True
            return
        r = int(result) if result == int(result) else result
        st.session_state.display = str(r)
        st.session_state.prev = str(r)
        st.session_state.expression = str(r) + " " + OP_LABELS[op]
    else:
        st.session_state.prev = st.session_state.display
        st.session_state.expression = st.session_state.display + " " + OP_LABELS[op]
    st.session_state.operator = op
    st.session_state.waiting = True

def equals():
    if st.session_state.prev is None or st.session_state.operator is None:
        return
    current = float(st.session_state.display)
    prev_val = float(st.session_state.prev)
    result = calculate(prev_val, current, st.session_state.operator)
    if result is None:
        st.session_state.expression = st.session_state.prev + " " + OP_LABELS[st.session_state.operator] + " " + st.session_state.display + " ="
        st.session_state.display = "Error"
    else:
        r = int(result) if result == int(result) else result
        st.session_state.expression = st.session_state.prev + " " + OP_LABELS[st.session_state.operator] + " " + st.session_state.display + " ="
        st.session_state.display = str(r)
    st.session_state.prev = None
    st.session_state.operator = None
    st.session_state.waiting = True

expr_text = st.session_state.expression if st.session_state.expression else " "
st.markdown(f"""
<div style="background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;min-height:90px;text-align:right;">
    <div style="color:#64748b;font-size:14px;min-height:20px;">{expr_text}</div>
    <div style="color:white;font-size:48px;font-weight:300;line-height:1.2;word-break:break-all;">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("AC", use_container_width=True, key="clear"):
        clear_all()
        st.rerun()
with col2:
    if st.button("+/-", use_container_width=True, key="neg"):
        negate()
        st.rerun()
with col3:
    if st.button("%", use_container_width=True, key="pct"):
        percent()
        st.rerun()
with col4:
    if st.button("x²", use_container_width=True, key="sq"):
        square()
        st.rerun()
with col5:
    if st.button("÷", use_container_width=True, key="div"):
        set_operator("/")
        st.rerun()

colA, colB, colC, colD = st.columns(4)
with colA:
    if st.button("7", use_container_width=True, key="7"):
        input_digit(7); st.rerun()
with colB:
    if st.button("8", use_container_width=True, key="8"):
        input_digit(8); st.rerun()
with colC:
    if st.button("9", use_container_width=True, key="9"):
        input_digit(9); st.rerun()
with colD:
    if st.button("×", use_container_width=True, key="mul"):
        set_operator("*"); st.rerun()

col9, col10, col11, col12 = st.columns(4)
with col9:
    if st.button("4", use_container_width=True, key="4"):
        input_digit(4); st.rerun()
with col10:
    if st.button("5", use_container_width=True, key="5"):
        input_digit(5); st.rerun()
with col11:
    if st.button("6", use_container_width=True, key="6"):
        input_digit(6); st.rerun()
with col12:
    if st.button("−", use_container_width=True, key="sub"):
        set_operator("-"); st.rerun()

col13, col14, col15, col16 = st.columns(4)
with col13:
    if st.button("1", use_container_width=True, key="1"):
        input_digit(1); st.rerun()
with col14:
    if st.button("2", use_container_width=True, key="2"):
        input_digit(2); st.rerun()
with col15:
    if st.button("3", use_container_width=True, key="3"):
        input_digit(3); st.rerun()
with col16:
    if st.button("+", use_container_width=True, key="add"):
        set_operator("+"); st.rerun()

col17, col18, col19 = st.columns([2, 1, 1])
with col17:
    if st.button("0", use_container_width=True, key="0"):
        input_digit(0); st.rerun()
with col18:
    if st.button(".", use_container_width=True, key="dot"):
        input_decimal(); st.rerun()
with col19:
    if st.button("=", use_container_width=True, key="eq"):
        equals(); st.rerun()

st.divider()
st.markdown("**How to use:** Enter numbers and tap an operator (+, −, ×, ÷), then tap another number and press **=** to see the result.")
