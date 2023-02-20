$(document).ready(function() {
    // Send AJAX request when form is submitted
    $('#task-form').submit(function(event) {
      event.preventDefault();
      var form = $(this);
      var data = form.serialize();
      $.ajax({
        url: '/scan',
        method: 'POST',
        data: data,
        success: function(result) {
          // Add task card to In Progress section
          var taskCard = createTaskCard(result.task_id, result.scan_type, result.ip, result.port_range);
          $('#task-cards').append(taskCard);
          // Set interval to check task status and update card
          var intervalId = setInterval(function() {
            $.ajax({
              url: '/task/' + result.task_id,
              method: 'GET',
              success: function(taskResult) {
                updateTaskCard(taskCard, taskResult.status, taskResult.result, taskResult.traceback);
                if (taskResult.status == 'SUCCESS' || taskResult.status == 'FAILURE') {
                  clearInterval(intervalId);
                  // Move task card to Completed section
                  taskCard.appendTo($('#completed-task-cards'));
                }
              }
            });
          }, 1000);
        }
      });
    });
  });

    // Create a task card
    function createTaskCard(taskId, scanType, ip, portRange) {
        var taskCard = $('<div>', {'class': 'card', 'id': taskId});
        var cardBody = $('<div>', {'class': 'card-body'});
        var cardTitle = $('<h5>', {'class': 'card-title', 'text': 'Task ' + taskId});
        var cardText = $('<p>', {'class': 'card-text', 'text': 'Scan Type: ' + scanType + ' | IP: ' + ip + ' | Port Range: ' + portRange});
        var cardStatus = $('<p>', {'class': 'card-text', 'text': 'Status: In Progress'});
        cardBody.append(cardTitle);
        cardBody.append(cardText);
        cardBody.append(cardStatus);
        taskCard.append(cardBody);
        return taskCard;
      }
      
      function updateTaskCard(taskCard, status, result, traceback) {
        var cardStatus = taskCard.find('.card-text').eq(1);
        cardStatus.text('Status: ' + status);
        if (status == 'SUCCESS') {
          cardStatus.removeClass('text-warning').addClass('text-success');
          cardStatus.after($('<p>', {'class': 'card-text', 'text': 'Result: ' + result}));
        } else if (status == 'FAILURE') {
          cardStatus.removeClass('text-warning').addClass('text-danger');
          cardStatus.after($('<p>', {'class': 'card-text', 'text': 'Error: ' + traceback}));
        }
      }      