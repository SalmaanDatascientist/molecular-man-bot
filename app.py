import streamlit as st
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

# Page configuration
st.set_page_config(
    page_title="Quadratic Equation Solver ",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
    }
    .equation-display {
        background-color: #f0f0f0;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .info-text {
        color: #ffd700;
        font-size: 16px;
        font-style: italic;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
col1, col2 = st.columns([1, 4])

with col1:
    try:
        st.image("logo.png", width=150)
    except:
        st.write("🧮")

with col2:
    st.markdown("""
        <div style="padding: 10px;">
            <div style="font-size: 42px; font-weight: bold; color: white;">The Molecular Man</div>
            <div style="font-size: 18px; color: #e0e0e0; margin: 5px 0;">Expert Tuition Solutions Bot</div>
            <div style="font-size: 16px; color: white; margin: 5px 0;">📞 +91 7339315376</div>
            <div style="font-size: 16px; color: white; margin: 5px 0;">🌐 <a href="https://the-molecularman-expert-tuitions.streamlit.app/" target="_blank" style="color: #ffd700;">Visit Our Website</a></div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.title("🧮 Quadratic Equation Solver")
st.caption("Solve ax² + bx + c = 0 with complete step-by-step solutions")

# Input section
st.markdown('<p class="info-text">💡 You can use expressions like: 3, -2*sqrt(6), sqrt(2), 5/2, etc.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**a (coeff of x²)**")
    a_input = st.text_input("a", value="1", key="a", label_visibility="collapsed")

with col2:
    st.markdown("**b (coeff of x)**")
    b_input = st.text_input("b", value="-5", key="b", label_visibility="collapsed")

with col3:
    st.markdown("**c (constant)**")
    c_input = st.text_input("c", value="6", key="c", label_visibility="collapsed")

# Parse inputs
try:
    x = symbols('x')
    a = parse_expr(a_input)
    b = parse_expr(b_input)
    c = parse_expr(c_input)
    
    equation = a*x**2 + b*x + c
    st.markdown('<div class="equation-display"></div>', unsafe_allow_html=True)
    st.latex(f"{latex(equation)} = 0")
    
except Exception as e:
    st.error(f"Error parsing input: {str(e)}")
    st.stop()

# Solve button
if st.button("Solve Equation", type="primary", use_container_width=True):
    try:
        if a == 0:
            st.error("Coefficient 'a' cannot be zero for a quadratic equation!")
        else:
            st.markdown("---")
            
            # Get roots FIRST
            roots = solve(equation, x)
            unique_roots = list(set([simplify(r) for r in roots]))
            discriminant = simplify(b**2 - 4*a*c)
            
            # ========== METHOD 1: SPLITTING MIDDLE TERM ==========
            st.markdown("## 📗 Method 1: Splitting the Middle Term")
            
            with st.container():
                st.markdown("""<div style='background-color: white; padding: 40px; border-radius: 10px; color: black;'>""", unsafe_allow_html=True)
                
                st.markdown(f"### Example: Find the roots of the quadratic equation")
                st.latex(f"{latex(equation)} = 0")
                
                st.markdown("### Solution:")
                
                # Calculate product a*c
                ac_product = expand(a * c)
                
                st.write("**Step 1:** For the equation")
                st.latex(f"{latex(a)}x^2 + ({latex(b)})x + {latex(c)} = 0")
                
                st.write("**Step 2:** Find two numbers whose product = a × c and sum = b")
                
                st.write("Product:")
                st.latex(f"{latex(a)} \\times {latex(c)} = {latex(ac_product)}")
                
                st.write("Sum:")
                st.latex(f"{latex(b)}")
                
                # Step 3: Split the middle term based on actual roots
                st.write("**Step 3:** Split the middle term:")
                st.write("We need to find two numbers that:")
                st.write("• Multiply to give a × c")
                st.write("• Add up to give b")
                
                if len(unique_roots) == 2:
                    # Two different roots
                    r1, r2 = unique_roots[0], unique_roots[1]
                    # For (x - r1)(x - r2) = x² - (r1+r2)x + r1*r2
                    # So b = -(r1+r2)*a, split as -r1*a and -r2*a
                    b_part1 = -r1 * a
                    b_part2 = -r2 * a
                    st.latex(f"= {latex(a)}x^2 + ({latex(b_part1)})x + ({latex(b_part2)})x + {latex(c)}")
                elif len(unique_roots) == 1:
                    # Repeated root - split b into two equal parts
                    b_half = b / 2
                    st.write(f"The two numbers are both {latex(b_half)}")
                    st.latex(f"= {latex(a)}x^2 + ({latex(b_half)})x + ({latex(b_half)})x + {latex(c)}")
                
                # Step 4: Group
                st.write("**Step 4:** Group the terms:")
                if len(unique_roots) == 2:
                    r1, r2 = unique_roots[0], unique_roots[1]
                    b_part1 = -r1 * a
                    b_part2 = -r2 * a
                    term1 = a*x**2 + b_part1*x
                    term2 = b_part2*x + c
                    st.latex(f"= ({latex(term1)}) + ({latex(term2)})")
                else:
                    b_half = b / 2
                    term1 = a*x**2 + b_half*x
                    term2 = b_half*x + c
                    st.latex(f"= ({latex(term1)}) + ({latex(term2)})")
                
                # Step 5: Factor each group - DETAILED
                st.write("**Step 5:** Factor out common terms from each group:")
                
                if a == 1:
                    # Simple case: x² - 5x + 6
                    if len(unique_roots) == 2:
                        r1, r2 = unique_roots[0], unique_roots[1]
                        st.latex(f"= x(x - {latex(r1)}) - {latex(r2)}(x - {latex(r1)})")
                    else:
                        r = unique_roots[0]
                        st.latex(f"= x(x - {latex(r)}) - {latex(r)}(x - {latex(r)})")
                else:
                    # Complex case: 3x² - 2√6x + 2
                    # Need to show the detailed factoring with square roots
                    sqrt_a = sqrt(a)
                    sqrt_c = sqrt(c)
                    
                    st.write(f"Think of {latex(a)} as (√{latex(a)})² and {latex(c)} as (√{latex(c)})²")
                    st.write("")
                    st.write("**From first group:** Factor out √" + f"{latex(a)}x")
                    st.latex(f"\\sqrt{{{latex(a)}}}x(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})")
                    
                    st.write("**From second group:** Factor out √" + f"{latex(c)}")
                    st.latex(f"\\sqrt{{{latex(c)}}}(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})")
                    
                    st.write("Put them together:")
                    st.latex(f"= \\sqrt{{{latex(a)}}}x(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}}) - \\sqrt{{{latex(c)}}}(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})")
                
                # Step 6: Take out common factor
                st.write("**Step 6:** Notice the common binomial factor (√" + f"{latex(a)}x - √{latex(c)}) and factor it out:")
                if len(unique_roots) == 1:
                    r = unique_roots[0]
                    if a == 1:
                        st.latex(f"= (x - {latex(r)})^2")
                    else:
                        sqrt_a = sqrt(a)
                        sqrt_c = sqrt(c)
                        st.latex(f"= (\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})")
                        st.write("This can be written as:")
                        st.latex(f"= (\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})^2")
                else:
                    r1, r2 = unique_roots[0], unique_roots[1]
                    if a == 1:
                        st.latex(f"= (x - {latex(r1)})(x - {latex(r2)})")
                    else:
                        st.latex(f"= {latex(a)}(x - {latex(r1)})(x - {latex(r2)})")
                
                # Step 7: Set to zero
                st.write("**Step 7:** Set the equation equal to zero:")
                if len(unique_roots) == 1:
                    r = unique_roots[0]
                    if a == 1:
                        st.latex(f"(x - {latex(r)})^2 = 0")
                        st.write("Taking square root of both sides:")
                        st.latex(f"x - {latex(r)} = 0")
                    else:
                        sqrt_a = sqrt(a)
                        sqrt_c = sqrt(c)
                        st.latex(f"(\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}})^2 = 0")
                        st.write("Taking square root of both sides:")
                        st.latex(f"\\sqrt{{{latex(a)}}}x - \\sqrt{{{latex(c)}}} = 0")
                else:
                    r1, r2 = unique_roots[0], unique_roots[1]
                    if a == 1:
                        st.latex(f"(x - {latex(r1)})(x - {latex(r2)}) = 0")
                    else:
                        st.latex(f"{latex(a)}(x - {latex(r1)})(x - {latex(r2)}) = 0")
                    st.write("By zero product property, at least one factor must be zero")
                
                # Step 8: Solve - VERY DETAILED
                st.write("**Step 8:** Solve for x:")
                
                if len(unique_roots) == 1:
                    r = unique_roots[0]
                    if a == 1:
                        st.latex(f"x - {latex(r)} = 0")
                        st.latex(f"x = {latex(r)}")
                    else:
                        # Show detailed solving for sqrt case
                        sqrt_a = sqrt(a)
                        sqrt_c = sqrt(c)
                        
                        st.write("Move √" + f"{latex(c)} to the right side:")
                        st.latex(f"\\sqrt{{{latex(a)}}}x = \\sqrt{{{latex(c)}}}")
                        
                        st.write("Divide both sides by √" + f"{latex(a)}:")
                        st.latex(f"x = \\frac{{\\sqrt{{{latex(c)}}}}}{{\\sqrt{{{latex(a)}}}}}")
                        
                        st.write("Simplify by combining the radicals:")
                        st.latex(f"x = \\sqrt{{\\frac{{{latex(c)}}}{{{latex(a)}}}}}")
                        
                        # Optional rationalization section
                        st.markdown("---")
                        st.write("**Optional Step (Rationalizing the Denominator):**")
                        st.info("ℹ️ **Note for students:** This step is optional and done only to write the answer in a different form. You don't need to do this unless specifically asked to rationalize!")
                        
                        st.write("**Goal:** Remove the square root from the denominator")
                        
                        st.write("**Step 1:** Multiply by 'clever 1' (√" + f"{latex(a)}/√{latex(a)}):")
                        st.latex(f"x = \\frac{{\\sqrt{{{latex(c)}}}}}{{\\sqrt{{{latex(a)}}}}} \\times \\frac{{\\sqrt{{{latex(a)}}}}}{{\\sqrt{{{latex(a)}}}}}")
                        
                        st.write("**Step 2:** Multiply the numerators (tops):")
                        st.write(f"√{latex(c)} × √{latex(a)} = √({latex(c)} × {latex(a)}) = √{latex(c*a)}")
                        st.latex(f"\\text{{Numerator: }} \\sqrt{{{latex(c)}}} \\times \\sqrt{{{latex(a)}}} = \\sqrt{{{latex(c*a)}}}")
                        
                        st.write("**Step 3:** Multiply the denominators (bottoms):")
                        st.write(f"√{latex(a)} × √{latex(a)} = {latex(a)}")
                        st.latex(f"\\text{{Denominator: }} \\sqrt{{{latex(a)}}} \\times \\sqrt{{{latex(a)}}} = {latex(a)}")
                        
                        st.write("**Final Result:**")
                        st.latex(f"x = \\frac{{\\sqrt{{{latex(c*a)}}}}}{{{latex(a)}}}")
                        
                        st.write("So both forms are equivalent:")
                        st.latex(f"x = \\sqrt{{\\frac{{{latex(c)}}}{{{latex(a)}}}}} = \\frac{{\\sqrt{{{latex(c*a)}}}}}{{{latex(a)}}}")
                        
                        st.markdown("---")
                else:
                    r1, r2 = unique_roots[0], unique_roots[1]
                    st.write(f"**From first factor:** x - {latex(r1)} = 0")
                    st.latex(f"x = {latex(r1)}")
                    st.write("")
                    st.write(f"**From second factor:** x - {latex(r2)} = 0")
                    st.latex(f"x = {latex(r2)}")
                
                if len(unique_roots) < len(roots):
                    st.info("**Note:** This root is repeated twice.")
                
                st.write("**Therefore, the roots of the equation are:**")
                
                if len(unique_roots) == 1:
                    st.latex(f"x = {latex(unique_roots[0])}, \\quad x = {latex(unique_roots[0])}")
                else:
                    for root in unique_roots:
                        st.latex(f"x = {latex(root)}")
                
                # Final answer box with LaTeX rendering
                if len(unique_roots) == 1:
                    st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                    st.latex(f"x = {latex(unique_roots[0])} \\text{{ (repeated twice)}}")
                else:
                    st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                    root_latex = ", \\quad ".join([f"x = {latex(r)}" for r in unique_roots])
                    st.latex(root_latex)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ========== METHOD 2: QUADRATIC FORMULA ==========
            st.markdown("## 📕 Method 2: Quadratic Formula")
            
            with st.container():
                st.markdown("""<div style='background-color: white; padding: 40px; border-radius: 10px; color: black;'>""", unsafe_allow_html=True)
                
                st.markdown("### Solution:")
                
                st.write("**Step 1:** For the equation")
                st.latex(f"{latex(equation)} = 0")
                
                st.write("**Step 2:** Use the quadratic formula:")
                st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                
                st.write("**Step 3:** Identify the coefficients:")
                st.latex(f"a = {latex(a)}, \\quad b = {latex(b)}, \\quad c = {latex(c)}")
                
                st.write("**Step 4:** Calculate the discriminant:")
                st.latex(f"\\Delta = b^2 - 4ac")
                b_squared = expand(b**2)
                four_ac = 4*a*c
                st.latex(f"\\Delta = ({latex(b)})^2 - 4({latex(a)})({latex(c)})")
                st.latex(f"\\Delta = {latex(b_squared)} - {latex(four_ac)}")
                st.latex(f"\\Delta = {latex(discriminant)}")
                
                st.write("**Step 5:** Substitute into the formula:")
                neg_b = -b
                two_a = 2*a
                st.latex(f"x = \\frac{{-({latex(b)}) \\pm \\sqrt{{{latex(discriminant)}}}}}{{2({latex(a)})}}")
                st.latex(f"x = \\frac{{{latex(neg_b)} \\pm \\sqrt{{{latex(discriminant)}}}}}{{{latex(two_a)}}}")
                
                st.write("**Step 6:** Calculate the roots:")
                
                if discriminant == 0:
                    st.latex(f"x = \\frac{{{latex(neg_b)}}}{{{latex(two_a)}}}")
                    st.write("Simplify:")
                    st.latex(f"x = {latex(simplify(unique_roots[0]))}")
                    st.info("**Note:** Since Δ = 0, there is one repeated root.")
                    
                    st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                    st.latex(f"x = {latex(unique_roots[0])} \\text{{ (repeated twice)}}")
                    
                elif discriminant > 0:
                    if len(roots) >= 2:
                        st.latex(f"x_1 = {latex(simplify(roots[0]))}")
                        st.latex(f"x_2 = {latex(simplify(roots[1]))}")
                        
                        st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                        root_latex = ", \\quad ".join([f"x = {latex(simplify(r))}" for r in roots])
                        st.latex(root_latex)
                    else:
                        for root in unique_roots:
                            st.latex(f"x = {latex(root)}")
                        
                        st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                        root_latex = ", \\quad ".join([f"x = {latex(r)}" for r in unique_roots])
                        st.latex(root_latex)
                
                else:
                    st.write("The discriminant is negative, so the roots are complex.")
                    for i, root in enumerate(roots, 1):
                        st.latex(f"x_{i} = {latex(root)}")
                    
                    st.markdown(f'<div style="background-color: #1a4d2e; padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #27ae60;"><p style="color: #27ae60; font-size: 22px; font-weight: bold; margin: 0;">✅ Final Answer:</p></div>', unsafe_allow_html=True)
                    root_latex = ", \\quad ".join([f"x = {latex(r)}" for r in roots])
                    st.latex(root_latex)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ========== VERIFICATION ==========
            st.markdown("## ✅ Verification")
            
            with st.container():
                st.markdown("""<div style='background-color: white; padding: 40px; border-radius: 10px; color: black;'>""", unsafe_allow_html=True)
                
                for i, root in enumerate(unique_roots, 1):
                    st.write(f"**Verification for x = {latex(root)}:**")
                    st.write("Substituting into the original equation:")
                    
                    term_a = a * root**2
                    term_b = b * root
                    term_c = c
                    result = simplify(term_a + term_b + term_c)
                    
                    lhs = f"{latex(a)}({latex(root)})^2 + ({latex(b)})({latex(root)}) + {latex(c)}"
                    st.latex(lhs)
                    st.latex(f"= {latex(simplify(term_a))} + {latex(simplify(term_b))} + {latex(c)}")
                    st.latex(f"= {latex(result)}")
                    
                    if result == 0:
                        st.success("✓ Verified! The root satisfies the equation.")
                    
                    if i < len(unique_roots):
                        st.markdown("---")
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #808080; padding: 20px;">
        <p>Developed by Mohammed Salmaan | The Molecular Man Expert Tuition Solutions</p>
    </div>
""", unsafe_allow_html=True)
