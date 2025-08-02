document.addEventListener('DOMContentLoaded', () => {
    const historyContainer = document.getElementById('history-container');
    const loader = document.getElementById('history-loader');

    async function fetchHistory() {
        loader.classList.remove('hidden');

        try {
            const response = await fetch('/api/history');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const historyData = await response.json();
            renderHistory(historyData);
        } catch (error) {
            console.error('Error fetching history:', error);
            historyContainer.innerHTML = '<p class="error">Could not load history. Please try again later.</p>';
        } finally {
            loader.classList.add('hidden');
        }
    }

    function renderHistory(history) {
        if (history.length === 0) {
            historyContainer.innerHTML = '<p>No campaigns found yet. Go generate some ideas!</p>';
            return;
        }

        history.forEach(campaign => {
            const campaignElement = document.createElement('div');
            campaignElement.className = 'campaign-card';

            const campaignHeader = document.createElement('h2');
            campaignHeader.textContent = `Campaign: ${campaign.topic}`;
            
            const campaignDate = document.createElement('span');
            campaignDate.className = 'date';
            campaignDate.textContent = new Date(campaign.created_at).toLocaleString();
            campaignHeader.appendChild(campaignDate);

            campaignElement.appendChild(campaignHeader);

            campaign.ideas.forEach(idea => {
                const ideaElement = document.createElement('div');
                ideaElement.className = 'idea-card';

                const ideaHeader = document.createElement('h3');
                ideaHeader.textContent = `Idea: ${idea.idea_text}`;
                ideaElement.appendChild(ideaHeader);

                if (idea.drafts && idea.drafts.length > 0) {
                    const draftsContainer = document.createElement('div');
                    draftsContainer.className = 'drafts-container';
                    ideaElement.appendChild(draftsContainer);

                    idea.drafts.forEach(draft => {
                        const draftItem = document.createElement('div');
                        draftItem.className = 'history-draft';
                        
                        let draftHTML = `<p><strong>Original Draft:</strong><br>${draft.draft_text.replace(/\n/g, '<br>')}</p>`;

                        // Check for and display specialized drafts
                        if (draft.specialized_drafts && draft.specialized_drafts.length > 0) {
                            draftHTML += '<div class="specialized-drafts-history">';
                            draft.specialized_drafts.forEach(sd => {
                                draftHTML += `
                                    <div class="specialized-draft-item">
                                        <strong>${sd.platform.charAt(0).toUpperCase() + sd.platform.slice(1)} Version:</strong>
                                        <p>${sd.specialized_text.replace(/\n/g, '<br>')}</p>
                                    </div>
                                `;
                            });
                            draftHTML += '</div>';
                        }

                        draftItem.innerHTML = draftHTML;
                        draftsContainer.appendChild(draftItem);
                    });
                }
                campaignElement.appendChild(ideaElement);
            });

            historyContainer.appendChild(campaignElement);
        });
    }

    // Initial fetch
    fetchHistory();
});
