var modal = document.getElementById("myModal");

        // Function to open the modal
        function openModal() {
            modal.style.display = "grid";
            var initialMessage = document.getElementById("initialMessage").textContent.trim();
            displayChatbotMessage(initialMessage);
        }

        // Function to close the modal
        function closeModal() {
            modal.style.display = "none";
        }

        function displayChatbotMessage(message) {
            var chatbotDiv = document.getElementById("chatbot");
            // Create div for logo
            var logoDiv = document.createElement("div");
            logoDiv.className = "logo";
            var logoImg = document.createElement("img");
            logoImg.style.height = '35px';
            logoImg.style.width = '35px';
            logoImg.src = "{% static 'supply/chat.png' %}"; // Replace with the actual path to your logo image
            logoDiv.appendChild(logoImg);
            
            // Create div for chatbot message
            var messageElement = document.createElement("div");
            
            messageElement.className = "chatbot-message";
            messageElement.textContent = message;
            messageElement.appendChild(logoDiv);
            // Append logo and message to chatbot div
            
            chatbotDiv.appendChild(messageElement);
        }

        function sendMessage() {
            var userInput = document.getElementById("userInput").value;
            var chatbotDiv = document.getElementById("chatbot");
            var messageElement2 = document.createElement("div");
            messageElement2.className = "user-message";
            messageElement2.textContent =  userInput;
            chatbotDiv.appendChild(messageElement2);
        }

        // Function to handle form submission using AJAX
        $("#chatForm").submit(function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        var formData = $(this).serialize();
            $.ajax({
                type: "POST",
                url: "{% url 'supply' %}",
                data: formData,
                success: function(response) {
                displayChatbotMessage(response.message);
                },
                error: function(xhr, status, error) {
                console.error("Error sending user message:", error);
                }
            });
        });

        var ctx = document.getElementById('myChart').getContext('2d');
        var Hotspot_Name = {{ Hotspot_Name|safe }};
        Hotspot_Name.sort().reverse()
        var Food_needed = {{ Food_needed|safe }};
        Food_needed.sort().reverse()
        console.log(Hotspot_Name)

        var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Hotspot_Name,
            datasets: [{
                label: 'Food Needed',
                data: Food_needed,  // Replace with your actual chart_data array
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });