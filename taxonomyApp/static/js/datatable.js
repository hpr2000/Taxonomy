$(document).ready(function() {
    // Function to perform the AJAX call and populate the table
    function callAjax(url, success) {
        $.ajax({
            url: '/get_data/',
            type: 'GET',
            success: function(data) {
                // Parse the JSON data
                var responseData = JSON.parse(data);

                // Get the maximum number of levels present in the Hierarchy field
                var maxLevels = responseData.data.reduce(function(max, item) {
                    return Math.max(max, item.Hierarchy.length);
                }, 0);

                // Define columns for DataTable
                var columns = [];

                // Create columns for each level in the Hierarchy
                for (var i = 0; i < maxLevels; i++) {
                    columns.push({
                        data: 'Hierarchy.' + i,
                        title: 'Level ' + (i + 1)
                    });
                }

                // Add Description column
                columns.push({ data: 'Description', title: 'Description' });

                // Initialize DataTable with parsed data and columns
                $('#hierarchyTable').DataTable({
                    data: responseData.data,
                    columns: columns
                });
            },
            error: function(error) {
                console.log('Error fetching data:', error);
            }
        });
    }

    // Call the AJAX function
    callAjax();
});
