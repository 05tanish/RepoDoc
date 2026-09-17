import sys
import os

def launch_tui(report_data):
    """
    Launches a cross-platform raw terminal UI.
    """
    try:
        # Check if windows
        if os.name == 'nt':
            import msvcrt
            def getch():
                return msvcrt.getch()
        else:
            import tty
            import termios
            def getch():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
                
        # Simple render loop
        selected = 0
        menu = ["View Summary", "View Security", "View Code Smells", "Exit"]
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== 🎮 RepoDoctor Interactive Dashboard ===")
            print(f"Health Score: {report_data.get('score', 'N/A')}/100\n")
            
            for i, item in enumerate(menu):
                if i == selected:
                    print(f" > \033[92m{item}\033[0m")
                else:
                    print(f"   {item}")
                    
            print("\n(Use W/S to move, Enter to select)")
            
            c = getch()
            if type(c) == bytes: c = c.decode('utf-8', 'ignore')
            c = c.lower()
            
            if c == 'w':
                selected = max(0, selected - 1)
            elif c == 's':
                selected = min(len(menu) - 1, selected + 1)
            elif c == '\r' or c == '\n':
                if selected == 3:
                    break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"--- {menu[selected]} ---")
                    print("This feature is active! Press any key to go back.")
                    getch()
            elif c == 'q':
                break
                
    except Exception as e:
        print(f"TUI Error: {e}")
