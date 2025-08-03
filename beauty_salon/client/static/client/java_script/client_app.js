// client/static/client/js/client_app.js

// ==========================================================================
// 1. Constants & Global Variables
// ==========================================================================

const API_URL = 'http://127.0.0.1:8000/api/clients/';

// --- DOM Element Selectors ---
// Create Form
const clientForm = document.getElementById('client-form');
const clientList = document.getElementById('client-list');
const feedbackMessage = document.getElementById('feedback-message');

// Edit Modal
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const closeButton = document.querySelector('.close-button');
const editClientId = document.getElementById('edit-client-id');


// ==========================================================================
// 2. API Communication (CRUD Functions)
// ==========================================================================

/**
 * Fetches all clients from the API and renders them in the table.
 * @async
 */
async function fetchClients() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        
        // Clear the table body before rendering new data
        clientList.innerHTML = ''; 

        // API might return data in a 'results' key if paginated
        const clients = data.results || data;

        clients.forEach(client => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${client.id}</td>
                <td>${client.client_name}</td>
                <td>${client.client_email}</td>
                <td>${client.client_number}</td>
                <td>
                    <button onclick="openEditModal(${client.id})">Editar</button>
                    <button onclick="deleteClient(${client.id})">Excluir</button>
                </td>
            `;
            clientList.appendChild(row);
        });

    } catch (error) {
        console.error('Error fetching clients:', error);
        showFeedback('Erro ao carregar a lista de clientes.', 'error');
    }
}

/**
 * Handles the submission of the create form, sending new client data to the API.
 * @async
 * @param {Event} event - The form submission event.
 */
async function createClient(event) {
    event.preventDefault(); // Prevent default browser form submission
    
    const formData = new FormData(clientForm);
    const clientData = {
        client_name: formData.get('client_name'),
        client_email: formData.get('client_email'),
        client_number: formData.get('client_number'),
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(clientData),
        });

        // HTTP 201 Created is the standard success status for POST
        if (response.status === 201) {
            showFeedback('Cliente cadastrado com sucesso!', 'success');
            clientForm.reset();
            await fetchClients(); // Refresh the client list
        } else {
            const errorData = await response.json();
            // A simple way to format API validation errors for display
            const errorMessage = Object.entries(errorData).map(([key, value]) => `${key}: ${value}`).join('\n');
            throw new Error(errorMessage);
        }
    } catch (error) {
        console.error('Error creating client:', error);
        showFeedback(`Erro ao salvar: ${error.message}`, 'error');
    }
}

/**
 * Deletes a client after user confirmation.
 * @async
 * @param {number} clientId - The ID of the client to delete.
 */
async function deleteClient(clientId) {
    // Use a native browser confirm dialog as a simple guardrail
    if (!confirm('Tem certeza que deseja excluir este cliente?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}${clientId}/`, {
            method: 'DELETE',
        });

        // HTTP 204 No Content is the standard success status for DELETE
        if (response.status === 204) {
            showFeedback('Cliente excluído com sucesso!', 'success');
            await fetchClients(); // Refresh the client list
        } else {
            throw new Error('Falha ao excluir o cliente.');
        }
    } catch (error) {
        console.error('Error deleting client:', error);
        showFeedback(error.message, 'error');
    }
}

/**
 * Fetches a single client's details and populates the edit modal.
 * @async
 * @param {number} clientId - The ID of the client to edit.
 */
async function openEditModal(clientId) {
    try {
        const response = await fetch(`${API_URL}${clientId}/`);
        if (!response.ok) throw new Error('Cliente não encontrado.');
        
        const client = await response.json();
        
        // Populate the edit form with the fetched data
        editClientId.value = client.id;
        document.getElementById('edit_client_name').value = client.client_name;
        document.getElementById('edit_client_email').value = client.client_email;
        document.getElementById('edit_client_number').value = client.client_number;
        
        editModal.style.display = 'block';

    } catch (error) {
        showFeedback(error.message, 'error');
    }
}

/**
 * Handles the submission of the edit form, sending updated data to the API.
 * @async
 * @param {Event} event - The form submission event.
 */
async function handleUpdateSubmit(event) {
    event.preventDefault();
    const clientId = editClientId.value;
    const clientData = {
        client_name: document.getElementById('edit_client_name').value,
        client_email: document.getElementById('edit_client_email').value,
        client_number: document.getElementById('edit_client_number').value,
    };

    try {
        const response = await fetch(`${API_URL}${clientId}/`, {
            method: 'PUT', // PUT replaces the entire resource, PATCH updates parts of it
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(clientData),
        });

        if (response.ok) {
            showFeedback('Cliente atualizado com sucesso!', 'success');
            editModal.style.display = 'none';
            await fetchClients();
        } else {
            const errorData = await response.json();
            const errorMessage = Object.entries(errorData).map(([key, value]) => `${key}: ${value}`).join('\n');
            throw new Error(errorMessage);
        }
    } catch (error) {
        showFeedback(`Erro ao atualizar: ${error.message}`, 'error');
    }
}


// ==========================================================================
// 3. UI Helper Functions & Event Listeners
// ==========================================================================

/**
 * Displays a feedback message to the user for a few seconds.
 * @param {string} message - The message to display.
 * @param {string} type - The message type ('success' or 'error'), used as a CSS class.
 */
function showFeedback(message, type) {
    feedbackMessage.textContent = message;
    feedbackMessage.className = type;
    feedbackMessage.style.display = 'block';
    
    // Hide the message after 5 seconds
    setTimeout(() => { feedbackMessage.style.display = 'none'; }, 5000);
}

// --- Modal Controls ---
closeButton.onclick = () => {
    editModal.style.display = 'none';
};

window.onclick = (event) => {
    // Close the modal if the user clicks on the dark overlay
    if (event.target == editModal) {
        editModal.style.display = 'none';
    }
};

// --- Main Event Listeners ---
// The script's entry points, linking functions to user actions.
clientForm.addEventListener('submit', createClient);
editForm.addEventListener('submit', handleUpdateSubmit);
document.addEventListener('DOMContentLoaded', fetchClients);