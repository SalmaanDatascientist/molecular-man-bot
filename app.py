import streamlit as st
import math

# -----------------------------------------------------------------------------
# 1. Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="The Molecular Man - Quadratic Solver",
    page_icon="⚛️",
    layout="centered"
)

# Custom CSS to match your original Tkinter blue branding (#1e3c72)
st.markdown("""
    <style>
    .main-header {
        background-color: #1e3c72;
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        font-family: Arial;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .main-header p {
        color: #e0e0e0;
        font-size: 1.2rem;
        margin-top: 5px;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border: none;
        height: 3rem;
    }
    .stButton>button:hover {
        background-color: #5a6fd6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Logic Functions (Directly from your code)
# -----------------------------------------------------------------------------

def find_factors(a, b, c):
    """Find two numbers that sum to b and multiply to a*c"""
    product = int(a * c)
    sum_val = b
    
    # Avoid huge loops if numbers are massive
    limit = abs(product) + 1
    if limit > 10000: limit = 10000 

    for i in range(-limit, limit):
        if i != 0 and product % i == 0:
            j = product // i
            if i + j == sum_val:
                return [i, j]
    return None

def solve_by_factorization(a, b, c):
    factors = find_factors(a, b, c)
    product = a * c
    
    if not factors:
        return {
            'success': False,
            'message': 'Cannot be easily factorized with integers.'
        }
    
    p, q = factors
    # Calculate roots
    discriminant = b * b - 4 * a * c
    # Check for negative discriminant to avoid math domain error in factorization check
    if discriminant < 0:
         return {'success': False, 'message': 'No real roots.'}

    x1 = (-b + math.sqrt(discriminant)) / (2 * a)
    x2 = (-b - math.sqrt(discriminant)) / (2 * a)
    
    steps = [
        f"**Given equation:** {a}x² {'+' if b >= 0 else ''}{b}x {'+' if c >= 0 else ''}{c} = 0",
        f"We need two numbers that add up to **{b}** and multiply to **{product}**.",
        f"Those numbers are **{p}** and **{q}**.",
        f"Split the middle term: {a}x² {'+' if p >= 0 else ''}{p}x {'+' if q >= 0 else ''}{q}x {'+' if c >= 0 else ''}{c} = 0"
    ]
    
    return {
        'success': True,
        'steps': steps,
        'roots': [x1, x2]
    }

def solve_by_formula(a, b, c):
    discriminant = b * b - 4 * a * c
    
    steps = [
        "**Using the quadratic formula:** $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$",
        f"Substituting values: a = {a}, b = {b}, c = {c}",
        f"Calculate discriminant: $\\Delta = b^2 - 4ac = ({b})^2 - 4({a})({c}) = {discriminant}$"
    ]
    
    if discriminant < 0:
        steps.append("Since discriminant is negative, there are **no real roots**.")
        return {
            'success': False,
            'steps': steps,
            'message': 'No real roots (discriminant < 0)'
        }
    
    sqrt_d = math.sqrt(discriminant)
    steps.append(f"$\\sqrt{{\\Delta}} = \\sqrt{{{discriminant}}} = {sqrt_d:.4f}$")
    
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    
    steps.append(f"$x_1 = \\frac{{-{b} + {sqrt_d:.4f}}}{{2 \\times {a}}} = {x1:.4f}$")
    steps.append(f"$x_2 = \\frac{{-{b} - {sqrt_d:.4f}}}{{2 \\times {a}}} = {x2:.4f}$")
    
    return {
        'success': True,
        'steps': steps,
        'roots': [x1, x2]
    }

# -----------------------------------------------------------------------------
# 3. User Interface
# -----------------------------------------------------------------------------

# --- Banner ---
st.markdown("""
    <div class="main-header">
        <div style="font-size: 3rem;">⚛️</div>
        <h1>Welcome to The Molecular Man</h1>
        <p>Expert Tuition Solutions Bot</p>
    </div>
""", unsafe_allow_html=True)

st.write("### 🧮 Quadratic Equation Solver")
st.caption("Solve $ax^2 + bx + c = 0$ instantly showing all steps.")

# --- Inputs Section ---
col1, col2, col3 = st.columns(3)

with col1:
    a = st.number_input("a (coeff of x²)", value=1.0, step=1.0, format="%g")
with col2:
    b = st.number_input("b (coeff of x)", value=5.0, step=1.0, format="%g")
with col3:
    c = st.number_input("c (constant)", value=6.0, step=1.0, format="%g")

# --- Dynamic Equation Display ---
# Streamlit updates this automatically whenever inputs change!
if a != 0:
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
        <h3 style="color: #667eea; margin:0;">
            {a}x² {'+' if b >= 0 else ''}{b}x {'+' if c >= 0 else ''}{c} = 0
        </h3>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("Error: Coefficient 'a' cannot be zero for a quadratic equation.")

# --- Solve Button ---
if st.button("Solve Equation") and a != 0:
    
    st.markdown("---")
    
    # METHOD 1: FACTORIZATION
    st.subheader("Method 1: Solving by Factorization")
    
    factor_result = solve_by_factorization(a, b, c)
    
    if factor_result['success']:
        for step in factor_result['steps']:
            st.write(f"- {step}")
        st.success(f"**Roots:** x₁ = {factor_result['roots'][0]:.4f}, x₂ = {factor_result['roots'][1]:.4f}")
    else:
        st.warning(f"⚠️ {factor_result['message']} (Try the formula method below)")

    st.markdown("---")

    # METHOD 2: FORMULA
    st.subheader("Method 2: Quadratic Formula")
    
    formula_result = solve_by_formula(a, b, c)
    
    for step in formula_result['steps']:
        st.write(f"- {step}")
        
    if formula_result['success']:
        st.success(f"**Roots:** x₁ = {formula_result['roots'][0]:.4f}, x₂ = {formula_result['roots'][1]:.4f}")
    else:
        st.error(formula_result['message'])

# --- Footer ---
st.markdown("---")
st.markdown("*Created by The Molecular Man Expert Tuition Solutions*")