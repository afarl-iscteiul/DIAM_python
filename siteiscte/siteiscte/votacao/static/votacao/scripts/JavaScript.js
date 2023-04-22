

function hideProfilePic() {
    document.getElementById("aluno.avatar").style.visibility = "hidden";
}

function showProfilePic() {
    document.getElementById("aluno.avatar").style.visibility = "visible";
}

function toogleQuestions() {
    var questions = document.getElementById("questoes");
    var toggleButton = document.getElementById("toggleButton");

    if (questions.style.visibility === "hidden") {
        questions.style.visibility = "visible";
        toggleButton.innerHTML = "Esconder lista de Questões";
    } else {
        questions.style.visibility = "hidden";
        toggleButton.innerHTML = "Mostrar lista de Questões";
    }
}

// Para o campo de comentários na página de registo

    let bannedWords = [];
    let commentValidated = false;

    function validateComment() {
        const comment = document.getElementById("comentario").value;
        const validationStatus = document.getElementById("comment-validation-status");
        //LISTA DE PALAVRAS BANIDAS

         // Fetch banned words from file
         //     fetch('banned_words.txt')
         //         .then(response => response.text())
         //         .then(data => bannedWords = data.split('\n'))
         //         .catch(error => console.error(error));

    const bannedWords = ["abécula", "abecula", "abentesma", "achavascado", "alimária", "alimaria",
            "andrajoso", "barregã", "barrega", "biltre", "cacóstomo", "cacostomo", "cuarra", "estólido", "estolido",
            "estroso", "estultilóquio", "estultiloquio", "nefelibata", "néscio", "nescio", "pechenga", "sevandija",
            "somítico", "somitico", "tatibitate", "xexé", "xexe", "cheché", "cheche", "xexelento"];


        for (let i = 0; i < bannedWords.length; i++) {
            if (comment.toLowerCase().includes(bannedWords[i])) {
                validationStatus.innerHTML = "Comentário não aceite.";
                document.getElementById("comentario").value = "";
                commentValidated = false;
                document.getElementById("registo-submit").disabled = true;
                return;
            }
        }

        validationStatus.innerHTML = "Comentário aceite.";
        commentValidated = true;
        document.getElementById("registo-submit").disabled = false;
    }

    // Add event listener to "comentario" input field
    document.getElementById("comentario").addEventListener("input", function () {
        // Reset validation status
        const validationStatus = document.getElementById("comment-validation-status");
        validationStatus.innerHTML = "";

        // Disable submit button
        document.getElementById("registo-submit").disabled = true;

        // Reset commentValidated flag
        commentValidated = false;
    });

    document.getElementById("registo-form").addEventListener("submit", function (event) {
        if (!commentValidated) {
            event.preventDefault();
            alert("Por favor, valide o comentário antes de submeter o formulário.");
        }
    });


