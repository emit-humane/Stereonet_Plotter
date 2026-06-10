function exportSelectedFormat() {
    const format = document.getElementById('exportFormat').value;
    console.log("Selected format:", format);  // Debugging line to confirm format selection
    exportPlot(format);
}

function exportPlot(format) {
    console.log("Exporting format:", format);  // Debugging line to check if function is called

    fetch(`/export_plot?format=${format}`)
        .then(response => {
            if (format === 'png') {
                response.json().then(data => {
                    console.log("PNG Data:", data.plot_data);  // Debugging line to verify PNG data

                    if (data.plot_data) {
                        const imgData = `data:image/png;base64,${data.plot_data}`;
                        const link = document.createElement('a');
                        link.href = imgData;
                        link.download = 'stereonet_plot.png';
                        link.click();
                    } else {
                        console.error("No PNG data found.");
                    }
                }).catch(error => console.error("Error parsing PNG JSON:", error));
            } else {
                response.blob().then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `stereonet_plot.${format}`;
                    link.click();
                    window.URL.revokeObjectURL(url);
                }).catch(error => console.error("Error processing blob:", error));
            }
        })
        .catch(error => console.error('Error exporting plot:', error));
}

// Function to update Dip Direction based on the input in Strike field
function updateDipDirection() {
    const strikeField = document.getElementById('strike');
    const dipDirectionField = document.getElementById('dipDirection');
    const strikeValue = strikeField.value;

    // If Strike field is empty, clear Dip Direction field
    if (strikeValue === '') {
        dipDirectionField.value = '';
    } else {
        const strike = parseFloat(strikeValue);
        if (!isNaN(strike)) {
            const dipDirection = (strike + 90) % 360;
            dipDirectionField.value = dipDirection;
        }
    }
}

// Function to update Strike based on the input in Dip Direction field
function updateStrikeDirection() {
    const dipDirectionField = document.getElementById('dipDirection');
    const strikeField = document.getElementById('strike');
    const dipDirectionValue = dipDirectionField.value;

    // If Dip Direction field is empty, clear Strike field
    if (dipDirectionValue === '') {
        strikeField.value = '';
    } else {
        const dipDirection = parseFloat(dipDirectionValue);
        if (!isNaN(dipDirection)) {
            const strike = (dipDirection - 90 + 360) % 360; // Adding 360 ensures a positive angle
            strikeField.value = strike;
        }
    }
}

$(document).ready(function() {
    // Clear plot data from the session when the page loads
    $.ajax({
        url: '/clear_plot_data',
        type: 'POST',
        success: function() {
            console.log("Plot data cleared from session.");
        },
        error: function() {
            console.error("Failed to clear plot data from session.");
        }
    });

    // Handle plot type selection
    $('#plotType').change(function() {
        if ($(this).val() === 'line') {
            $('#lineInputs').show();
            $('#planeInputs').hide();
        } else {
            $('#lineInputs').hide();
            $('#planeInputs').show();
        }
    });

    // Add plot data
    $('#addPlot').click(function() {
        const plotType = $('#plotType').val();
        const data = {
            type: plotType,
            trend: plotType === 'line' ? parseFloat($('#trend').val()) : null,
            plunge: plotType === 'line' ? parseFloat($('#plunge').val()) : null,
            strike: plotType === 'plane' ? parseFloat($('#strike').val()) : null,
            dip_direction: plotType === 'plane' ? parseFloat($('#dipDirection').val()) : null,
            dip_angle: plotType === 'plane' ? parseFloat($('#dipAngle').val()) : null
        };

        $.ajax({
            url: '/plot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function(response) {
                $('#stereonetImage').attr('src', 'data:image/png;base64,' + response.plot_data);
                updatePlotTable();
            }
        });
    });

    // Update plot table
    function updatePlotTable() {
        $.getJSON('/get_plot_data', function(plotData) {
            $('#plotTable tbody').empty();
            $.each(plotData.lines, function(index, line) {
                $('#plotTable tbody').append(`
                    <tr>
                        <td>Line</td>
                        <td>Trend: ${line[0]}, Plunge: ${line[1]}</td>
                        <td><button class="deletePlot" data-type="line" data-index="${index}">Delete</button></td>
                    </tr>
                `);
            });
            $.each(plotData.planes, function(index, plane) {
                $('#plotTable tbody').append(`
                    <tr>
                        <td>Plane</td>
                        <td>Strike: ${plane[0]}, Dip Direction: ${plane[1]}, Dip Angle: ${plane[2]}</td>
                        <td><button class="deletePlot" data-type="plane" data-index="${index}">Delete</button></td>
                    </tr>
                `);
            });
        });
    }

    // Delete plot data
    $('#plotTable').on('click', '.deletePlot', function() {
        const plotType = $(this).data('type');
        const index = $(this).data('index');

        $.ajax({
            url: '/delete',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ type: plotType, index: index }),
            dataType: 'json',
            success: function(response) {
                $('#stereonetImage').attr('src', 'data:image/png;base64,' + response.plot_data);
                updatePlotTable();
            }
        });
    });

    // Initial load
    updatePlotTable();
});