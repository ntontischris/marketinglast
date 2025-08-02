document.addEventListener('DOMContentLoaded', () => {
    // Form elements
    const form = document.getElementById('idea-form');
    const topicInput = document.getElementById('topic-input');

    // Ideas section elements
    const ideasSection = document.getElementById('ideas-section');
    const ideasLoader = document.getElementById('ideas-loader');
    const ideasList = document.getElementById('ideas-list');

    // Draft section elements
    const draftSection = document.getElementById('draft-section');
    const draftLoader = document.getElementById('draft-loader');
    const draftOutput = document.getElementById('draft-output');

    // Specialist section elements
    const specialistSection = document.getElementById('specialist-section');
    const specialistButtonsContainer = document.getElementById('specialist-buttons-container');
    const specialistResultsContainer = document.getElementById('specialist-results-container');

    // --- Event Listeners ---

    // 1. Handle the main form submission to generate ideas
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const topic = topicInput.value;

        if (!topic) return;

        // Reset UI
        ideasSection.classList.add('hidden');
        draftSection.classList.add('hidden');
        specialistSection.classList.add('hidden'); // Hide specialist section on new generation
        ideasList.innerHTML = '';
        draftOutput.innerHTML = '';
        specialistButtonsContainer.innerHTML = ''; // Clear old buttons
        specialistResultsContainer.innerHTML = ''; // Clear old results
        ideasLoader.classList.remove('hidden');

        try {
            const response = await fetch('/generate-ideas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            const data = await response.json();
            displayIdeas(data.generated_ideas, topic);

        } catch (error) {
            console.error('Error fetching ideas:', error);
            ideasList.innerHTML = `<li class='error'>Failed to fetch ideas. Please try again.</li>`;
        } finally {
            ideasLoader.classList.add('hidden');
            ideasSection.classList.remove('hidden');
        }
    });

    // --- UI Functions ---

    // 2. Function to display the list of ideas
    function displayIdeas(ideas, topic) {
        ideasList.innerHTML = ''; // Clear previous ideas

        if (!ideas || ideas.length === 0) {
            ideasList.innerHTML = `<li class='error'>No ideas were generated.</li>`;
            return;
        }

        ideas.forEach(idea => {
            const ideaItem = document.createElement('li');
            
            const textSpan = document.createElement('span');
            textSpan.textContent = idea.text; // Text is already clean from the backend
            
            const draftButton = document.createElement('button');
            draftButton.textContent = 'Write Draft';
            draftButton.className = 'draft-button';
            
            // Attach data and click listener
            draftButton.dataset.id = idea.id;
            draftButton.dataset.text = idea.text;
            draftButton.addEventListener('click', () => generateDraft(topic, idea.id, idea.text));

            ideaItem.appendChild(textSpan);
            ideaItem.appendChild(draftButton);
            ideasList.appendChild(ideaItem);
        });
    }

    // 3. Function to fetch a draft for a selected idea
    async function generateDraft(topic, ideaId, ideaText) {
        console.log(`Generating draft for Idea ID: ${ideaId}`);

        // Show draft section and loader
        draftSection.classList.remove('hidden');
        draftLoader.classList.remove('hidden');
        draftOutput.innerHTML = '';

        try {
            const response = await fetch('/generate-draft', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    topic: topic, 
                    idea_id: parseInt(ideaId, 10), // Send the ID as an integer
                    idea_text: ideaText // Also send the text for the prompt
                }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            const data = await response.json();
            // Replace newlines with <br> for proper HTML rendering
            draftOutput.innerHTML = data.draft.replace(/\n/g, '<br>');

            // Now that the draft is created, show the specialist agent buttons
            displaySpecialistButtons(data.draft_id, data.draft);

        } catch (error) {
            console.error('Error fetching draft:', error);
            draftOutput.textContent = 'Failed to generate draft. Please check the console.';
        } finally {
            draftLoader.classList.add('hidden');
        }
    }

    // 4. Function to display the specialist agent buttons
    function displaySpecialistButtons(draftId, draftText) {
        specialistSection.classList.remove('hidden');
        specialistButtonsContainer.innerHTML = ''; // Clear previous buttons
        specialistResultsContainer.innerHTML = ''; // Clear previous results

        const platforms = ['Twitter', 'Instagram', 'Facebook', 'TikTok', 'Blog'];

        platforms.forEach(platform => {
            const button = document.createElement('button');
            button.textContent = `Adapt for ${platform}`;
            button.className = 'specialist-button';
            button.onclick = () => specializeDraft(draftId, draftText, platform.toLowerCase());
            specialistButtonsContainer.appendChild(button);
        });
    }

    // 5. Function to call the specialist agent API
    async function specializeDraft(draftId, draftText, platform) {
        console.log(`Specializing draft ID ${draftId} for ${platform}`);
        
        // Create a dedicated container for this platform's result
        let resultContainer = document.getElementById(`result-${platform}`);
        if (!resultContainer) {
            resultContainer = document.createElement('div');
            resultContainer.id = `result-${platform}`;
            resultContainer.className = 'specialist-result-box';
            specialistResultsContainer.appendChild(resultContainer);
        }

        resultContainer.innerHTML = `<div class="loader"></div>`; // Show loader

        try {
            const response = await fetch('/specialize-draft', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    draft_id: draftId,
                    draft_text: draftText,
                    platform: platform
                }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            const data = await response.json();

            // Display the result
            resultContainer.innerHTML = `
                <h3>${platform.charAt(0).toUpperCase() + platform.slice(1)} Version</h3>
                <p>${data.specialized_draft.replace(/\n/g, '<br>')}</p>
            `;

        } catch (error) {
            console.error(`Error specializing for ${platform}:`, error);
            resultContainer.innerHTML = `<p class="error">Failed to adapt for ${platform}.</p>`;
        }
    }
});
