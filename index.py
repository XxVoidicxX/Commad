# index.py

try:
    import commad
    # Import additional tools (commented out as they don't exist yet)
    # from tool_module_1 import Tool1
    # from tool_module_2 import Tool2
    # from tool_module_3 import Tool3
except ImportError as e:
    print(f"Error importing module: {e}")

if __name__ == "__main__":
    app = commad.ToolApp()
    app.startup()
    
    # tool1 = Tool1()
    # tool2 = Tool2()
    # tool3 = Tool3()
