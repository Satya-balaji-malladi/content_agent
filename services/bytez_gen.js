import Bytez from "bytez.js";
import fs from "fs";
import https from "https";

const key = process.argv[2];
const prompt = process.argv[3];
const outputFile = process.argv[4] || "generated_video.mp4";

if (!key || !prompt) {
    console.error("Usage: node bytez_gen.js <API_KEY> <PROMPT> [OUTPUT_FILE]");
    process.exit(1);
}

const sdk = new Bytez(key);
const model = sdk.model("Wan-AI/Wan2.1-T2V-14B");

console.log(`Generating video for prompt: "${prompt}"...`);

async function run() {
    try {
        const { error, output } = await model.run(prompt);

        if (error) {
            console.error("Bytez Error:", error);
            process.exit(1);
        }

        console.log("Generation Success. Output URL:", output);

        // Output might be a base64 string or a URL. 
        // Bytez usually returns a URL or a buffer. Let's handle both or check docs.
        // Assuming output is a URL based on common T2V APIs.

        // Check if output is a Data URI
        if (output && output.startsWith('data:')) {
            const base64Data = output.split(';base64,').pop();
            fs.writeFileSync(outputFile, base64Data, { encoding: 'base64' });
            console.log(`Video saved to ${outputFile}`);
        }
        else if (output && output.startsWith('http')) {
            // Download file
            const file = fs.createWriteStream(outputFile);
            https.get(output, function (response) {
                response.pipe(file);
                file.on('finish', function () {
                    file.close(() => {
                        console.log(`Video downloaded to ${outputFile}`);
                        process.exit(0);
                    });
                });
            }).on('error', function (err) {
                console.error("Download Error:", err);
                process.exit(1);
            });
        }
        else {
            // It might be a raw buffer or object?
            console.log("Raw Output:", output);
            // Try writing directly if it's a buffer-like object
            fs.writeFileSync(outputFile, output);
        }

    } catch (e) {
        console.error("Script Error:", e);
        process.exit(1);
    }
}

run();
