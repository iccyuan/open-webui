/**
 * Agent Browser OpenAPI Server
 * 
 * A RESTful API server that wraps agent-browser with full OpenAPI 3.0 specification.
 * This server can be imported into Open WebUI as an external tool via openapi.json.
 * 
 * Installation:
 *   npm install express cors swagger-ui-express
 *   npm install -g agent-browser
 * 
 * Usage:
 *   node openapi-server.js
 * 
 * OpenAPI spec available at: http://localhost:5000/openapi.json
 * Swagger UI available at: http://localhost:5000/docs
 */

const express = require('express');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs');
const path = require('path');

const execPromise = util.promisify(exec);
const app = express();
const PORT = process.env.PORT || 5000;

// Load OpenAPI specification
const openapiSpec = JSON.parse(
    fs.readFileSync(path.join(__dirname, 'openapi.json'), 'utf8')
);

// Update server URL in spec based on environment
openapiSpec.servers[0].url = `http://localhost:${PORT}`;

// Middleware
app.use(cors());
app.use(express.json());

// Serve OpenAPI specification
app.get('/openapi.json', (req, res) => {
    res.json(openapiSpec);
});

// Serve Swagger UI
app.use('/docs', swaggerUi.serve, swaggerUi.setup(openapiSpec));

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        service: 'agent-browser-openapi',
        version: openapiSpec.info.version
    });
});

/**
 * POST /search
 * Search the web using agent-browser
 */
app.post('/search', async (req, res) => {
    try {
        const { query, maxResults = 5 } = req.body;

        if (!query) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'Query parameter is required'
            });
        }

        console.log(`[Search] Query: "${query}", Max Results: ${maxResults}`);

        // Construct Google search URL
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;

        // Use agent-browser to fetch search results
        // Note: Adjust selector based on actual Google HTML structure
        const command = `agent-browser browse "${searchUrl}" --selector ".g" --extract "title:.LC20lb, link:a[href], snippet:.VwiC3b" --format json --limit ${maxResults}`;

        const { stdout, stderr } = await execPromise(command, {
            timeout: 30000,
            maxBuffer: 1024 * 1024 * 10
        });

        if (stderr) {
            console.warn(`[Search] Warning: ${stderr}`);
        }

        let results = [];
        try {
            const parsed = JSON.parse(stdout);
            results = Array.isArray(parsed) ? parsed : [parsed];
        } catch (parseError) {
            console.warn('[Search] Failed to parse JSON, returning empty results');
        }

        res.json({
            query,
            results,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('[Search] Error:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: error.message
        });
    }
});

/**
 * POST /browse
 * Browse a URL and extract content
 */
app.post('/browse', async (req, res) => {
    try {
        const { url, selector = 'body', extract = 'text' } = req.body;

        if (!url) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'URL parameter is required'
            });
        }

        console.log(`[Browse] URL: "${url}", Selector: "${selector}"`);

        let command = `agent-browser browse "${url}"`;

        if (selector) {
            command += ` --selector "${selector}"`;
        }

        if (extract) {
            command += ` --extract "${extract}"`;
        }

        command += ` --format json`;

        const { stdout, stderr } = await execPromise(command, {
            timeout: 30000,
            maxBuffer: 1024 * 1024 * 10
        });

        if (stderr) {
            console.warn(`[Browse] Warning: ${stderr}`);
        }

        let content;
        try {
            content = JSON.parse(stdout);
        } catch (parseError) {
            content = { text: stdout };
        }

        res.json({
            url,
            content,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('[Browse] Error:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: error.message
        });
    }
});

/**
 * POST /screenshot
 * Take a screenshot of a URL
 */
app.post('/screenshot', async (req, res) => {
    try {
        const { url } = req.body;

        if (!url) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'URL parameter is required'
            });
        }

        console.log(`[Screenshot] URL: "${url}"`);

        const command = `agent-browser screenshot "${url}" --format base64`;

        const { stdout, stderr } = await execPromise(command, {
            timeout: 30000,
            maxBuffer: 1024 * 1024 * 50
        });

        if (stderr) {
            console.warn(`[Screenshot] Warning: ${stderr}`);
        }

        res.json({
            url,
            screenshot: stdout.trim(),
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('[Screenshot] Error:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: error.message
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({
        error: 'Internal Server Error',
        message: err.message
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Agent Browser OpenAPI Server running on http://localhost:${PORT}`);
    console.log(`📋 OpenAPI Spec: http://localhost:${PORT}/openapi.json`);
    console.log(`📖 Swagger UI: http://localhost:${PORT}/docs`);
    console.log(`\n🔧 To use in Open WebUI:`);
    console.log(`   1. Go to Workspace -> Tools`);
    console.log(`   2. Click "Import Tool"`);
    console.log(`   3. Enter URL: http://localhost:${PORT}/openapi.json`);
    console.log(`   (Use http://host.docker.internal:${PORT}/openapi.json if Open WebUI is in Docker)\n`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('SIGINT received, shutting down gracefully...');
    process.exit(0);
});
