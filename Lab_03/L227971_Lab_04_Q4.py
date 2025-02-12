def remove_alphanumeric(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        filtered_content = ''.join(ch for ch in content if not ch.isalnum())
        
        with open("output.txt", 'w', encoding='utf-8') as file:
            file.write(filtered_content)
        
        print("Processing complete. Check output.txt for results.")
    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

remove_alphanumeric("input.txt")