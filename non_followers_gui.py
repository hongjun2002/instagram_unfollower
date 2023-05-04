# Import the required modules
from tkinter import *
from tkinter import messagebox, ttk
from non_followers import login, get_non_followers, unfollow_users

# Define the GUI function
def create_gui():
    # Create a dictionary to hold the data
    data = {'api': None, 'non_followers': []}

    # Define the function to be called when the "Get Non-followers" button is pressed
    def submit_form():
        # Get the username and password entered by the user
        username = username_entry.get()
        password = password_entry.get()

        # Show an error message if either the username or password is missing
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Use the login function to log in to Instagram and get the list of non-followers
        data['api'] = login(username, password)
        data['non_followers'] = get_non_followers(data['api'])

        # Update the list of non-followers in the GUI
        update_non_followers_list(data['non_followers'])

    # Define the function to update the list of non-followers in the GUI
    def update_non_followers_list(non_followers):
        non_followers_list.delete(0, END)
        for user in non_followers:
            non_followers_list.insert(END, f"{user['username']} (ID: {user['pk']})")

    # Define the function to be called when the "Unfollow Selected" button is pressed
    def unfollow_selected():
        # Get the indices of the selected users in the listbox
        selected_indices = non_followers_list.curselection()

        # Show an error message if no users are selected
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one user to unfollow.")
            return

        # Get the IDs of the selected users and call the unfollow_users function to unfollow them
        selected_users = [non_followers_list.get(index).split(" (ID: ")[1].rstrip(")") for index in selected_indices]
        unfollow_users(data['api'], selected_users)

        # Show a message to confirm that the users have been unfollowed, and update the list of non-followers in the GUI
        messagebox.showinfo("Unfollowed", f"Unfollowed {len(selected_users)} users.")
        submit_form()

    # Define the function to be called when the "Unfollow All" button is pressed
    def unfollow_all():
        # Get the IDs of all non-followers and call the unfollow_users function to unfollow them
        non_follower_ids = [user['pk'] for user in data['non_followers']]
        unfollow_users(data['api'], non_follower_ids)

        # Show a message to confirm that all non-followers have been unfollowed, and update the list of non-followers in the GUI
        messagebox.showinfo("Unfollowed", f"Unfollowed all {len(non_follower_ids)} non-followers.")
        submit_form()

    # Create the main window
    window = Tk()
    window.title("Instagram Non-followers")

    # Create a main frame to hold the widgets
    main_frame = ttk.Frame(window, padding="30 15")
    main_frame.grid(row=0, column=0, sticky=(N, W, E, S))

    # Create the username label and entry widget
    username_label = Label(main_frame, text="Username:")
    username_label.grid(row=0, column=0, sticky=W)

    password_label = Label(main_frame, text="Password:")
    password_label.grid(row=1, column=0, sticky=W)

    username_entry = Entry(main_frame)
    username_entry.grid(row=0, column=1)

    # Create the password label and entry widget
    password_entry = Entry(main_frame, show="*")
    password_entry.grid(row=1, column=1)

    submit_button = Button(main_frame, text="Get Non-followers", command=submit_form)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
                       
                       
    non_followers_list = Listbox(main_frame, width=40, height=20, selectmode='multiple')
    non_followers_list.grid(row=3, column=0, columnspan=2, pady=10)

    unfollow_selected_button = Button(main_frame, text="Unfollow Selected", command=unfollow_selected)
    unfollow_selected_button.grid(row=4, column=0, pady=10)

    unfollow_all_button = Button(main_frame, text="Unfollow All", command=unfollow_all)
    unfollow_all_button.grid(row=4, column=1, pady=10)

    window.mainloop()
    
    
if __name__ == "__main__":
    create_gui()