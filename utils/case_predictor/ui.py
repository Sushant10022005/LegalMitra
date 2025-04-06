"""
Case Predictor UI Components

This module provides UI components for the case outcome prediction feature.
"""

import streamlit as st
from typing import Dict, Any
from .analyzer import analyze_case_outcome

def render_case_predictor_ui():
    """
    Render the UI for the case outcome predictor feature.
    
    Returns:
        None
    """
    st.subheader("Case Outcome Predictor")
    st.write("Enter details about your case to get a prediction on the outcome and settlement recommendations.")
    
    # Add guidance for case details
    with st.expander("Tips for effective case analysis"):
        st.markdown("""
        To get the most accurate prediction, provide:
        - Detailed description of the case
        - Complete information about all parties involved
        - All available evidence
        - Timeline of events
        - Any previous legal history relevant to the case
        
        The more detailed information you provide, the more accurate the prediction will be.
        """)
    
    # Case Analysis Form
    with st.form("case_analysis_form"):
        # Basic case information
        case_type = st.selectbox(
            "Case Type",
            ["Civil", "Criminal", "Family", "Property", "Employment", "Consumer", "Other"]
        )
        
        jurisdiction = st.text_input("Jurisdiction/Court", placeholder="e.g., Delhi High Court, Mumbai District Court")
        
        # Party information
        accuser = st.text_area("Accuser/Plaintiff Details", placeholder="Name, age, occupation, and any relevant background")
        accused = st.text_area("Accused/Defendant Details", placeholder="Name, age, occupation, and any relevant background")
        victim = st.text_area("Victim Details (if applicable)", placeholder="Name, age, occupation, and any relevant background")
        
        # Case details
        case_description = st.text_area("Case Description", placeholder="Detailed description of the case, including the main issues and claims")
        timeline = st.text_area("Timeline of Events", placeholder="Chronological sequence of events leading to the case")
        
        # Evidence
        evidence = st.text_area("Evidence", placeholder="List all evidence available, including documents, witnesses, photos, etc.")
        
        # Previous legal history
        previous_legal_history = st.text_area("Previous Legal History", placeholder="Any previous legal proceedings related to this case or the parties involved")
        
        # Submit button
        submitted = st.form_submit_button("Analyze Case")
        
        if submitted:
            # Reset the session state to allow rendering the analysis again
            if 'analysis_rendered' in st.session_state:
                del st.session_state['analysis_rendered']
                
            # Validate required fields
            if not case_description or not accuser or not accused:
                st.error("Please provide at least the case description, accuser, and accused details.")
            else:
                # Collect all form data
                case_details = {
                    "case_type": case_type,
                    "jurisdiction": jurisdiction,
                    "accuser": accuser,
                    "accused": accused,
                    "victim": victim,
                    "case_description": case_description,
                    "timeline": timeline,
                    "evidence": evidence,
                    "previous_legal_history": previous_legal_history
                }
                
                # Show progress indicator
                with st.spinner("Analyzing your case..."):
                    # Call the API to analyze the case
                    result = analyze_case_outcome(case_details)
                    
                    # Check if there was an error
                    if "error" in result:
                        st.error(f"Error analyzing case: {result['error']}")
                    else:
                        # Display results in a structured way
                        render_analysis_results(result)

def render_analysis_results(result: Dict[str, Any]):
    """
    Render the analysis results in a structured way.
    
    Args:
        result: Dictionary containing the analysis results
        
    Returns:
        None
    """
    # Check if this is a duplicate call
    if 'analysis_rendered' in st.session_state:
        return
    
    # Mark that we've rendered the analysis
    st.session_state['analysis_rendered'] = True
    
    st.subheader("Case Analysis Results")
    
    # Win probability with visual indicator
    win_prob = result.get("win_probability", 0)
    confidence = result.get("confidence_score", 0)
    
    # Create a color-coded progress bar for win probability
    if win_prob >= 70:
        color = "green"
    elif win_prob >= 40:
        color = "orange"
    else:
        color = "red"
        
    st.markdown(f"### Win Probability: {win_prob}%")
    st.progress(win_prob / 100, text=f"Confidence: {confidence}%")
    
    # Key factors
    st.markdown("### Key Factors")
    for factor in result.get("key_factors", []):
        st.markdown(f"- {factor}")
    
    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Strengths")
        for strength in result.get("strengths", []):
            st.markdown(f"- {strength}")
            
    with col2:
        st.markdown("### Weaknesses")
        for weakness in result.get("weaknesses", []):
            st.markdown(f"- {weakness}")
    
    # Legal arguments
    st.markdown("### Legal Arguments")
    st.markdown("#### Arguments in Favor of the Plaintiff")
    for argument in result.get("legal_arguments", {}).get("plaintiff", []):
        st.markdown(f"- {argument}")
    
    st.markdown("#### Arguments in Favor of the Defendant")
    for argument in result.get("legal_arguments", {}).get("defendant", []):
        st.markdown(f"- {argument}")
    
    # Applicable laws
    st.markdown("### Applicable Laws")
    for law in result.get("applicable_laws", []):
        st.markdown(f"- **{law.get('name', 'Unknown Law')}**: {law.get('description', 'No description provided')}")
        if law.get("link"):
            st.markdown(f"  - [View on Indian Kanoon]({law.get('link')})")
    
    # Settlement recommendation if applicable
    settlement_recommendation = result.get("settlement_recommendation", "")
    if isinstance(settlement_recommendation, str) and settlement_recommendation and win_prob < 50:
        st.markdown("### Settlement Recommendation")
        st.info(settlement_recommendation)
    
    # Similar cases
    st.markdown("### Similar Cases")
    for case in result.get("similar_cases", []):
        with st.expander(f"{case.get('case_name', 'Unknown Case')}"):
            st.markdown(f"**Outcome:** {case.get('outcome', 'Not specified')}")
            if case.get("link"):
                st.markdown(f"**Link:** [View on Indian Kanoon]({case.get('link')})")
    
    # Disclaimer
    st.divider()
    st.caption("""
    **Disclaimer**: This analysis is based on the information provided and is not a guarantee of case outcome. 
    Legal outcomes depend on many factors including judge discretion, new evidence, and legal precedents.
    Always consult with a qualified legal professional for advice on your specific case.
    """) 