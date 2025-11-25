def treasure(all_treasures_list):
    all_treasures = set(all_treasures_list)
    found_treasure = set()
    while True:
        if len(all_treasures) == len(found_treasure):
            print("\nCongratulations! You found all the treasures.")
            break
        
        x_input= (input("Enter the X coordinate or (type 'quit' to exit): "))
       
        if x_input.lower() == "quit":
            break

        y_input= (input("Enter the Y coordinate or (type 'quit' to exit): "))
        
        if y_input.lower() == "quit":
            break
        try:
            x = int(x_input)
            y = int(y_input)
        except ValueError:
            print("Invalid input. Please enter numbers for coordinates.")
            continue 

        current_xy = (x, y)
       
        
        if current_xy in found_treasure:
            print("You already collected that one.")
        
            
        elif current_xy in all_treasures:
            print("You found treasure!") 
            found_treasure.add(current_xy)
        else:
            
            print("No treasure found at these coordinates.")

    remaining = len(all_treasures) - len(found_treasure)

    print("*" * 5,"Summary","*" * 5)    
    print(f"Treasure remaining: {remaining}")    
    
    sorted_treasure = (sorted(list(found_treasure)))
    print(f"Your treasures: {sorted_treasure}")
        
    return remaining      

if __name__ == "__main__":
    treasure(((2,4),(5,7),(8,3)))