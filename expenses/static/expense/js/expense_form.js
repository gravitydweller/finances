/* expenses/static/expense/js/expense_form.js */

document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("expense-form");
    var utilityChoiceField = document.getElementById("id_utility_choice");
    var loanChoiceField = document.getElementById("id_loan_choice");

    var descriptionField = document.getElementById("id_description");
    var tagField = document.getElementById("id_tag");
    var categoryField = document.getElementById("id_category");

    // Set default value for tag and category fields on page load
    setSelectedValue(tagField, "");
    setSelectedValue(categoryField, "normal expense");

    // Set the date field to the current date and time
    var dateField = document.getElementById("id_date");
    if (dateField) {
        var now = new Date();
        var formattedDate = now.toISOString().slice(0, 16);
        dateField.value = formattedDate;
    }

    // Add event listener for utility choice change
    utilityChoiceField.addEventListener("change", handleUtilityChoiceChange);

    // Trigger utility choice change event initially
    handleUtilityChoiceChange();

    // Function to handle utility choice change
    function handleUtilityChoiceChange() {
        var selectedUtility = utilityChoiceField.value;

        if (selectedUtility) {
            // Construct the description string
            var now = new Date();
            var year = now.getFullYear();
            var month = now.getMonth(); // Get the current month (0-11)
            var monthNames = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
            var previousMonthName = monthNames[(month === 0) ? 11 : month - 1]; // Get the name of the previous month
            var description = selectedUtility + " " + previousMonthName + " " + year;

            // Update the description field
            descriptionField.value = description;

            // Set the tag and category fields to "utility expense"
            setSelectedValue(tagField, "utility");
            setSelectedValue(categoryField, "utility expense");
        } else {
            // Reset the tag, category, and description fields
            descriptionField.value = "";
            setSelectedValue(tagField, "");
            setSelectedValue(categoryField, "normal expense"); // Default value when no utility choice is selected
        }
    }

    // Function to set the selected value of a select element
    function setSelectedValue(selectObj, valueToSet) {
        for (var i = 0; i < selectObj.options.length; i++) {
            if (selectObj.options[i].text === valueToSet) {
                selectObj.options[i].selected = true;
                return;
            }
        }
    }

    // Add event listener for loan choice change
    loanChoiceField.addEventListener("change", handleLoanChoiceChange);

    // Trigger loan choice change event initially
    handleLoanChoiceChange();

    // Function to handle loan choice change
    function handleLoanChoiceChange() {
        var selectedLoan = loanChoiceField.value;

        if (selectedLoan) {
            // Get the selected option's text (assuming the option value is the loan ID)
            var loanName = loanChoiceField.options[loanChoiceField.selectedIndex].text;

            // Construct the description string
            var description = "expense for " + loanName;

            // Update the description field
            descriptionField.value = description;

            // Set the tag field to the loan name
            setSelectedValue(tagField, loanName);

            // Set the category field to "loan expense"
            setSelectedValue(categoryField, "loan expense");
        } else {
            // Reset the tag, category, and description fields
            descriptionField.value = "";
            setSelectedValue(tagField, "");
            setSelectedValue(categoryField, "normal expense"); // Default value when no loan choice is selected
        }
    }   

});
