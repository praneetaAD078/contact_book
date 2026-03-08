#TASK 5 - contact book
import json
import gradio as gr

# File to store contacts
CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Initialize contacts
contacts = load_contacts()

# Function to add a contact
def add_contact(name, phone, email, address):
    if not name or not phone:
        return "Name and Phone are required fields!"

    # Check if contact already exists
    for contact in contacts:
        if contact["phone"] == phone:
            return "Contact with this phone number already exists!"

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts()
    return f"Contact '{name}' added successfully!"

# Function to view all contacts
def view_contacts():
    if not contacts:
        return "No contacts found!"
    return "\n".join([f"{c['name']} - {c['phone']}" for c in contacts])

# Function to search a contact by name or phone
def search_contact(query):
    result = [c for c in contacts if query.lower() in c["name"].lower() or query in c["phone"]]
    if not result:
        return "No matching contacts found!"
    return "\n".join([f"{c['name']} - {c['phone']} ({c['email']}, {c['address']})" for c in result])

# Function to update a contact
def update_contact(phone, new_name, new_phone, new_email, new_address):
    for contact in contacts:
        if contact["phone"] == phone:
            contact["name"] = new_name if new_name else contact["name"]
            contact["phone"] = new_phone if new_phone else contact["phone"]
            contact["email"] = new_email if new_email else contact["email"]
            contact["address"] = new_address if new_address else contact["address"]
            save_contacts()
            return f"Contact '{new_name}' updated successfully!"
    return "Contact not found!"

# Function to delete a contact
def delete_contact(phone):
    global contacts
    contacts = [c for c in contacts if c["phone"] != phone]
    save_contacts()
    return f"Contact with phone '{phone}' deleted successfully!"

# Gradio UI
with gr.Blocks() as contact_book:
    gr.Markdown("## 📖 Contact Book")

    # Add Contact Section
    with gr.Row():
        with gr.Column():
            name_input = gr.Textbox(label="Name")
            phone_input = gr.Textbox(label="Phone")
            email_input = gr.Textbox(label="Email (Optional)")
            address_input = gr.Textbox(label="Address (Optional)")
            add_btn = gr.Button("➕ Add Contact")
        output_add = gr.Textbox(label="Add Contact Status", interactive=False)

    # View Contacts
    view_btn = gr.Button("📜 View All Contacts")
    output_view = gr.Textbox(label="Contact List", interactive=False)

    # Search Contact
    search_query = gr.Textbox(label="Search by Name or Phone")
    search_btn = gr.Button("🔍 Search")
    output_search = gr.Textbox(label="Search Results", interactive=False)

    # Update Contact
    with gr.Row():
        phone_update = gr.Textbox(label="Existing Phone Number")
        new_name = gr.Textbox(label="New Name (Leave blank to keep same)")
        new_phone = gr.Textbox(label="New Phone (Leave blank to keep same)")
        new_email = gr.Textbox(label="New Email (Leave blank to keep same)")
        new_address = gr.Textbox(label="New Address (Leave blank to keep same)")
        update_btn = gr.Button("✏️ Update Contact")
    output_update = gr.Textbox(label="Update Status", interactive=False)

    # Delete Contact
    delete_phone = gr.Textbox(label="Phone Number to Delete")
    delete_btn = gr.Button("🗑 Delete Contact")
    output_delete = gr.Textbox(label="Delete Status", interactive=False)

    # Button Click Events
    add_btn.click(add_contact, inputs=[name_input, phone_input, email_input, address_input], outputs=output_add)
    view_btn.click(view_contacts, outputs=output_view)
    search_btn.click(search_contact, inputs=search_query, outputs=output_search)
    update_btn.click(update_contact, inputs=[phone_update, new_name, new_phone, new_email, new_address], outputs=output_update)
    delete_btn.click(delete_contact, inputs=delete_phone, outputs=output_delete)

# Launch the app
contact_book.launch()
