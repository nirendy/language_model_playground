import streamlit as st


def render():
    st.write(
        f"""
        # Welcome to the Transformers Playground!
        
        This playground designed as an interactive tutorial for the Transformers library by HuggingFace 🤗 
        
        It will be done in steps, tha every step is relying on the one before it
        
        Now you're in the Home step, you can move steps clicking on the corresponding button
        
        ---
        **Step 1: Choose a Task **
        - First define what is the task that we are trying to solve 
        
        **Step 2: Choose a model**
        - Models designed or trained for a specific task, therefore, we want to browse only models that are trained 
        for the selected task
        
        **Step 3: Choose Generation Params**
        - There are degrees of freedom in deciding how to create the resulted output by the logits...

        **Step 4: See and compare the results**
        - See multiple models output simultaneously and notice the difference in the results
        
        ---
        
        Start by clicking on the Task Selection Button at the top. 
        You can return this page for reference at any point!
        """
    )
