from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="https://raw.githubusercontent.com/Luann8/Quiz-Cyberseguranca/main/OIG.ico"
        type="image/x-icon">
    <title>Qu1z de h4ck3r</title>
    <style>
        * {
            padding: 0;
            margin: 0;
            box-sizing: border-box;
        }

        html {
            background: rgb(0, 0, 0);
            height: 100%;
            overflow: hidden;
        }

        body {
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: 'Courier New', Courier, monospace;
            overflow: hidden;
            position: relative; 
        }

        .background-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5); 
            z-index: -1; 
        }

        .container {
            background-color: #111111f6;
            border: 2px solid #e1e1e6;
            border-radius: 0px;
            padding: 20px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
            text-align: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1; 
        }

        .questions-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
        }

        .question {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #ffffff;
        }

        .answers-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }

        .answer:disabled {
            cursor: not-allowed;
        }

        .next-question {
            margin-top: 32px;
        }

        .button {
            background-color: #014410;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 0px;
            padding: 12px 32px;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.2s;
        }

        .button:hover {
            
            transform: scale(1.05);
        }

        .final-message {
            font-size: 20px;
            text-align: center;
            margin-top: 20px;
        }

        .final-message span {
            display: block;
            margin-top: 8px;
        }

        .hide {
            display: none;
        }

        .correct {
            background-color: #049b48;
            color: #fff; /* Cor branca para o texto */
        }

        .incorrect {
            background-color: #a10101;
        }

        h1,
        h2 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 30px;
            color: #049b11;
        }

        h1 {
            animation: glitch 2s infinite;
        }

        h2 {
            animation: glitch 2s infinite reverse;
        }

        @keyframes glitch {

            0%,
            100% {
                transform: none;
            }

            20% {
                transform: translate(-2px, -2px) skew(0deg);
            }

            40% {
                transform: translate(2px, 2px) skew(0deg);
            }

            60% {
                transform: translate(-2px, 2px) skew(2deg);
            }

            80% {
                transform: translate(2px, -2px) skew(-2deg);
            }
        }

        .content {
            margin-bottom: 30px;
            text-align: center;
        }
    
        .final-message {
            font-size: 20px;
            text-align: center;
            margin-top: 20px;
            color: #fff; /* Define a cor do texto como branca */
        }

        .final-message span {
            display: block;
            margin-top: 8px;
            color: #fff; /* Define a cor do texto como branca */
        }
    </style>
</head>

