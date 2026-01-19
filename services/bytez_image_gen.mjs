import Bytez from "bytez.js";
import fs from "fs";
import https from "https";

// Arguments: API_KEY, PROMPT, OUTPUT_PATH
const apiKey = process.argv[2];
const promptText = process.argv[3];
const outputPath = process.argv[4];

if (!apiKey || !promptText || !outputPath) {
    console.error("Usage: node bytez_image_gen.mjs <API_KEY> <PROMPT> <OUTPUT_PATH>");
    process.exit(1);
}

const sdk = new Bytez(apiKey);
// Using SDXL 1.0 as requested
const model = sdk.model("stabilityai/stable-diffusion-xl-base-1.0");

async function generate() {
    try {
        console.log(`Generating image...`);
        // model.run returns { error, output }
        const { error, output } = await model.run(promptText);

        if (error) {
            console.error("Bytez API Error:", error);
            process.exit(1);
        }

        if (output) {
            // Handle URL output (common for image models on Bytez)
            if (typeof output === 'string' && output.startsWith("http")) {
                const file = fs.createWriteStream(outputPath);
                https.get(output, (response) => {
                    response.pipe(file);
                    file.on('finish', () => {
                        file.close(() => {
                            console.log("SUCCESS");
                            process.exit(0);
                        });
                    });
                }).on('error', (err) => {
                    console.error("Download Error:", err);
                    process.exit(1);
                });
            }
            // Handle Base64 Data URI
            else if (typeof output === 'string' && output.startsWith("data:")) {
                const base64Data = output.split(';base64,').pop();
                fs.writeFileSync(outputPath, base64Data, { encoding: 'base64' });
                console.log("SUCCESS");
                process.exit(0);
            }
            // Handle Buffer directly
            else {
                fs.writeFileSync(outputPath, output);
                console.log("SUCCESS");
                process.exit(0);
            }
        } else {
            console.error("No output received from Bytez.");
            process.exit(1);
        }

    } catch (e) {
        console.error("Script Exception:", e);
        process.exit(1);
    }
}

generate();
