let addBtn;
let container;
let questionCount = 0;
const INITIAL_QUESTION_COUNT = 10;

//create a question block HTML
function createQuestionBlock(idx, isDeletable) {
    const deleteButton = isDeletable 
        ? `<button type="button" class="btn-delete-question" onclick="deleteQuestion(${idx})">Delete</button>`
        : '';
    
    return `
        <div class="question-block" data-question-index="${idx}" data-deletable="${isDeletable}">
            <div class="question-header-row">
                <div class="question-header">Question ${idx + 1}</div>
                ${deleteButton}
            </div>

            <div class="question-row">

                <div class="question-text">

                    <label>Enter Question</label><br>
                    <input type="text" name="questions[${idx}][text]" class="full-width-input" required>

                </div>

                <div class="question-diff">
                    <label>Difficulty</label><br>
                    <select name="questions[${idx}][difficulty]" required>

                        <option value="900">Easy</option>
                        <option value="1000">Medium</option>
                        <option value="1100">Hard</option>

                    </select>
                </div>
            </div>

            <div class="answers-label">Answer Options:</div>
            <div class="answers-row">

                <input type="text" name="questions[${idx}][choices][]" placeholder="Correct Answer" required>
                <input type="text" name="questions[${idx}][choices][]" placeholder="Answer Option" required>
                <input type="text" name="questions[${idx}][choices][]" placeholder="Optional Answer">
                <input type="text" name="questions[${idx}][choices][]" placeholder="Optional Answer">

            </div>
        </div>
    `;
}

//delete a question
window.deleteQuestion = function(idx) {
    if (!container) {
        container = document.getElementById("questions-container");
    }
    const questionBlock = container.querySelector(`[data-question-index="${idx}"]`);
    if (questionBlock) {
        questionBlock.remove();
        renumberQuestions();
    }
};

function renumberQuestions() {
    if (!container) {
        container = document.getElementById("questions-container");
    }
    const questionBlocks = container.querySelectorAll('.question-block');
    questionBlocks.forEach((block, index) => {
        const header = block.querySelector('.question-header');
        if (header) {
            header.textContent = `Question ${index + 1}`;
        }
        
        const isDeletable = index >= INITIAL_QUESTION_COUNT;
        block.setAttribute('data-question-index', index);
        block.setAttribute('data-deletable', isDeletable);
        
        const inputs = block.querySelectorAll('input, select');
        inputs.forEach(input => {
            const name = input.getAttribute('name');
            if (name) {
                // Replace the index in the name attribute
                const newName = name.replace(/questions\[\d+\]/, `questions[${index}]`);
                input.setAttribute('name', newName);
            }
        });
        
        const deleteBtn = block.querySelector('.btn-delete-question');
        const headerRow = block.querySelector('.question-header-row');
        
        if (isDeletable) {
            if (!deleteBtn) {
                const newDeleteBtn = document.createElement('button');
                newDeleteBtn.type = 'button';
                newDeleteBtn.className = 'btn-delete-question';
                newDeleteBtn.textContent = 'Delete';
                newDeleteBtn.onclick = () => deleteQuestion(index);
                headerRow.appendChild(newDeleteBtn);
            } else {
                //existing button onclick
                deleteBtn.setAttribute('onclick', `deleteQuestion(${index})`);
            }
        } else {
            //q not deletable
            if (deleteBtn) {
                deleteBtn.remove();
            }
        }
    });
    
    //questionCount to the current number of questions
    questionCount = questionBlocks.length;
}

//start w 10 questions
function initializeQuestions() {
    addBtn = document.getElementById("add-question");
    container = document.getElementById("questions-container");
    
    if (!addBtn || !container) {
        console.error("Required elements not found");
        return;
    }
    
    for (let i = 0; i < INITIAL_QUESTION_COUNT; i++) {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = createQuestionBlock(i, false);
        const block = tempDiv.firstElementChild;
        container.appendChild(block);
        questionCount++;
    }
    
    //event listener for adding new questions
    addBtn.addEventListener("click", () => {
        const idx = questionCount;
        //questions added after the initial 10 are deletable
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = createQuestionBlock(idx, true);
        const block = tempDiv.firstElementChild;
        container.appendChild(block);
        questionCount++;
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeQuestions);
} else {
    initializeQuestions();
}

