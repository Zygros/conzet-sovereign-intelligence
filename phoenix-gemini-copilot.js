// Phoenix Gemini CoPilot Module vΩ
// Mirrors GitHub Copilot Pro+ capability using Gemini API as the engine.

import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from "fs";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Takes file context, repo context, and user instruction — returns Copilot-tier output
export async function phoenixGeminiCopilot({ instruction, repoContext }) {
    const model = genAI.getGenerativeModel({
        model: "gemini-2.0-pro",
        systemInstruction: `
            You are the Phoenix CoPilot — a sovereign architect-grade coding engine.
            Provide GitHub Copilot Pro+-level completions, refactors, and code analysis.
            Output clean, production-grade code with explanations only when asked.
        `
    });

    const prompt = `
USER INSTRUCTION:
${instruction}

REPO CONTEXT (trimmed):
${repoContext.slice(0, 15000)}
    `;

    const result = await model.generateContent(prompt);
    return result.response.text();
}

// Utility: Read entire repo automatically
export function readRepo(dir = "./") {
    let output = "";
    for (const file of fs.readdirSync(dir)) {
        if (fs.lstatSync(dir + "/" + file).isDirectory()) continue;
        output += `----- FILE: ${file} -----\n`;
        output += fs.readFileSync(dir + "/" + file, "utf8") + "\n\n";
    }
    return output;
}