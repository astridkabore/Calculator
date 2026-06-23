import streamlit as st
import math

st.set_page_config(page_title="Astrid's Calculator", page_icon="🔢", layout="centered")
st.title("🔢 Astrid's calculator")
st.caption("My first python project")

for key, default in [
    ("display", "0"),
    ("expr", ""),
    ("paren_count", 0),
    ("expression", ""),
    ("waiting", False),
    ("fx_formula", "2*x + 1"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

def fmt(val):
    if isinstance(val, float):
        if val == int(val) and abs(val) < 1e15:
            return str(int(val))
        return str(round(val, 10))
    return str(val)

def nice_expr(raw):
    return (raw
        .replace("**", "^")
        .replace("*", "×")
        .replace("/", "÷")
        .replace("math.pi", "π")
        .replace("math.e", "e"))

def update_display_expr():
    e = st.session_state.expr
    if e:
        st.session_state.expression = nice_expr(e)

def input_digit(d):
    if st.session_state.waiting:
        st.session_state.display = str(d)
        st.session_state.waiting = False
    else:
        st.session_state.display = str(d) if st.session_state.display == "0" else st.session_state.display + str(d)

def input_decimal():
    if st.session_state.waiting:
        st.session_state.display = "0."
        st.session_state.waiting = False
        return
    if "." not in st.session_state.display:
        st.session_state.display += "."

def clear_all():
    st.session_state.display = "0"
    st.session_state.expr = ""
    st.session_state.paren_count = 0
    st.session_state.expression = ""
    st.session_state.waiting = False

def negate():
    val = float(st.session_state.display)
    if val != 0:
        st.session_state.display = fmt(-val)

def percent():
    val = float(st.session_state.display)
    st.session_state.display = fmt(val / 100)

def insert_pi():
    st.session_state.display = fmt(math.pi)
    st.session_state.waiting = False

def apply_unary(fn_raw, fn_nice):
    val_str = st.session_state.display
    try:
        result = fn_raw(float(val_str))
        st.session_state.expression = fn_nice + "(" + val_str + ") ="
        st.session_state.display = fmt(result)
        st.session_state.expr = ""
        st.session_state.waiting = True
    except Exception:
        st.session_state.display = "Error"
        st.session_state.waiting = True

def square():      apply_unary(lambda v: v**2,           "x²")
def cube():        apply_unary(lambda v: v**3,           "x³")
def square_root(): apply_unary(lambda v: math.sqrt(v) if v >= 0 else (_ for _ in ()).throw(ValueError()), "√")
def logarithm():   apply_unary(lambda v: math.log10(v) if v > 0 else (_ for _ in ()).throw(ValueError()), "log")
def natural_log(): apply_unary(lambda v: math.log(v)   if v > 0 else (_ for _ in ()).throw(ValueError()), "ln")
def cosinus():     apply_unary(lambda v: math.cos(math.radians(v)), "cos")
def sinus():       apply_unary(lambda v: math.sin(math.radians(v)), "sin")
def tangente():    apply_unary(lambda v: math.tan(math.radians(v)) if v % 180 != 90 else (_ for _ in ()).throw(ValueError()), "tan")

def evaluate_fx():
    formula = st.session_state.fx_formula
    x = float(st.session_state.display)
    try:
        result = eval(formula, {"__builtins__": {}}, {"x": x, "math": math})
        st.session_state.expression = f"f({fmt(x)}) = {formula} ="
        st.session_state.display = fmt(result)
        st.session_state.expr = ""
        st.session_state.waiting = True
    except Exception:
        st.session_state.display = "Error"
        st.session_state.waiting = True

def compare(op):
    if not st.session_state.waiting:
        st.session_state.expr += st.session_state.display + op
    else:
        st.session_state.expr += op
    st.session_state.display = "0"
    st.session_state.waiting = True
    st.session_state.expression = nice_expr(st.session_state.expr)

def compare_equals():
    full = st.session_state.expr + (st.session_state.display if not st.session_state.waiting else "")
    try:
        result = eval(full, {"__builtins__": {}}, {"math": math})
        st.session_state.expression = nice_expr(full) + " ="
        st.session_state.display = str(result)
    except Exception:
        st.session_state.display = "Error"
    st.session_state.expr = ""
    st.session_state.paren_count = 0
    st.session_state.waiting = True

OP_MAP = {"+": "+", "-": "-", "*": "×", "/": "÷", "**": "^"}

def set_operator(op):
    if not st.session_state.waiting:
        st.session_state.expr += st.session_state.display + op
    else:
        for raw_op in ["**", "*", "/", "+", "-"]:
            if st.session_state.expr.endswith(raw_op):
                st.session_state.expr = st.session_state.expr[:-len(raw_op)] + op
                break
        else:
            st.session_state.expr += op
    st.session_state.display = "0"
    st.session_state.waiting = True
    update_display_expr()

def open_paren():
    if not st.session_state.waiting and st.session_state.display != "0":
        st.session_state.expr += st.session_state.display + "*("
    else:
        st.session_state.expr += "("
    st.session_state.paren_count += 1
    st.session_state.display = "0"
    st.session_state.waiting = False
    update_display_expr()

def close_paren():
    if st.session_state.paren_count > 0:
        st.session_state.expr += st.session_state.display + ")"
        st.session_state.paren_count -= 1
        update_display_expr()
        try:
            result = eval(st.session_state.expr, {"__builtins__": {}}, {"math": math})
            st.session_state.display = fmt(result)
        except Exception:
            pass
        st.session_state.waiting = True

def equals():
    full = st.session_state.expr + (st.session_state.display if not st.session_state.waiting else "")
    if not full:
        return
    try:
        result = eval(full, {"__builtins__": {}}, {"math": math})
        st.session_state.expression = nice_expr(full) + " ="
        st.session_state.display = fmt(result)
    except Exception:
        st.session_state.expression = nice_expr(full) + " ="
        st.session_state.display = "Error"
    st.session_state.expr = ""
    st.session_state.paren_count = 0
    st.session_state.waiting = True

expr_text = st.session_state.expression if st.session_state.expression else "\u00a0"
st.markdown(f"""
<div style="background:#e91e8c;border-radius:12px;padding:16px 20px;margin-bottom:16px;min-height:90px;text-align:right;">
    <div style="color:#ffd6eb;font-size:14px;min-height:20px;">{expr_text}</div>
    <div style="color:white;font-size:48px;font-weight:300;line-height:1.2;word-break:break-all;">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    if st.button("AC",  use_container_width=True, key="clear"): clear_all(); st.rerun()
with c2:
    if st.button("+/-", use_container_width=True, key="neg"):   negate();    st.rerun()
with c3:
    if st.button("%",   use_container_width=True, key="pct"):   percent();   st.rerun()
with c4:
    if st.button("x²",  use_container_width=True, key="sq"):    square();    st.rerun()
with c5:
    if st.button("x³",  use_container_width=True, key="cb"):    cube();      st.rerun()
with c6:
    if st.button("√",   use_container_width=True, key="sqrt"):  square_root(); st.rerun()
with c7:
    if st.button("÷",   use_container_width=True, key="div"):   set_operator("/"); st.rerun()

c8, c9, c10, c11, c12 = st.columns(5)
with c8:
    if st.button("log", use_container_width=True, key="log"):   logarithm();   st.rerun()
with c9:
    if st.button("ln",  use_container_width=True, key="ln"):    natural_log(); st.rerun()
with c10:
    if st.button("cos", use_container_width=True, key="cos"):   cosinus();     st.rerun()
with c11:
    if st.button("sin", use_container_width=True, key="sin"):   sinus();       st.rerun()
with c12:
    if st.button("tan", use_container_width=True, key="tan"):   tangente();    st.rerun()

c13, c14, c15, c16, c17, c18 = st.columns(6)
with c13:
    if st.button("π",   use_container_width=True, key="pi"):    insert_pi();        st.rerun()
with c14:
    if st.button("xʸ",  use_container_width=True, key="pow"):   set_operator("**"); st.rerun()
with c15:
    if st.button("(",   use_container_width=True, key="lparen"): open_paren();       st.rerun()
with c16:
    if st.button(")",   use_container_width=True, key="rparen"): close_paren();      st.rerun()
with c17:
    if st.button("<",   use_container_width=True, key="lt"):    compare("<");        st.rerun()
with c18:
    if st.button(">",   use_container_width=True, key="gt"):    compare(">");        st.rerun()

cX1, cX2 = st.columns([3, 1])
with cX1:
    st.session_state.fx_formula = st.text_input(
        "f(x) formula",
        value=st.session_state.fx_formula,
        placeholder="e.g. 2*x + 1",
        label_visibility="collapsed"
    )
with cX2:
    if st.button("f(x)", use_container_width=True, key="fx"):
        evaluate_fx(); st.rerun()

r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1:
    if st.button("7", use_container_width=True, key="7"): input_digit(7); st.rerun()
with r1c2:
    if st.button("8", use_container_width=True, key="8"): input_digit(8); st.rerun()
with r1c3:
    if st.button("9", use_container_width=True, key="9"): input_digit(9); st.rerun()
with r1c4:
    if st.button("−", use_container_width=True, key="sub"): set_operator("-"); st.rerun()

r2c1, r2c2, r2c3, r2c4 = st.columns(4)
with r2c1:
    if st.button("4", use_container_width=True, key="4"): input_digit(4); st.rerun()
with r2c2:
    if st.button("5", use_container_width=True, key="5"): input_digit(5); st.rerun()
with r2c3:
    if st.button("6", use_container_width=True, key="6"): input_digit(6); st.rerun()
with r2c4:
    if st.button("+", use_container_width=True, key="add"): set_operator("+"); st.rerun()

r3c1, r3c2, r3c3, r3c4 = st.columns(4)
with r3c1:
    if st.button("1", use_container_width=True, key="1"): input_digit(1); st.rerun()
with r3c2:
    if st.button("2", use_container_width=True, key="2"): input_digit(2); st.rerun()
with r3c3:
    if st.button("3", use_container_width=True, key="3"): input_digit(3); st.rerun()
with r3c4:
    if st.button("=", use_container_width=True, key="eq"): equals(); st.rerun()

r4c1, r4c2 = st.columns([2, 1])
with r4c1:
    if st.button("0", use_container_width=True, key="0"): input_digit(0); st.rerun()
with r4c2:
    if st.button(".", use_container_width=True, key="dot"): input_decimal(); st.rerun()

st.divider()
st.markdown("**How to use:** Enter numbers and tap an operator (+, −, ×, ÷), then tap another number and press **=** to see the result. Use **(  )** to group expressions, **π** for pi, and **xʸ** to raise to any power.")
st.markdown("<p style='text-align:center; color:#e91e8c; font-weight:600; margin-top:16px;'>Made by Astrid 🩷</p>", unsafe_allow_html=True)