<body>
    <div class="background-overlay"></div>
    <div class="container">
        <h1>Qu1z h4ck3r</h1>
        <br>
        <div class="questions-container hide">
            <span class="question">Pergunta aqui?</span>
            <div class="answers-container"></div>
        </div>
        <div class="controls-container">
            <button class="start-quiz button">Começar Quiz!</button>
            <button class="next-question button hide">Próxima pergunta</button>
        </div>
    </div>

    <canvas id="Matrix"></canvas>


    <script>
        const $startGameButton = document.querySelector(".start-quiz");
        const $nextQuestionButton = document.querySelector(".next-question");
        const $questionsContainer = document.querySelector(".questions-container");
        const $questionText = document.querySelector(".question");
        const $answersContainer = document.querySelector(".answers-container");
        const $answers = document.querySelectorAll(".answer");

        let currentQuestionIndex = 0;
        let totalCorrect = 0;

        $startGameButton.addEventListener("click", startGame);
        $nextQuestionButton.addEventListener("click", displayNextQuestion);

        function startGame() {
            $startGameButton.classList.add("hide");
            $questionsContainer.classList.remove("hide");
            displayNextQuestion();
        }

        function displayNextQuestion() {
            resetState();

            if (questions.length === currentQuestionIndex) {
                return finishGame();
            }

            $questionText.textContent = questions[currentQuestionIndex].question;
            questions[currentQuestionIndex].answers.forEach(answer => {
                const newAnswer = document.createElement("button");
                newAnswer.classList.add("button", "answer");
                newAnswer.textContent = answer.text;
                if (answer.correct) {
                    newAnswer.dataset.correct = answer.correct;
                }
                $answersContainer.appendChild(newAnswer);

                newAnswer.addEventListener("click", selectAnswer);
            });
        }

        function resetState() {
            while ($answersContainer.firstChild) {
                $answersContainer.removeChild($answersContainer.firstChild);
            }

            document.body.removeAttribute("class");
            $nextQuestionButton.classList.add("hide");
        }

        function selectAnswer(event) {
            const answerClicked = event.target;

            if (answerClicked.dataset.correct) {
                document.body.classList.add("correct");
                totalCorrect++;
            } else {
                document.body.classList.add("incorrect");
            }

            document.querySelectorAll(".answer").forEach(button => {
                button.disabled = true;

                if (button.dataset.correct) {
                    button.classList.add("correct");
                } else {
                    button.classList.add("incorrect");
                }
            });

            $nextQuestionButton.classList.remove("hide");
            currentQuestionIndex++;
        }

        function finishGame() {
            const totalQuestions = questions.length;
            const performance = Math.floor(totalCorrect * 100 / totalQuestions);

            let message = "";

            switch (true) {
                case (performance >= 90):
                    message = "Excelente :)";
                    break;
                case (performance >= 70):
                    message = "Muito bom :)";
                    break;
                case (performance >= 50):
                    message = "Bom";
                    break;
                default:
                    message = "Pode melhorar :(";
            }

            $questionsContainer.innerHTML =
                `
                <p class="final-message">
                    Você acertou ${totalCorrect} de ${totalQuestions} questões!
                    <span>Resultado: ${message}</span>
                </p>
                <button 
                    onclick=window.location.reload() 
                    class="button"
                >
                    Refazer teste
                </button>
            `;
        }

        const questions = [
            {
                question: "O que é engenharia social?",
                answers: [
                    { text: "a) Um método de criptografia avançada.", correct: false },
                    { text: "b) Um ataque que explora falhas no código-fonte.", correct: false },
                    { text: "c) Uma técnica que utiliza manipulação psicológica para obter informações confidenciais.", correct: true },
                    { text: "d) Um tipo de ataque de negação de serviço.", correct: false },
                    { text: "e) Um protocolo de segurança de rede.", correct: false }
                ]
            },
            {
                question: "O que é um ataque de phishing?",
                answers: [
                    { text: "a) Um ataque físico a servidores de dados.", correct: false },
                    { text: "b) Uma técnica de recuperação de senhas perdidas.", correct: false },
                    { text: "c) Um ataque que explora vulnerabilidades de software.", correct: false },
                    { text: "d) Uma tentativa de enganar as pessoas para obter informações confidenciais.", correct: true },
                    { text: "e) Um método de criptografia de dados em trânsito.", correct: false }
                ]
            },
            {
                question: "O que é um firewall?",
                answers: [
                    { text: "a) Um software de antivírus.", correct: false },
                    { text: "b) Um dispositivo de hardware que filtra o tráfego de rede.", correct: true },
                    { text: "c) Um protocolo de segurança para criptografia de dados.", correct: false },
                    { text: "d) Uma ferramenta de análise de vulnerabilidades.", correct: false },
                    { text: "e) Um método de autenticação de dois fatores.", correct: false }
                ]
            },
            {
                question: "O que é um ataque de força bruta?",
                answers: [
                    { text: "a) Um ataque que utiliza a força física para acessar um sistema.", correct: false },
                    { text: "b) Uma técnica de engenharia social.", correct: false },
                    { text: "c) Um ataque que explora falhas no código-fonte.", correct: false },
                    { text: "d) Uma tentativa de adivinhar uma senha por meio de repetidas tentativas.", correct: true },
                    { text: "e) Um ataque de negação de serviço distribuído (DDoS).", correct: false }
                ]
            },
            {
                question: "O que é criptografia de ponta a ponta?",
                answers: [
                    { text: "a) Um protocolo de segurança para redes Wi-Fi.", correct: false },
                    { text: "b) Uma técnica de mascaramento de endereços IP.", correct: false },
                    { text: "c) Um método de proteção contra malware.", correct: false },
                    { text: "d) Um sistema em que apenas as partes comunicantes podem entender as mensagens.", correct: true },
                    { text: "e) Uma forma de autenticação biométrica.", correct: false }
                ]
            },
            {
                question: "O que é um token de segurança?",
                answers: [
                    { text: "a) Uma senha temporária enviada por SMS.", correct: false },
                    { text: "b) Um dispositivo de hardware que gera códigos de acesso únicos.", correct: true },
                    { text: "c) Um certificado digital para servidores web.", correct: false },
                    { text: "d) Um método de autenticação baseado em biometria.", correct: false },
                    { text: "e) Um tipo de firewall.", correct: false }
                ]
            },
            {
                question: "O que é um ataque de injeção SQL?",
                answers: [
                    { text: "a) Um ataque físico a servidores de banco de dados.", correct: false },
                    { text: "b) Um ataque que explora vulnerabilidades de software.", correct: false },
                    { text: "c) Uma técnica de engenharia reversa.", correct: false },
                    { text: "d) Uma tentativa de inserir código malicioso em consultas SQL.", correct: true },
                    { text: "e) Um tipo de ataque de phishing.", correct: false }
                ]
            },
            {
                question: "O que é um certificado SSL?",
                answers: [
                    { text: "a) Um tipo de antivírus.", correct: false },
                    { text: "b) Um protocolo de segurança para redes locais.", correct: false },
                    { text: "c) Um dispositivo de hardware para filtrar tráfego de rede.", correct: false },
                    { text: "d) Um certificado que garante a segurança na camada de transporte.", correct: true },
                    { text: "e) Uma forma de autenticação por chave pública.", correct: false }
                ]
            }
        ];
    </script>

    <canvas id="Matrix"></canvas>
    <script>
        const canvas = document.getElementById('Matrix');
        const context = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';

        const alphabet = katakana + latin + nums;

        const fontSize = 16;
        const columns = canvas.width / fontSize;

        const rainDrops = [];

        for (let x = 0; x < columns; x++) {
            rainDrops[x] = 1;
        }

        const draw = () => {
            context.fillStyle = 'rgba(0, 0, 0, 0.05)';
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.fillStyle = '#0F0';
            context.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                context.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        };

        setInterval(draw, 30);
    </script>
</body>

</html>
    """
    return render_template_string(html_content)