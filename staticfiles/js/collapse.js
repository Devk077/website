window.addEventListener('load', function () {
    // Find all collapse elements
    var collapseElements = document.querySelectorAll('.collapse');

    // Loop through each collapse element
    collapseElements.forEach(function (element) {
        // Remove the 'collapse' class
        element.classList.remove('collapse');
        // Add the 'show' class to expand the element
        element.classList.add('show');
    });
});
