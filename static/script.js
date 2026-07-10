const chat = document.getElementById("chatBox");
const questionBox = document.getElementById("question");
const sendBtn = document.getElementById("sendBtn");
const welcome = document.getElementById("welcome");

/* ===========================
        AUTO RESIZE
=========================== */

questionBox.addEventListener("input", () => {

    questionBox.style.height = "auto";

    questionBox.style.height = questionBox.scrollHeight + "px";

});


/* ===========================
    ENTER TO SEND
=========================== */

questionBox.addEventListener("keydown", (e) => {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        askQuestion();

    }

});


/* ===========================
    EXAMPLE PROMPTS
=========================== */

document.querySelectorAll(".example").forEach(card => {

    card.addEventListener("click", () => {

        questionBox.value = card.innerText;

        askQuestion();

    });

});


/* ===========================
    SCROLL
=========================== */

function scrollBottom(){

    chat.scrollTo({

        top: chat.scrollHeight,

        behavior: "smooth"

    });

}


/* ===========================
        ASK
=========================== */

async function askQuestion(){

    const question = questionBox.value.trim();

    if(question==="")
        return;

    //----------------------------------
    // Hide Welcome Card
    //----------------------------------

    if(welcome){

        welcome.style.display="none";

    }

    //----------------------------------
    // Disable UI
    //----------------------------------

    sendBtn.disabled=true;

    //----------------------------------
    // USER MESSAGE
    //----------------------------------

    chat.innerHTML += `

        <div class="user-message">

            <div class="bubble user">

                ${question}

            </div>

        </div>

    `;

    questionBox.value="";

    questionBox.style.height="55px";

    scrollBottom();

    //----------------------------------
    // THINKING
    //----------------------------------

    const loadingId="loading-"+Date.now();

    chat.innerHTML+=`

        <div class="bot-message" id="${loadingId}">

            <div class="bubble bot">

                <div class="thinking">

                    <span>Thinking</span>

                    <div class="dot1"></div>

                    <div class="dot2"></div>

                    <div class="dot3"></div>

                </div>

            </div>

        </div>

    `;

    scrollBottom();

    //----------------------------------
    // FETCH
    //----------------------------------

    try{

        const response=await fetch("/ask",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                question:question

            })

        });

        if(!response.ok){

            throw new Error("Server Error");

        }

        const data=await response.json();

        //----------------------------------
        // Replace Loading
        //----------------------------------

        document.getElementById(loadingId).innerHTML=`

            <div class="bubble bot">

                <div class="model">

                    🟢 Powered By ${data.model}

                </div>

                <div class="answer">

                    ${marked.parse(data.answer)}

                </div>

            </div>

        `;

        //----------------------------------
        // Highlight Code
        //----------------------------------

        document.querySelectorAll("pre code").forEach((el)=>{

            hljs.highlightElement(el);

        });

    }

    catch(error){

        document.getElementById(loadingId).innerHTML=`

            <div class="bubble bot">

                ❌ Something went wrong.

                Please try again.

            </div>

        `;

    }

    //----------------------------------
    // Enable
    //----------------------------------

    sendBtn.disabled=false;

    questionBox.focus();

    scrollBottom();

}
document.addEventListener("DOMContentLoaded", () => {

    const logo = document.getElementById("logo");
    const overlay = document.getElementById("logoOverlay");

    logo.addEventListener("click", function(e){

        e.stopPropagation();

        logo.classList.toggle("expanded");
        overlay.classList.toggle("show");

    });

    overlay.addEventListener("click", function(){

        logo.classList.remove("expanded");
        overlay.classList.remove("show");

    });

    document.addEventListener("click", function(){

        logo.classList.remove("expanded");
        overlay.classList.remove("show");

    });

});