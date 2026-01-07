import streamlit as st
import sympy as sp
import re
import base64

# -----------------------------------------------------------------------------
# 1. Page Configuration & Styling (From app(2).py)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="The Molecular Man - Quadratic Solver",
    page_icon="⚛️",
    layout="centered"
)

# Function to load image and convert to base64 for HTML embedding
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# Get the logo data (Assumes 'logo.png' is in the same folder)
logo_data = get_base64_of_bin_file("logo.png")

# Custom CSS from app(2).py
st.markdown("""
    <style>
    .banner-container {
        background-color: #1e3c72;
        padding: 20px;
        border-radius: 15px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
    }
    
    .text-content {
        text-align: left;
    }
    
    .text-content h1 {
        color: white !important;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
        padding-bottom: 5px;
    }
    
    .text-content p {
        color: #e0e0e0;
        font-size: 1rem;
        margin: 2px 0;
    }
    
    .text-content a {
        color: #ffcc00 !important;
        text-decoration: none;
        font-weight: bold;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border: none;
        height: 3rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #5a6fd6;
        color: white;
    }
    
    .method-box { 
        background-color: #111827; 
        border: 1px solid #374151; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        color: #e5e7eb; 
    }
    
    .question-banner {
        background-color: #e0e7ff; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        margin: 20px 0; 
        color: #1e3a8a;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 600px) {
        .banner-container {
            flex-direction: column;
            text-align: center;
        }
        .text-content {
            text-align: center;
        }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Logic Functions (Expert Math Engine from app.py)
# -----------------------------------------------------------------------------

def clean_input(input_str):
    if not input_str: return "0"
    s = str(input_str)
    # Fix sqrt2 -> sqrt(2)
    s = re.sub(r'sqrt(\d+)', r'sqrt(\1)', s) 
    s = s.replace('^', '**')
    # Implicit multiplication
    s = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', s)
    s = re.sub(r'(\))(\d|[a-zA-Z])', r'\1*\2', s)
    return s

def format_term(coeff, var_part=""):
    """Helper to format terms nicely: 1x -> + x, -1x -> - x"""
    if coeff == 0: return ""
    sign = "+" if coeff > 0 else "-"
    val = sp.simplify(abs(coeff))
    if val == 1 and var_part:
        return f"{sign} {var_part}"
    return f"{sign} {sp.latex(val)}{var_part}"

def solve_quadratic_expert(a_str, b_str, c_str):
    x = sp.Symbol('x')
    
    try:
        a = sp.sympify(clean_input(a_str))
        b = sp.sympify(clean_input(b_str))
        c = sp.sympify(clean_input(c_str))
    except:
        return {'success': False, 'message': "Invalid input syntax."}

    if a == 0: return {'success': False, 'message': "Coefficient 'a' cannot be 0."}

    equation = a*x**2 + b*x + c
    
    # Discriminant & Roots
    delta = sp.simplify(b**2 - 4*a*c)
    try:
        delta_val = float(delta.evalf())
    except:
        delta_val = 1.0 
    
    r1 = (-b + sp.sqrt(delta)) / (2*a)
    r2 = (-b - sp.sqrt(delta)) / (2*a)
    
    r1 = sp.radsimp(sp.simplify(r1))
    r2 = sp.radsimp(sp.simplify(r2))
    
    # Calculate Splitting Terms for Method 1
    t1 = sp.simplify(-a * r1)
    t2 = sp.simplify(-a * r2)
    
    split_found = False
    if sp.simplify(t1 + t2 - b) == 0:
        split_found = True

    return {
        'success': True,
        'a': a, 'b': b, 'c': c,
        'equation': equation,
        'delta': delta,
        'delta_val': delta_val,
        'r1': r1, 'r2': r2,
        't1': t1, 't2': t2,
        'split_found': split_found
    }

# -----------------------------------------------------------------------------
# 3. User Interface
# -----------------------------------------------------------------------------

# --- Banner Construction (From app(2).py) ---
logo_html = f'<img src="data:image/png;base64,{logo_data}" class="logo-img">' if logo_data else '<div style="font-size: 80px;">⚛️</div>'

st.markdown(f"""
    <div class="banner-container">
        {logo_html}
        <div class="text-content">
            <h1>The Molecular Man</h1>
            <p style="font-weight: bold; color: #b3c7ff;">Expert Tuition Solutions Bot</p>
            <p>📞 +91 7339315376</p>
            <p>🌐 <a href="https://tmmtuitions.gitlab.io/" target="_blank">Visit Our Website</a></p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("### 🧮 Quadratic Equation Solver")
st.caption("Solve $ax^2 + bx + c = 0$ instantly showing all steps.")

# --- Inputs Section ---
col1, col2, col3 = st.columns(3)
with col1:
    a_in = st.text_input("a (coeff of x²)", value="sqrt2")
with col2:
    b_in = st.text_input("b (coeff of x)", value="7")
with col3:
    c_in = st.text_input("c (constant)", value="5sqrt2")

if st.button("Solve Equation"):
    result = solve_quadratic_expert(a_in, b_in, c_in)
    
    if result['success']:
        a, b, c = result['a'], result['b'], result['c']
        r1, r2 = result['r1'], result['r2']
        
        # Textbook Question Banner
        st.markdown(f"""
        <div class="question-banner">
             $${sp.latex(result['equation'])} = 0$$
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------------------
        # METHOD 1: FACTORIZATION
        # -----------------------------------------
        st.subheader("Method 1: Solving by Factorization")
        st.markdown('<div class="method-box">', unsafe_allow_html=True)
        
        if result['split_found']:
            t1, t2 = result['t1'], result['t2']
            x = sp.Symbol('x')
            
            st.write(f"We split the middle term ${sp.latex(b)}x$ into **${sp.latex(t1)}x$** and **${sp.latex(t2)}x$**.")
            st.write("This satisfies: sum = $b$ and product = $ac$.")
            
            st.markdown("**Step 1: Write the split terms**")
            st.latex(f"{sp.latex(a)}x^2 {format_term(t1, 'x')} {format_term(t2, 'x')} + {sp.latex(c)} = 0")
            
            st.markdown("**Step 2: Group terms**")
            # Intermediate factors logic
            g1_expr = a*x**2 + t1*x
            g1_factored = sp.factor(g1_expr)
            g2_expr = t2*x + c
            g2_factored = sp.factor(g2_expr)
            
            # Format the second group with a plus sign if needed
            g2_str = sp.latex(g2_factored)
            if t2.evalf() > 0:
                g2_str = f"+ {g2_str}"
            
            st.latex(f"{sp.latex(g1_factored)} {g2_str} = 0")
            
            st.markdown("**Step 3: Factor out the common bracket**")
            final_factored = sp.factor(result['equation'])
            st.latex(f"{sp.latex(final_factored)} = 0")
            
            st.markdown("**Step 4: Final Roots**")
            st.write("Equating factors to zero:")
            
            # Explicit Final Answer for Method 1
            st.success("**Final Answer:**")
            if r1 == r2:
                st.latex(f"x = {sp.latex(r1)}")
            else:
                st.latex(f"x = {sp.latex(r1)}, \\quad x = {sp.latex(r2)}")

        else:
            st.warning("Could not find simple splitting terms for factorization.")
            
        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------------------
        # METHOD 2: QUADRATIC FORMULA
        # -----------------------------------------
        st.subheader("Method 2: Quadratic Formula")
        st.markdown('<div class="method-box">', unsafe_allow_html=True)
        
        st.write("Using formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$")
        st.latex(fr"\Delta = ({sp.latex(b)})^2 - 4({sp.latex(a)})({sp.latex(c)}) = {sp.latex(result['delta'])}")
        
        if result['delta_val'] < 0:
            st.error("Since $\Delta < 0$, there are no real roots.")
        else:
            st.write("Apply Formula:")
            st.latex(fr"x = \frac{{-{sp.latex(b)} \pm \sqrt{{{sp.latex(result['delta'])}}}}}{{2({sp.latex(a)})}}")
            
            st.success("**Final Answer:**")
            if result['delta_val'] == 0:
                 st.latex(f"x = {sp.latex(r1)}")
            else:
                 st.latex(f"x_1 = {sp.latex(r1)}, \\quad x_2 = {sp.latex(r2)}")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error(result['message'])

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>Created by The Molecular Man Expert Tuition Solutions</p>
        <p>Contact: +91 7339315376 | <a href="https://tmmtuitions.gitlab.io/">tmmtuitions.gitlab.io</a></p>
    </div>
""", unsafe_allow_html=True)