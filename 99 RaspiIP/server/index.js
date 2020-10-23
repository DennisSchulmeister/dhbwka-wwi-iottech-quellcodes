#!/usr/bin/env node

/*
 * Copyright © 2020 Dennis Schulmeister-Zimolong
 *
 * E-Mail: dhbw@windows3.de
 * Webseite: https://www.wpvs.de/
 *
 * Dieser Quellcode ist lizenziert unter einer
 * Creative Commons Namensnennung 4.0 International Lizenz.
 */

// Modulimporte
const path = require("path");
const express = require("express");
const bodyParser = require('body-parser')
const expressNunjucks = require("express-nunjucks");
const yargs = require('yargs');

const app = express();
app.use(bodyParser.json()) // for parsing application/json

// Webserver-Konfiguration
let staticDir = path.normalize(path.join(__dirname, "static"));
app.use(express.static(staticDir));

let templateDir = path.normalize(path.join(__dirname, "templates"));
app.set("views", templateDir);

let isDev = app.get("env") === "development";

expressNunjucks(app, {
    watch: isDev,
    noCache: isDev
});

// URL-Routing
app.get("/", (request, response) => {
    response.render("index");
});

app.get("/:device", (request, response) => {
    // request.params.device
});

app.put("/:device", (request, response) => {
    // request.params.device
    response.json({
        "message": "success",
    });
});

// Serverstart
const argv = yargs.command("port", {
    alias: "p",
    description: "Port number",
    default: 8888,
    type: Number,
}).help().alias('help', 'h').argv;

app.listen(argv.port, () => {
    console.log(`Webservier steht auf Port ${argv.port} bereit!`);
});
