function logMessage(message, isError) {
    console.log(message);
    var outputDiv = document.getElementById("output");

    if (isError) {
        outputDiv.innerHTML += '<br><span style="color:red;">' + message + '</span>';
    } else {
        outputDiv.innerHTML += '<br>' + message;
    }
}

// Main function to run BFS AMCC when the button is clicked
function runBFS(event) {
    event.preventDefault();
    logMessage("Running BFS AMCC... Please wait.");
    $("#spinner").show();

     var formData = {};
     $(event.target).serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
     });

    $.ajax({
        url: '/run',
        type: 'POST',
        dataType: 'json',
        data: formData,
        success: function (data) {
            $("#spinner").hide();
            if (data.status === "success") {
                logMessage("BFS processing was successful!");

                if (data.messages && data.messages.length > 0) {
                    data.messages.forEach(function (msg) {
                        logMessage(msg);
                    });
                }
            } else {
                logMessage("Error: " + (data.message || "Unknown error occurred during BFS processing!"), true);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $("#spinner").hide();
            logMessage("AJAX Error: " + textStatus + ": " + errorThrown, true);
        }
    });
}

$(document).ready(function() {
    // Set up the button event listener
    $("#run").submit(runBFS);

    // Fetch logs every second and display them
    window.setInterval(function () {
        $.get("/log", function(logs) {
            logs.forEach(function(log) {
                logMessage(log);
            });
        });
    }, 1000);

    logMessage("Program loaded and ready!");
});