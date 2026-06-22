const http = require("http");
const TOKEN = "gbrain_0541532fb241cca779103ea73052d2de0856621431f9b3711bd9a03a262684dc";

let buffer = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", c => buffer += c);
process.stdin.on("end", () => {
  try {
    const request = JSON.parse(buffer);
    const postData = JSON.stringify(request);
    
    const options = {
      hostname: "127.0.0.1",
      port: 3131,
      path: "/mcp",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": "Bearer " + TOKEN,
        "Content-Length": Buffer.byteLength(postData)
      },
      timeout: 30000
    };

    const req = http.request(options, res => {
      let data = "";
      res.on("data", c => data += c);
      res.on("end", () => {
        try {
          // Parse SSE format: "event: message\ndata: {...}\n\n"
          const lines = data.split("\n");
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const jsonStr = line.substring(6);
              const json = JSON.parse(jsonStr);
              process.stdout.write(JSON.stringify(json));
              process.exit(0);
            }
          }
          // Fallback: try parse directly
          process.stdout.write(JSON.stringify(JSON.parse(data)));
          process.exit(0);
        } catch (e) {
          process.stderr.write("Parse error: " + e.message + "\n");
          process.exit(1);
        }
      });
    });

    req.on("error", e => {
      process.stderr.write("HTTP error: " + e.message + "\n");
      process.exit(1);
    });

    req.on("timeout", () => {
      req.destroy();
      process.stderr.write("Timeout\n");
      process.exit(1);
    });

    req.write(postData);
    req.end();
  } catch (e) {
    process.stderr.write("Error: " + e.message + "\n");
    process.exit(1);
  }
});