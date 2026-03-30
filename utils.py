def get_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def print_menu(options):
    print("\n--- MENU ---")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    
    while True:
        choice = get_input(f"Enter your choice (1-{len(options)}): ")
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
        print(f"Invalid choice. Please select 1 to {len(options)}.")
